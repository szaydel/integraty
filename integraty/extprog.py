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
        return "ExternalProgram({!r}, timeout={})".format(self.cmd, self.timeout)

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
        return {"env": os.environ.copy(), "encoding": encoding, "timeout": self.timeout}

    @property
    def _uses_subprocess(self):
        return isinstance(self.subprocess, subprocess.Popen)

    @property
    def _uses_pexpect(self):
        return isinstance(self.subprocess, PopenSpawn)

    ### String Processing Private Methods Below ###

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
            raise InvalidStream

    def _stdout_lines(self):
        return self._splitlines()

    def _stderr_lines(self):
        return self._splitlines(stream="stderr")

    def _list_of_lines(self, strip_punct=False, strip_chars=PCHARS, stream="stdout"):
        if not self.was_run:
            raise ExternalProgramException(
                "Run program to obtain results before requesting resulting data"
            )
        lines = []
        if stream == "stdout":
            for l in self.out.split("\n"):
                tokens = l.split()
                if tokens:
                    if strip_punct:
                        tokens = tuple(stripper(tok, strip_chars) for tok in tokens)
                    lines.append(tokens)
        elif stream == "stderr":
            for l in self.err.split("\n"):
                tokens = l.split()
                if tokens:
                    if strip_punct:
                        tokens = [stripper(tok, strip_chars) for tok in tokens]
                    lines.append(tokens)
        else:
            raise InvalidStream
        return lines

    def _trim_prefix(self, prefix, pattern=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            unfiltered_lines = [l for l in lines]
            return [
                l[len(prefix) :] if l.startswith(prefix) else l
                for l in unfiltered_lines
            ]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [l[len(prefix) :] if l.startswith(prefix) else l for l in filtered_lines]

    def _trim_suffix(self, suffix, pattern=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            unfiltered_lines = [l for l in lines]
            return [
                l[len(suffix) :] if l.endswith(suffix) else l for l in unfiltered_lines
            ]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [l[len(suffix) :] if l.endswith(suffix) else l for l in filtered_lines]

    def _with_prefix(self, prefix, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not prefix:
            return lines
        if exclude:
            return [l for l in lines if not l.startswith(prefix)]
        return [l for l in lines if l.startswith(prefix)]

    def _with_suffix(self, suffix=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not suffix:
            return lines
        if exclude:
            return [l for l in lines if not l.endswith(suffix)]
        return [l for l in lines if l.endswith(suffix)]

    def _with_substr(self, substr=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not substr:
            return lines
        if exclude:
            return [l for l in lines if l.find(substr) == -1]
        return [l for l in lines if l.find(substr) >= 0]

    def _at_least_n_substr(self, substr=None, n=0, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) >= n]

    def _at_most_n_substr(self, substr=None, n=0, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) <= n]

    def _first_last_n(
        self, n=1, pattern=None, exclude=False, first=True, stream="stdout"
    ):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
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
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            return [col.split(sep)[0].strip() for col in lines]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [col.split(sep)[0].strip() for col in filtered_lines]

    def _tail(self, sep=None, pattern=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            return [tuple(col.split(sep)[1:]) for col in lines]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [tuple(col.split(sep)[1:]) for col in filtered_lines]

    def _take_column(
        self, sep=None, column=0, pattern=None, exclude=False, stream="stdout"
    ):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            return [col.split(sep)[column].strip() for col in lines]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [col.split(sep)[column].strip() for col in filtered_lines]

    def _take_some_columns(
        self, sep=None, selectors=(), pattern=None, exclude=False, stream="stdout",
    ):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            return [
                tuple(itertools.compress(col.split(sep), selectors)) for col in lines
            ]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [
            tuple(itertools.compress(col.split(sep), selectors))
            for col in filtered_lines
        ]

    def _take_range_columns(
        self,
        sep=None,
        slc_range=(0, 1, 1),
        pattern=None,
        exclude=False,
        stream="stdout",
    ):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        slc_obj = slice(*slc_range)
        if not pattern:
            return [col.split(sep)[slc_obj] for col in lines]
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return [col.split(sep)[slc_obj] for col in filtered_lines]

    def _dict_transform_func(
        self, func, sep=None, pattern=None, exclude=False, stream="stdout",
    ):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            return dict(func(line) for line in lines)
        if exclude:
            filtered_lines = [l for l in lines if not re.search(pattern, l)]
        else:
            filtered_lines = [l for l in lines if re.search(pattern, l)]
        return dict(func(line) for line in filtered_lines)

    def _filter_func(self, func, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        return [line for line in lines if func(line)]

    def _map_func(self, func, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        return [func(line) for line in lines]

    def _json_loads(self, stream="stdout"):
        if stream == "stdout":
            json_string = self.out
        elif stream == "stderr":
            json_string = self.err
        else:
            raise InvalidStream
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
        if stream == "stdout":
            lines = self._stdout_lines()
        elif stream == "stderr":
            lines = self._stderr_lines()
        else:
            raise InvalidStream
        if not pattern:
            return [
                dict(
                    zip(
                        keys if keys else [i for i in range(0, len(col.split(sep)))],
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
                    keys if keys else [i for i in range(0, len(col.split(sep)))],
                    col.split(sep),
                )
            )
            for col in filtered_lines
        ]

    ### End String Processing Private Methods ###

    ### String Processing Public Methods Below ###

    @property
    def stdout_json_loads(self):
        return self._json_loads()

    @property
    def stderr_json_loads(self):
        return self._json_loads(stream="stderr")

    def stdout_count(self, pattern=None, exclude=False):
        lines = self._stdout_lines()
        if not pattern:
            return lines.__len__()
        if exclude:
            return [l for l in lines if not re.search(pattern, l)].__len__()
        return [l for l in lines if re.search(pattern, l)].__len__()

    def stderr_count(self, pattern=None, exclude=False):
        lines = self._stderr_lines()
        if not pattern:
            return lines.__len__()
        if exclude:
            return [l for l in lines if not re.search(pattern, l)].__len__()
        return [l for l in lines if re.search(pattern, l)].__len__()

    def stdout_lines(self, pattern=None, exclude=False):
        lines = self._stdout_lines()
        if not pattern:
            return lines
        if exclude:
            return [l for l in lines if not re.search(pattern, l)]
        return [l for l in lines if re.search(pattern, l)]

    def stderr_lines(self, pattern=None, exclude=False):
        lines = self._stderr_lines()
        if not pattern:
            return lines
        if exclude:
            return [l for l in lines if not re.search(pattern, l)]
        return [l for l in lines if re.search(pattern, l)]

    def stdout_dict_transform_func(self, func, sep=None, pattern=None, exclude=False):
        return self._dict_transform_func(func, sep, pattern, exclude)

    def stderr_dict_transform_func(self, func, sep=None, pattern=None, exclude=False):
        return self._dict_transform_func(func, sep, pattern, exclude, stream="stderr")

    def stdout_dict_from_line(self, keys=None, sep=None, pattern=None, exclude=False):
        return self._dict_from_line(keys, sep, pattern, exclude)

    def stderr_dict_from_line(self, keys=None, sep=None, pattern=None, exclude=False):
        return self._dict_from_line(keys, sep, pattern, exclude, stream="stderr")

    def stdout_firstn(self, n=1, pattern=None, exclude=None):
        return self._first_last_n(n, pattern, exclude)

    def stderr_firstn(self, n=1, pattern=None, exclude=None):
        return self._first_last_n(n, pattern, exclude, stream="stderr")

    def stdout_lastn(self, n=1, pattern=None, exclude=None):
        return self._first_last_n(n, pattern, exclude, first=False)

    def stderr_lastn(self, n=1, pattern=None, exclude=None):
        return self._first_last_n(n, pattern, exclude, first=False, stream="stderr")

    def stdout_head(self, sep=None, pattern=None, exclude=False):
        return self._head(sep, pattern, exclude)

    def stderr_head(self, sep=None, pattern=None, exclude=False):
        return self._head(sep, pattern, exclude, stream="stderr")

    def stdout_tail(self, sep=None, pattern=None, exclude=False):
        return self._tail(sep, pattern, exclude)

    def stderr_tail(self, sep=None, pattern=None, exclude=False):
        return self._tail(sep, pattern, exclude, stream="stderr")

    def stdout_take_column(self, sep=None, column=0, pattern=None, exclude=False):
        return self._take_column(sep, column, pattern, exclude)

    def stderr_take_column(self, sep=None, column=0, pattern=None, exclude=False):
        return self._take_column(sep, column, pattern, exclude, stream="stderr")

    def stdout_take_some_columns(
        self, sep=None, selectors=(), pattern=None, exclude=False
    ):
        return self._take_some_columns(sep, selectors, pattern, exclude)

    def stderr_take_some_columns(
        self, sep=None, selectors=(), pattern=None, exclude=False
    ):
        return self._take_some_columns(
            sep, selectors, pattern, exclude, stream="stderr"
        )

    def stdout_take_range_columns(
        self, sep=None, slc_range=(0, 1, 1), pattern=None, exclude=False
    ):
        return self._take_range_columns(sep, slc_range, pattern, exclude)

    def stderr_take_range_columns(
        self, sep=None, slc_range=(0, 1, 1), pattern=None, exclude=False
    ):
        return self._take_range_columns(
            sep, slc_range, pattern, exclude, stream="stderr"
        )

    def stdout_line_tuples(self, strip_punct=False, strip_chars=PCHARS):
        return self._list_of_lines(strip_punct, strip_chars, stream="stdout")

    def stderr_line_tuples(self, strip_punct=False, strip_chars=PCHARS):
        return self._list_of_lines(strip_punct, strip_chars, stream="stderr")

    @property
    def stdout_splitlines(self):
        return self._splitlines()

    @property
    def stderr_splitlines(self):
        return self._splitlines(stream="stderr")

    def stdout_trim_prefix(self, prefix, pattern=None, exclude=False):
        return self._trim_prefix(prefix, pattern, exclude)

    def stderr_trim_prefix(self, prefix, pattern=None, exclude=False):
        return self._trim_prefix(prefix, pattern, exclude, stream="stderr")

    # FIXME: Add trim_suffix

    def stdout_with_prefix(self, prefix, exclude=False):
        return self._with_prefix(prefix, exclude)

    def stderr_with_prefix(self, prefix, exclude=False):
        return self._with_prefix(prefix, exclude, stream="stderr")

    def stdout_with_suffix(self, suffix=None, exclude=False):
        return self._with_suffix(suffix, exclude)

    def stderr_with_suffix(self, suffix=None, exclude=False):
        return self._with_suffix(suffix, exclude, stream="stderr")

    def stdout_at_least_n_substr(self, substr=None, n=0):
        return self._at_least_n_substr(substr, n)

    def stderr_at_least_n_substr(self, substr=None, n=0):
        return self._at_least_n_substr(substr, n, stream="stderr")

    def stdout_at_most_n_substr(self, substr=None, n=0):
        return self._at_most_n_substr(substr, n)

    def stderr_at_most_n_substr(self, substr=None, n=0):
        return self._at_most_n_substr(substr, n, stream="stderr")

    def stdout_filter_func(self, func):
        return self._filter_func(func)

    def stderr_filter_func(self, func):
        return self._filter_func(func)

    def stdout_map_func(self, func):
        return self._map_func(func)

    def stderr_map_func(self, func):
        return self._map_func(func)

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
            del popen_kwargs["stdin"]
            popen_kwargs["universal_newlines"] = not binary
            if cwd:
                popen_kwargs["cwd"] = cwd
            if env:
                popen_kwargs["env"].update(env)
            if not shell:
                popen_kwargs["shell"] = False
            s = subprocess.Popen(self._popen_args, **popen_kwargs)
        # Otherwise, use pexpect.
        else:
            pexpect_kwargs = self._default_pexpect_kwargs.copy()
            if binary:
                pexpect_kwargs["encoding"] = None
            if cwd:
                pexpect_kwargs["cwd"] = cwd
            if env:
                pexpect_kwargs["env"].update(env)
            # Enable Python subprocesses to work with expect functionality.
            pexpect_kwargs["env"]["PYTHONUNBUFFERED"] = "1"
            s = PopenSpawn(self._popen_args, **pexpect_kwargs)
        self.subprocess = s
        self.was_run = True

    def run_wait(self, env=None, shell=True):
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
            raise RuntimeError("expect can only be used on non-blocking commands.")

        try:
            self.subprocess.expect(pattern=pattern, timeout=timeout)
        except pexpect.EOF:
            pass

    def send(self, s, end=os.linesep, signal=False):
        """Sends the given string or signal to std_in."""

        if self.blocking:
            raise RuntimeError("send can only be used on non-blocking commands.")

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
