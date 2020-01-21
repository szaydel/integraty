# -*- coding: utf-8 -*-

import itertools
import json
import os
import re
import subprocess
import shlex
import signal
import sys
import locale
import errno

from functools import reduce
from typing import TypeVar, Callable, Sequence

from pexpect.popen_spawn import PopenSpawn
import pexpect

pexpect.EOF.__module__ = "pexpect.exceptions"

# Include `unicode` in STR_TYPES for Python 2.X
try:
    STR_TYPES = (str, unicode)
except NameError:
    STR_TYPES = (str,)

PCHARS = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


def stripper(w, chars):
    if chars:
        return stripper(w.replace(chars[0], ""), chars[1:])
    else:
        return w


class NoCommandException(Exception):
    pass


class InvalidStream(Exception):
    pass


class ExternalProgramException(Exception):
    pass


def pid_exists(pid):
    """Check whether pid exists in the current process table."""
    if pid == 0:
        # According to "man 2 kill" PID 0 has a special meaning:
        # it refers to <<every process in the process group of the
        # calling process>> so we don't want to go any further.
        # If we get here it means this UNIX platform *does* have
        # a process with id 0.
        return True
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH) therefore we should never get
            # here. If we do let's be explicit in considering this
            # an error.
            raise err
    else:
        return True


class ExternalProgram(object):
    """
    ExternalProgram is an abstraction over the subprocess module with
    convenience methods for running processes or pipelines and fetching
    results from executed programs as well as collecting their stdout
    and stderr. Optionally, there is also expect functionality to interact
    with programs which require some level of interaction from user.

    You may use this class as a context manager, since ExternalProgram
    implements this functionality. It may be more convenient depending upon
    how the results are going to be used.
    
    Because this is really meant to be used as part of a testing framework
    primary focus is on usability and minimal boilerplate, while having
    as much expressiveness as possible. Context managers positively contribute
    to this goal. Here are some examples to make this a little more concrete:

    >>> from integraty import extprog
    >>> from pprint import pprint
    >>> with extprog.ExternalProgram('dig microsoft.com') as c:
    ...     c.do_shell()
    ...     res = c.stdout_map_func(lambda l: dict(zip(('name', 'ttl', 'class','q_type', 'address'), l.split())), pattern='^microsoft.com')
    ...     pprint([n['name'] == 'microsoft.com.' for n in res])
    ...     pprint(sorted([n['address'] for n in res]))
    [True, True, True, True, True]
    ['104.215.148.63',
     '13.77.161.179',
     '40.112.72.205',
     '40.113.200.201',
     '40.76.4.15']

    Try this out with `python3 -m doctest integraty/extprog.py` if you have
    sources checked out in a convenient place.
    """
    def __init__(self, cmd, timeout=None):
        super(ExternalProgram, self).__init__()
        self.cmd = cmd
        self.timeout = timeout
        self.subprocess = None
        self.blocking = None
        self.was_run = False
        self.__out = None
        self.__err = None

    def __repr__(self):
        return "ExternalProgram({!r}, timeout={})".format(
            self.cmd, self.timeout
        )

    def __enter__(self):
        return self

    # FIXME: Do something useful with exc_* args.
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.std_out.closed:
            self.std_out.close()
        if not self.std_err.closed:
            self.std_err.close()

    @property
    def _popen_args(self):
        return self.cmd

    @property
    def _default_popen_kwargs(self):
        return {
            "env": os.environ.copy(),
            "stdin": subprocess.PIPE,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "shell": True,
            "universal_newlines": True,
            "bufsize": 0,
        }

    @property
    def _default_pexpect_kwargs(self):
        encoding = "utf-8"
        if sys.platform == "win32":
            default_encoding = locale.getdefaultlocale()[1]
            if default_encoding is not None:
                encoding = default_encoding
        return {
            "env": os.environ.copy(),
            "encoding": encoding,
            "timeout": self.timeout,
        }

    @property
    def _uses_subprocess(self):
        return isinstance(self.subprocess, subprocess.Popen)

    @property
    def _uses_pexpect(self):
        return isinstance(self.subprocess, PopenSpawn)

    ### String Processing Private Methods Below ###

    def _lines_from_impl(self, pattern=None, exclude=False, stream=None):
        if stream == "stdout":
            return self._stdout_lines(pattern=pattern, exclude=exclude)
        elif stream == "stderr":
            return self._stderr_lines(pattern=pattern, exclude=exclude)
        else:
            raise InvalidStream("Allowed streams are stdout and stderr")

    def _splitlines(self, stream="stdout"):
        if not self.was_run:
            raise ExternalProgramException(
                "Run program to obtain results before requesting resulting data"
            )
        if stream == "stdout":
            return [l.strip() for l in self.out.splitlines()]
        elif stream == "stderr":
            return [l.strip() for l in self.err.splitlines()]
        else:
            raise InvalidStream("Allowed streams are stdout and stderr")

    def _stdout_lines(self, pattern=None, exclude=False):
        lines = self._splitlines()
        filtered_lines = None
        if pattern and exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        elif pattern:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return filtered_lines if filtered_lines else lines

    def _stderr_lines(self, pattern=None, exclude=False):
        lines = self._splitlines(stream="stderr")
        filtered_lines = None
        if pattern and exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        elif pattern:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return filtered_lines if filtered_lines else lines

    def _line_tuples(
        self,
        sep=None,
        pattern=None,
        exclude=False,
        strip_punct=False,
        strip_chars=PCHARS,
        stream="stdout",
    ):
        new_lines = []
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        for l in lines:
            tokens = tuple(l.split(sep))
            if tokens:
                if strip_punct:
                    tokens = tuple(
                        stripper(tok, strip_chars) for tok in tokens
                    )
                new_lines.append(tokens)
        return new_lines

    def _trim_prefix(
        self, prefix, pattern=None, exclude=False, stream="stdout"
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return [
            l[len(prefix):].strip() if l.startswith(prefix) else l
            for l in lines
        ]

    def _trim_suffix(
        self, suffix, pattern=None, exclude=False, stream="stdout"
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return [
            l[: l.rindex(suffix)].strip() if l.endswith(suffix) else l
            for l in lines
        ]

    def _with_prefix(
        self, prefix=None, pattern=None, exclude=False, stream="stdout"
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )
        if not prefix:
            return lines

        return [l for l in lines if l.startswith(prefix)]

    def _with_suffix(
        self, suffix=None, pattern=None, exclude=False, stream="stdout"
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )
        if not suffix:
            return lines

        return [l for l in lines if l.endswith(suffix)]

    def _with_substr(self, substr=None, exclude=False, stream="stdout"):
        lines = self._lines_from_impl(stream=stream)
        if not substr:
            return lines
        if exclude:
            return [l for l in lines if l.find(substr) == -1]
        return [l for l in lines if l.find(substr) >= 0]

    def _at_least_n_substr(self, substr=None, n=0, stream="stdout"):
        lines = self._lines_from_impl(stream=stream)
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) >= n]

    def _at_most_n_substr(self, substr=None, n=0, stream="stdout"):
        lines = self._lines_from_impl(stream=stream)
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) <= n]

    def _first_last_n(
        self, n=1, pattern=None, exclude=False, first=True, stream="stdout"
    ):
        lines = self._lines_from_impl(stream=stream)
        if n < 1:
            raise ValueError("Number of lines cannot be less than '1'")
        if first:
            slc_obj = slice(0, n, 1)
        else:
            slc_obj = slice(-n, len(lines), 1)
        if not pattern:
            unfiltered_lines = [l for l in lines]
            return unfiltered_lines[slc_obj]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
            return filtered_lines[slc_obj]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return filtered_lines[slc_obj]

    def _head(self, sep=None, pattern=None, exclude=False, stream="stdout"):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return [col.split(sep)[0].strip() for col in lines]

    def _tail(self, sep=None, pattern=None, exclude=False, stream="stdout"):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return [tuple(col.split(sep)[1:]) for col in lines]

    def _columns(self, sep=None, pattern=None, exclude=False, stream="stdout"):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return list(
            zip(*map(lambda x: map(lambda x: x.strip(), x.split()), lines))
        )

    def _take_column(
        self, sep=None, column=0, pattern=None, exclude=False, stream="stdout"
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )
        return [col.split(sep)[column].strip() for col in lines]

    def _take_some_columns(
        self,
        sep=None,
        selectors=(),
        pattern=None,
        exclude=False,
        stream="stdout",
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return [
            tuple(itertools.compress(col.split(sep), selectors))
            for col in lines
        ]

    def _take_range_columns(
        self,
        sep=None,
        slc_range=(0, 1, 1),
        pattern=None,
        exclude=False,
        stream="stdout",
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )
        slc_obj = slice(*slc_range)

        return [col.split(sep)[slc_obj] for col in lines]

    def _to_dict_func(
        self, func, pattern=None, exclude=False, stream="stdout",
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return dict(func(line) for line in lines)

    def _to_tuple_func(
        self, func, pattern=None, exclude=False, stream="stdout",
    ):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )

        return [func(line) for line in lines]

    def _filter_func(self, func, exclude=False, stream="stdout"):
        lines = self._lines_from_impl(stream=stream)
        if exclude:
            filtered_lines = [line for line in lines if not func(line)]
        else:
            filtered_lines = [line for line in lines if func(line)]
        return filtered_lines

    def _map_func(self, func, pattern=None, exclude=False, stream="stdout"):
        lines = self._lines_from_impl(
            pattern=pattern, exclude=exclude, stream=stream
        )
        return [func(line) for line in lines]

    def _json_loads(self, stream="stdout"):
        if stream == "stdout":
            json_string = self.out
        elif stream == "stderr":
            json_string = self.err
        else:
            raise InvalidStream("Allowed streams are stdout and stderr")
        if not json_string:
            return None
        d = {}
        try:
            d = json.loads(json_string)
        except json.JSONDecodeError:
            return None
        return d

    def _dict_from_line(
        self, keys=None, sep=None, pattern=None, exclude=False, stream="stdout"
    ):
        lines = self._lines_from_impl(stream=stream)
        if not pattern:
            return [
                dict(
                    zip(
                        keys
                        if keys
                        else [i for i in range(0, len(col.split(sep)))],
                        col.split(sep),
                    )
                )
                for col in lines
            ]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [
            dict(
                zip(
                    keys
                    if keys
                    else [i for i in range(0, len(col.split(sep)))],
                    col.split(sep),
                )
            )
            for col in filtered_lines
        ]

    def _funcs_pipeline(self, *funcs, stream="stdout"):
        lines = self._lines_from_impl(stream=stream)
        T = TypeVar("T")

        def pipeline(value: T, funcs: Sequence[Callable[[T], T]],) -> T:
            return reduce(lambda v, f: f(v), funcs, value)

        return [
            pipeline(line, *funcs) for line in lines
        ]  # pylint: disable=no-value-for-parameter

    ### End String Processing Private Methods ###

    ### String Processing Public Methods Below ###

    @property
    def stdout_json_loads(self):
        """
        For JSON data written to stdout, attempt to convert to native data type.

        Returns:
            bool, int, string, dict, list: Unmarshaled JSON data.
        """
        return self._json_loads()

    @property
    def stderr_json_loads(self):
        """
        For JSON data written to stderr, attempt to convert to native data type.

        Returns:
            bool, int, string, dict, list: Unmarshaled JSON data.
        """
        return self._json_loads(stream="stderr")

    def stdout_count(self, pattern=None, exclude=False):
        """
        Count number of lines written to stdout.

        Args:
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            int: Count of lines.
        """
        return self._stdout_lines(pattern=pattern, exclude=exclude).__len__()

    def stderr_count(self, pattern=None, exclude=False):
        """
        Count number of lines written to stderr.

        Args:
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            int: Count of lines.
        """
        return self._stderr_lines(pattern=pattern, exclude=exclude).__len__()

    def stdout_skip_lines(
        self, skip_head=0, skip_tail=0, pattern=None, exclude=False
    ):
        """
        Skips some number of lines from the beginning, i.e. the head of the list
        and/or from the end, i.e. the tail of the list of lines from stdout.
        If a pattern results in some subset of original lines, this subset will
        be subject to application of 'skip_head' and/or 'skip_tail'. In other
        words, skipping of lines occurs after application of 'pattern' and
        'exclude' parameters, not before.

        Args:
            skip_head (int, optional): Number of lines to skip relative to beginning of data. Defaults to 0.
            skip_tail (int, optional): Number of lines to skip relative to the end of the data. Defaults to 0.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines written to stdout.
        """
        if skip_head < 0:
            raise ValueError("skip_head cannot be less than 0")
        if skip_tail < 0:
            raise ValueError("skip_tail cannot be less than 0")
        lines = self._stdout_lines(pattern=pattern, exclude=exclude)
        return lines[skip_head: len(lines) - skip_tail]

    def stderr_skip_lines(
        self, skip_head=0, skip_tail=0, pattern=None, exclude=False
    ):
        """
        Skips some number of lines from the beginning, i.e. the head of the list
        and/or from the end, i.e. the tail of the list of lines from stderr.
        If a pattern results in some subset of original lines, this subset will
        be subject to application of 'skip_head' and/or 'skip_tail'. In other
        words, skipping of lines occurs after application of 'pattern' and
        'exclude' parameters, not before.

        Args:
            skip_head (int, optional): Number of lines to skip relative to beginning of data. Defaults to 0.
            skip_tail (int, optional): Number of lines to skip relative to the end of the data. Defaults to 0.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines written to stderr.
        """
        if skip_head < 0:
            raise ValueError("skip_head cannot be less than 0")
        if skip_tail < 0:
            raise ValueError("skip_tail cannot be less than 0")
        lines = self._stderr_lines(pattern=pattern, exclude=exclude)
        return lines[skip_head: len(lines) - skip_tail]

    def stdout_to_tuple_func(self, tuple_func, pattern=None, exclude=False):
        """
        Applies 'tuple_func' to each line from stdout, adding resulting tuple
        to list. It is expected that result from 'tuple_func' is a single tuple
        object.

        Args:
            tuple_func (str): Conversion function from string to N-element tuple.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list(tuple): List of tuples for each line over which 'tuple_func'
            was applied.
        """
        return self._to_tuple_func(tuple_func, pattern, exclude)

    def stderr_to_tuple_func(self, tuple_func, pattern=None, exclude=False):
        """
        Applies 'tuple_func' to each line from stderr, adding resulting tuple
        to list. It is expected that result from 'tuple_func' is a single tuple
        object.

        Args:
            tuple_func (str): Conversion function from string to N-element tuple.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list(tuple): List of tuples for each line over which 'tuple_func' was applied.
        """
        return self._to_tuple_func(
            tuple_func, pattern, exclude, stream="stderr"
        )

    def stdout_to_dict_func(self, tuple_func, pattern=None, exclude=False):
        """
        Applies 'tuple_func' to each line from stdout, adding resulting tuple
        to dict. It is expected that result from 'tuple_func' is a single
        two-element tuple object, where first element becomes dict key and
        second value for given key.

        Args:
            tuple_func (str): Conversion function from string to two-element tuple.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            dict: Dict made from tuples for each line over which 'tuple_func'
            was applied.
        """
        return self._to_dict_func(tuple_func, pattern, exclude)

    def stderr_to_dict_func(self, tuple_func, pattern=None, exclude=False):
        """
        Applies 'tuple_func' to each line from stdout, adding resulting tuple
        to dict. It is expected that result from 'tuple_func' is a single
        two-element tuple object, where first element becomes dict key and
        second value for given key.

        Args:
            tuple_func (str): Conversion function from string to two-element tuple.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            dict: Dict made from tuples for each line over which 'tuple_func'
            was applied.
        """
        return self._to_dict_func(
            tuple_func, pattern, exclude, stream="stderr"
        )

    def stdout_dict_from_line(
        self, keys=None, sep=None, pattern=None, exclude=False
    ):
        """
        Converts stdout lines into dicts, where 'keys' is a list of keys which 
        should be zip(able) with contents of split line. This means that the
        following expression should be true: len(keys) == len(line.split(sep))
        for each line. If len(line) > len(keys), only len(keys) elements are
        taken from each split line. Reverse of this is true also. This is done
        so that equal number of key=value pairs was available for establishing
        a mapping.
        If keys == None, then after a line is split, it is zipped with a range
        object generated from length of split line. In other words, if
        len(line) == 3, resulting dict is {0: line[0], 1: line[1], 2: line[2]}.

        Args:
            keys (hashable, optional): A list of keys to build a dict from line. Defaults to None.
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of dictionaries generated from lines.
        """
        return self._dict_from_line(keys, sep, pattern, exclude)

    def stderr_dict_from_line(
        self, keys=None, sep=None, pattern=None, exclude=False
    ):
        """
        Converts stderr lines into dicts, where 'keys' is a list of keys which 
        should be zip(able) with contents of split line. This means that the
        following expression should be true: len(keys) == len(line.split(sep))
        for each line. If len(line) > len(keys), only len(keys) elements are
        taken from each split line. Reverse of this is true also. This is done
        so that equal number of key=value pairs was available for establishing
        a mapping.
        If keys == None, then after a line is split, it is zipped with a range
        object generated from length of split line. In other words, if
        len(line) == 3, resulting dict is {0: line[0], 1: line[1], 2: line[2]}.

        Args:
            keys (hashable, optional): A list of keys to build a dict from line. Defaults to None.
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of dictionaries generated from lines.
        """
        return self._dict_from_line(
            keys, sep, pattern, exclude, stream="stderr"
        )

    def stdout_firstn(self, n=1, pattern=None, exclude=None):
        """
        Select first n lines from stdout.

        Args:
            n (int, optional): Number of lines to select. Defaults to 1.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines 0 through n.
        """
        return self._first_last_n(n, pattern, exclude)

    def stderr_firstn(self, n=1, pattern=None, exclude=None):
        """
        Select first n lines from stderr.

        Args:
            n (int, optional): Number of lines to select. Defaults to 1.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines 0 through n.
        """
        return self._first_last_n(n, pattern, exclude, stream="stderr")

    def stdout_lastn(self, n=1, pattern=None, exclude=None):
        """
        Select last n lines from stdout.

        Args:
            n (int, optional): Number of lines to select. Defaults to 1.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines len(lines) - n through len(lines).
        """
        return self._first_last_n(n, pattern, exclude, first=False)

    def stderr_lastn(self, n=1, pattern=None, exclude=None):
        """
        Select last n lines from stderr.

        Args:
            n (int, optional): Number of lines to select. Defaults to 1.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines len(lines) - n through len(lines).
        """
        return self._first_last_n(
            n, pattern, exclude, first=False, stream="stderr"
        )

    def stdout_head(self, sep=None, pattern=None, exclude=False):
        """
        Select first column of each line from stdout, after splitting on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of first element of each split line.
        """
        return self._head(sep, pattern, exclude)

    def stderr_head(self, sep=None, pattern=None, exclude=False):
        """
        Select first column of each line from stderr, after splitting on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of first element of each split line.
        """
        return self._head(sep, pattern, exclude, stream="stderr")

    def stdout_tail(self, sep=None, pattern=None, exclude=False):
        """
        Select all but first column of each line from stdout, after splitting on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples with all but first element of each split line.
        """
        return self._tail(sep, pattern, exclude)

    def stderr_tail(self, sep=None, pattern=None, exclude=False):
        """
        Select all but first column of each line from stderr, after splitting on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples with all but first element of each split line.
        """
        return self._tail(sep, pattern, exclude, stream="stderr")

    def stdout_columns(self, sep=None, pattern=None, exclude=False):
        """
        Split each line from stdout into columns and join each column into a
        tuple. This is meant to be used with text where multiple lines contain
        same number of fields (columns), and result of this is a list of tuples
        where each tuple contains elements from a given position across all
        lines. Given a string: 'alpha beta gamma\\ndelta epsilon zeta\\n', this
        produces: [('alpha', 'delta'), ('beta', 'epsilon'), ('gamma', 'zeta')].

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples from each split line.
        """
        return self._columns(sep, pattern, exclude)

    def stderr_columns(self, sep=None, pattern=None, exclude=False):
        """
        Split each line from stderr into columns and join each column into a
        tuple. This is meant to be used with text where multiple lines contain
        same number of fields (columns), and result of this is a list of tuples
        where each tuple contains elements from a given position across all
        lines. Given a string: 'alpha beta gamma\\ndelta epsilon zeta\\n', this
        produces: [('alpha', 'delta'), ('beta', 'epsilon'), ('gamma', 'zeta')].

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples from each split line.
        """
        return self._columns(sep, pattern, exclude, stream="stderr")

    def stdout_take_column(
        self, sep=None, column=0, pattern=None, exclude=False
    ):
        """
        Select a single column of each line from stdout, after splitting the
        line on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            column (int, optional): Select column matching this index. Defaults to 0.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of elements extracted from each split line.
        """
        return self._take_column(sep, column, pattern, exclude)

    def stderr_take_column(
        self, sep=None, column=0, pattern=None, exclude=False
    ):
        """
        Select a single column from each line from stderr, after splitting the
        line on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            column (int, optional): [description]. Defaults to 0.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of elements extracted, one from each split line.
        """
        return self._take_column(
            sep, column, pattern, exclude, stream="stderr"
        )

    def stdout_take_some_columns(
        self, sep=None, selectors=(), pattern=None, exclude=False
    ):
        """
        Select multiple columns from each line from stdout, after splitting the
        line on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            selectors (tuple, optional): Sequence of column indexes. Defaults to ().
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples, where each tuple contains one or more columns from each split line.
        """
        return self._take_some_columns(sep, selectors, pattern, exclude)

    def stderr_take_some_columns(
        self, sep=None, selectors=(), pattern=None, exclude=False
    ):
        """
        Select multiple columns from each line from stderr, after splitting the
        line on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            selectors (tuple, optional): Sequence of column indexes. Defaults to ().
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples, where each tuple contains one or more columns from each split line.
        """
        return self._take_some_columns(
            sep, selectors, pattern, exclude, stream="stderr"
        )

    def stdout_take_range_columns(
        self, sep=None, slc_range=(0, 1, 1), pattern=None, exclude=False
    ):
        """
        Select multiple columns within the 'slc_range' range from each line
        from stdout, after splitting the line on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            slc_range (tuple, optional): Range (start, end, stride). Defaults to (0, 1, 1).
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples, where each tuple contains one or more columns from each split line.
        """
        return self._take_range_columns(sep, slc_range, pattern, exclude)

    def stderr_take_range_columns(
        self, sep=None, slc_range=(0, 1, 1), pattern=None, exclude=False
    ):
        """
        Select multiple columns within the 'slc_range' range from each line
        from stderr, after splitting the line on 'sep'.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            slc_range (tuple, optional): Range (start, end, stride). Defaults to (0, 1, 1).
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples, where each tuple contains one or more columns from each split line.
        """
        return self._take_range_columns(
            sep, slc_range, pattern, exclude, stream="stderr"
        )

    def stdout_line_tuples(
        self,
        sep=None,
        pattern=None,
        exclude=False,
        strip_punct=False,
        strip_chars=PCHARS,
    ):
        """
        Split lines written to stdout into tuples on 'sep', where each line is
        a tuple consisting of all split tokens from that line.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.
            strip_punct (bool, optional): Enable punctuation stripping. Defaults to False.
            strip_chars (str, optional): Characters to strip if 'strip_punct' is True. Defaults to PCHARS.

        Returns:
            list: List of tuples, where each tuple contains columns from each split line.
        """
        return self._line_tuples(
            sep, pattern, exclude, strip_punct, strip_chars
        )

    def stderr_line_tuples(
        self,
        sep=None,
        pattern=None,
        exclude=False,
        strip_punct=False,
        strip_chars=PCHARS,
    ):
        """
        Split lines written to stdout into tuples on 'sep', where each line is
        a tuple consisting of all split tokens from that line.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.
            strip_punct (bool, optional): Enable punctuation stripping. Defaults to False.
            strip_chars (str, optional): Characters to strip if 'strip_punct' is True. Defaults to PCHARS.

        Returns:
            list: List of tuples, where each tuple contains columns from each split line.
        """
        return self._line_tuples(
            sep, pattern, exclude, strip_punct, strip_chars, stream="stderr"
        )

    @property
    def stdout_lines(self):
        """
        Unfiltered lines written to stdout.

        Returns:
            list: List of lines written to stdout.
        """
        return self._stdout_lines()

    @property
    def stderr_lines(self):
        """
        Unfiltered lines written to stderr.

        Returns:
            list: List of lines written to stderr.
        """
        return self._stderr_lines()

    def stdout_trim_prefix(self, prefix, pattern=None, exclude=False):
        """
        Trim substring in 'prefix' from beginning of each line from stdout,
        assuming substring is present.

        Args:
            prefix (str): Prefix to trim from beginning of each line.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines with prefix trimmed from each.
        """
        return self._trim_prefix(prefix, pattern, exclude)

    def stderr_trim_prefix(self, prefix, pattern=None, exclude=False):
        """
        Trim substring in 'prefix' from beginning of each line from stderr,
        assuming substring is present.

        Args:
            prefix (str): Prefix to trim from beginning of each line.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines with prefix trimmed from each.
        """
        return self._trim_prefix(prefix, pattern, exclude, stream="stderr")

    def stdout_trim_suffix(self, suffix, pattern=None, exclude=False):
        """
        Trim substring in 'suffix' from end of each line from stdout,
        assuming substring is present.

        Args:
            suffix (str): Suffix to trim from end of each line.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines with suffix trimmed from each.
        """
        return self._trim_suffix(suffix, pattern, exclude)

    def stderr_trim_suffix(self, suffix, pattern=None, exclude=False):
        """
        Trim substring in 'suffix' from end of each line from stderr,
        assuming substring is present.

        Args:
            suffix (str): Suffix to trim from end of each line.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines with suffix trimmed from each.
        """
        return self._trim_suffix(suffix, pattern, exclude, stream="stderr")

    def stdout_with_prefix(self, prefix, pattern=None, exclude=False):
        """
        Limits included lines from stdout to those matching given prefix.
        If a pattern results in some subset of original lines, this subset
        will be subject to application of 'prefix'. In other words, lines with
        'prefix' may be excluded as a result of pattern matching, because
        prefix checking occurs after application of 'pattern' and 'exclude'
        parameters, not before.

        Args:
            prefix (str): Lines with given prefix should be included.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: Lines matching given prefix.
        """
        return self._with_prefix(prefix, pattern, exclude)

    def stderr_with_prefix(self, prefix, pattern=None, exclude=False):
        """
        Limits included lines from stderr to those matching given prefix.
        If a pattern results in some subset of original lines, this subset
        will be subject to application of 'prefix'. In other words, lines with
        'prefix' may be excluded as a result of pattern matching, because
        prefix checking occurs after application of 'pattern' and 'exclude'
        parameters, not before.

        Args:
            prefix (str): Lines with given prefix should be included.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: Lines matching given prefix.
        """
        return self._with_prefix(prefix, pattern, exclude, stream="stderr")

    def stdout_with_suffix(self, suffix, pattern=None, exclude=False):
        """
        Limits included lines from stdout to those matching given suffix.
        If a pattern results in some subset of original lines, this subset
        will be subject to application of 'suffix'. In other words, lines with
        'suffix' may be excluded as a result of pattern matching, because
        suffix checking occurs after application of 'pattern' and 'exclude'
        parameters, not before.

        Args:
            suffix (str): Lines with given prefix should be included.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: Lines matching given suffix.
        """
        return self._with_suffix(suffix, pattern, exclude)

    def stderr_with_suffix(self, suffix, pattern=None, exclude=False):
        """
        Limits included lines from stderr to those matching given suffix.
        If a pattern results in some subset of original lines, this subset
        will be subject to application of 'suffix'. In other words, lines with
        'suffix' may be excluded as a result of pattern matching, because
        suffix checking occurs after application of 'pattern' and 'exclude'
        parameters, not before.

        Args:
            suffix (str): Lines with given prefix should be included.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: Lines matching given suffix.
        """
        return self._with_suffix(suffix, pattern, exclude, stream="stderr")

    def stdout_at_least_n_substr(self, substr=None, n=0):
        return self._at_least_n_substr(substr, n)

    def stderr_at_least_n_substr(self, substr=None, n=0):
        return self._at_least_n_substr(substr, n, stream="stderr")

    def stdout_at_most_n_substr(self, substr=None, n=0):
        return self._at_most_n_substr(substr, n)

    def stderr_at_most_n_substr(self, substr=None, n=0):
        return self._at_most_n_substr(substr, n, stream="stderr")

    def stdout_filter_func(self, func, exclude=False):
        """
        Filters lines written to stdout with a filtering function in
        'func' argument. This function should expect a single string argument
        which will be a line and return a boolean. Any lines that cause this
        function to return `True` will be included in the resulting list, and
        those that result in `False` will be excluded, unless 'exclude' is
        `True`, which inverts this logic.

        Args:
            func ((s: str) -> bool): Filtering function emitting a boolean.
            exclude (bool, optional): Invert filtering logic. Defaults to False.
        Returns:
            list: List of lines after filtering function is applied.
        """
        return self._filter_func(func, exclude)

    def stderr_filter_func(self, func, exclude=False):
        """
        Filters lines written to stderr with a filtering function in
        'func' argument. This function should expect a single string argument
        which will be a line and return a boolean. Any lines that cause this
        function to return `True` will be included in the resulting list, and
        those that result in `False` will be excluded, unless 'exclude' is
        `True`, which inverts this logic.

        Args:
            func ((s: str) -> bool): Filtering function emitting a boolean.
            exclude (bool, optional): Invert filtering logic. Defaults to False.
        Returns:
            list: List of lines after filtering function is applied.
        """
        return self._filter_func(func, exclude, stream="stderr")

    def stdout_map_func(self, func, pattern=None, exclude=False):
        """
        Applies function in 'func' to each line written to stdout.
        Transformations from these map operations will be included in
        the resulting list. Result of calling 'func' should not be None.

        Args:
            func ((s: str) -> Any): Mapping function receiving a string and emitting Any other type.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of results from application of mapping function.
        """
        return self._map_func(func, pattern=pattern, exclude=exclude)

    def stderr_map_func(self, func, pattern=None, exclude=None):
        """
        Applies function in 'func' to each line written to stderr.
        Transformations from these map operations will be included in
        the resulting list. Result of calling 'func' should not be None.

        Args:
            func ((s: str) -> Any): Mapping function receiving a string and emitting Any other type.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of results from application of mapping function.
        """
        return self._map_func(
            func, pattern=pattern, exclude=exclude, stream="stderr"
        )

    def stdout_funcs_pipeline(self, *funcs):
        """
        Applies functions in a given order over each line written to stdout.
        This function is meant to emulate a unix pipeline, where information
        is piped through multiple programs and possibly mutated throughout the
        pipeline. Each function passed in is assumed to have a single argument
        which will be a single line. Each function is also expected to return
        a string, which may or may not be a mutated version of information
        passed into the function, and the result from the function call is
        passed into next function in the sequence until there are no more
        functions to apply over the data.

        Sementically, this is similar to doing the following for each line:
        x = "some value"
        x = func_a(x)
        x = func_b(x)
        x = func_c(x)
        ... where 'x' is one line in input.

        Args:
            *funcs (Sequence[Callable[(s: str) -> string]]): A sequence of functions, each receiving a string and emitting a string.

        Returns:
            list: List of results from application of sequence of callables.
        """
        return self._funcs_pipeline(funcs)

    def stderr_funcs_pipeline(self, *funcs):
        """
        Applies functions in a given order over each line written to stderr.
        This function is meant to emulate a unix pipeline, where information
        is piped through multiple programs and possibly mutated throughout the
        pipeline. Each function passed in is assumed to have a single argument
        which will be a single line. Each function is also expected to return
        a string, which may or may not be a mutated version of information
        passed into the function, and the result from the function call is
        passed into next function in the sequence until there are no more
        functions to apply over the data.

        Sementically, this is similar to doing the following for each line:
        x = "some value"
        x = func_a(x)
        x = func_b(x)
        x = func_c(x)
        ... where 'x' is one line in input.

        Args:
            *funcs (Sequence[Callable[(s: str) -> string]]): A sequence of functions, each receiving a string and emitting a string.

        Returns:
            list: List of results from application of sequence of callables.
        """
        return self._funcs_pipeline(funcs, stream="stderr")

    ### End String Processing Public Methods ###

    @property
    def std_out(self):
        return self.subprocess.stdout

    @property
    def ok(self):
        return self.return_code == 0

    @property
    def _pexpect_out(self):
        if self.subprocess.encoding:
            result = ""
        else:
            result = b""

        if self.subprocess.before:
            result += self.subprocess.before

        if self.subprocess.after and self.subprocess.after is not pexpect.EOF:
            result += self.subprocess.after

        result += self.subprocess.read()
        return result

    @property
    def out(self):
        """Std/out output (cached)"""
        if self.__out:
            return self.__out

        if self._uses_subprocess:
            if not self.std_out.closed:
                self.__out = self.std_out.read()
                self.std_out.close()
        else:
            self.__out = self._pexpect_out

        return self.__out

    @property
    def std_err(self):
        return self.subprocess.stderr

    @property
    def err(self):
        """Std/err output (cached)"""
        if self.__err:
            return self.__err

        if self._uses_subprocess:
            if not self.std_err.closed:
                self.__err = self.std_err.read()
                self.std_err.close()
        else:
            self.__err = self._pexpect_out

        return self.__err

    @property
    def pid(self):
        """The process' PID."""
        # Support for pexpect's functionality.
        if hasattr(self.subprocess, "proc"):
            return self.subprocess.proc.pid
        # Standard subprocess method.
        return self.subprocess.pid

    @property
    def is_alive(self):
        """Is the process alive?"""
        return pid_exists(self.pid)

    @property
    def return_code(self):
        # Support for pexpect's functionality.
        if self._uses_pexpect:
            return self.subprocess.exitstatus
        # Standard subprocess method.
        return self.subprocess.returncode

    @property
    def std_in(self):
        return self.subprocess.stdin

    def run(self, block=True, binary=False, cwd=None, env=None, shell=True):
        """Runs the given command, with or without pexpect functionality enabled."""
        self.blocking = block

        # Use subprocess.
        if self.blocking:
            popen_kwargs = self._default_popen_kwargs.copy()
            del popen_kwargs['stdin']
            popen_kwargs['universal_newlines'] = not binary
            if cwd:
                popen_kwargs['cwd'] = cwd
            if env:
                popen_kwargs['env'].update(env)
            if not shell:
                popen_kwargs['shell'] = False
            s = subprocess.Popen(self._popen_args, **popen_kwargs)
        # Otherwise, use pexpect.
        else:
            pexpect_kwargs = self._default_pexpect_kwargs.copy()
            if binary:
                pexpect_kwargs['encoding'] = None
            if cwd:
                pexpect_kwargs['cwd'] = cwd
            if env:
                pexpect_kwargs['env'].update(env)
            # Enable Python subprocesses to work with expect functionality.
            pexpect_kwargs['env']['PYTHONUNBUFFERED'] = "1"
            s = PopenSpawn(self._popen_args, **pexpect_kwargs)
        self.subprocess = s
        self.was_run = True

    def do_shell(self, env=None, shell=True):
        """ Runs the command and blocks (waits) until the command is complete. """
        if not shell and not isinstance(self._popen_args, list):
            raise ExternalProgramException(
                "With 'shell=False' command must be a sequence not a string"
            )
        self.run(env=env, shell=shell)
        self.block()

    def expect(self, pattern, timeout=-1):
        """Waits on the given pattern to appear in std_out"""

        if self.blocking:
            raise RuntimeError(
                "expect can only be used on non-blocking commands."
            )

        try:
            self.subprocess.expect(pattern=pattern, timeout=timeout)
        except pexpect.EOF:
            pass

    def send(self, s, end=os.linesep, signal=False):
        """Sends the given string or signal to std_in."""

        if self.blocking:
            raise RuntimeError(
                "send can only be used on non-blocking commands."
            )

        if not signal:
            if self._uses_subprocess:
                return self.subprocess.communicate(s + end)
            else:
                return self.subprocess.send(s + end)
        else:
            self.subprocess.send_signal(s)

    def terminate(self):
        self.subprocess.terminate()

    def kill(self):
        if self._uses_pexpect:
            self.subprocess.kill(signal.SIGINT)
        else:
            self.subprocess.send_signal(signal.SIGINT)

    def block(self):
        """Blocks until process is complete."""
        if self._uses_subprocess:
            # consume stdout and stderr
            if self.blocking:
                try:
                    stdout, stderr = self.subprocess.communicate(
                        timeout=self.timeout if self.timeout else None
                    )
                    self.__out = stdout
                    self.__err = stderr
                except ValueError:
                    pass  # Don't read from finished subprocesses.
            else:
                self.subprocess.stdin.close()
                self.std_out.close()
                self.std_err.close()
                # self.subprocess.wait(self.timeout if self.timeout else None)
                self.subprocess.wait()
        else:
            self.subprocess.sendeof()
            try:
                self.subprocess.wait()
            finally:
                if self.subprocess.proc.stdout:
                    self.subprocess.proc.stdout.close()

    def poll(self):
        if self._uses_subprocess:
            if self.blocking:
                if self.subprocess.poll() == 0:
                    return True
                return False
            return False
        else:
            raise ExternalProgramException("Do not combine poll() with expect")

    def pipe(self, command, timeout=None, cwd=None):
        """Runs the current command and passes its output to the next
        given process.
        """
        if not timeout:
            timeout = self.timeout

        if not self.was_run:
            self.run(block=False, cwd=cwd)

        data = self.out

        if timeout:
            c = ExternalProgram(command, timeout)
        else:
            c = ExternalProgram(command)

        c.run(block=False, cwd=cwd)
        if data:
            c.send(data)
        c.block()
        return c


def _expand_args(command):
    """Parses command strings and returns a Popen-ready list."""

    # Prepare arguments.
    if isinstance(command, STR_TYPES):
        if sys.version_info[0] == 2:
            splitter = shlex.shlex(command.encode("utf-8"))
        elif sys.version_info[0] == 3:
            splitter = shlex.shlex(command)
        else:
            splitter = shlex.shlex(command.encode("utf-8"))
        splitter.whitespace = "|"
        splitter.whitespace_split = True
        command = []

        while True:
            token = splitter.get_token()
            if token:
                command.append(token)
            else:
                break

        command = list(map(shlex.split, command))

    return command


def chain(command, timeout=None, cwd=None, env=None):
    commands = _expand_args(command)
    data = None

    for command in commands:

        c = run(command, block=False, timeout=timeout, cwd=cwd, env=env)

        if data:
            c.send(data, end="")
            c.subprocess.sendeof()

        data = c.out

    return c


def run(command, block=True, binary=False, timeout=None, cwd=None, env=None):
    c = ExternalProgram(command, timeout=timeout)
    c.run(block=block, binary=binary, cwd=cwd, env=env)

    if block:
        c.block()

    return c
