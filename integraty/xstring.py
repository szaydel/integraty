# -*- coding: utf-8 -*-

import itertools
import json
import re

from functools import reduce
from typing import Callable, Dict, List, TypeVar, Sequence, Sequence

PCHARS = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


def stripper(w, chars):
    if chars:
        return stripper(w.replace(chars[0], ""), chars[1:])
    else:
        return w


class String(str):

    def __init__(self, string: str):
        self._s = string

    def __repr__(self):
        if len(self._s) > 10:
            rep_str = self._s[:10] + "..."
        else:
            rep_str = self._s
        return "String({!r})".format(rep_str)

    ### String Processing Private Methods Below ###

    def _lines_from_impl(self,
                         sub_pattern=None,
                         replacement=None,
                         pattern=None,
                         exclude=False):
        return self._lines(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def _splitlines(self):
        return [l.strip() for l in self._s.splitlines()]

    def _lines(self,
               sub_pattern=None,
               replacement=None,
               pattern=None,
               exclude=False):
        compiled_pattern = None if not sub_pattern else re.compile(sub_pattern)

        def sub_if_necessary(pat, repl, s):
            """ Apply substitution if there's a pattern, otherwise return string untouched."""
            return s if not pat else re.sub(pat, repl, s)

        lines = self._splitlines()
        filtered_lines = None
        if pattern and exclude:
            filtered_lines = [
                sub_if_necessary(compiled_pattern, replacement, l)
                for l in lines if not re.search(pattern, l)
            ]
        elif pattern:
            filtered_lines = [
                sub_if_necessary(compiled_pattern, replacement, l)
                for l in lines if re.search(pattern, l)
            ]
        else:
            filtered_lines = [
                sub_if_necessary(compiled_pattern, replacement, l)
                for l in lines
            ]
        return filtered_lines

    def _line_tuples(
        self,
        sep=None,
        strip_punct=False,
        strip_chars=PCHARS,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        new_lines = []
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

        for l in lines:
            tokens = tuple(l.split(sep))
            if tokens:
                if strip_punct:
                    tokens = tuple(
                        stripper(tok, strip_chars) for tok in tokens)
                new_lines.append(tokens)
        return new_lines

    def _trim_prefix(
        self,
        prefix,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

        return [
            l[len(prefix):].strip() if l.startswith(prefix) else l
            for l in lines
        ]

    def _trim_suffix(
        self,
        suffix,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

        return [
            l[:l.rindex(suffix)].strip() if l.endswith(suffix) else l
            for l in lines
        ]

    def _with_prefix(
        self,
        prefix=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        if not prefix:
            return lines

        return [l for l in lines if l.startswith(prefix)]

    def _with_suffix(
        self,
        suffix=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        if not suffix:
            return lines

        return [l for l in lines if l.endswith(suffix)]

    def _count_substrs(self, substr=None, pattern=None, exclude=False):
        lines = self._lines_from_impl(pattern=pattern, exclude=exclude)
        if not substr:
            return len(lines)
        return sum(1 for line in lines if line.find(substr) >= 0)

    def _with_substr(self, substr=None, exclude=False):
        lines = self._lines_from_impl()
        if not substr:
            return lines
        if exclude:
            return [l for l in lines if l.find(substr) == -1]
        return [l for l in lines if l.find(substr) >= 0]

    def _at_least_n_substr(self, substr=None, n=0):
        lines = self._lines_from_impl()
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) >= n]

    def _at_most_n_substr(self, substr=None, n=0):
        lines = self._lines_from_impl()
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) <= n]

    def _first_last_n(self, n=1, first=True, pattern=None, exclude=False):
        lines = self._lines_from_impl()
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

    def _head(
        self,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

        return [col.split(sep)[0].strip() for col in lines]

    def _tail(
        self,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

        return [tuple(col.split(sep)[1:]) for col in lines]

    def _fields(
        self,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

        return list(
            zip(*map(lambda x: map(lambda x: x.strip(), x.split()), lines)))

    def _take_column(
        self,
        sep=None,
        column=0,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        return [col.split(sep)[column].strip() for col in lines]

    def _compress(
        self,
        sep=None,
        indexes=(),
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        if not indexes or not isinstance(indexes, tuple):
            raise ValueError(
                "Argument 'indexes' must be a tuple with at least one index")
        selectors = tuple(True if i in indexes else False
                          for i in range(0,
                                         max(indexes) + 1))
        return [
            tuple(itertools.compress(col.split(sep), selectors))
            for col in lines
        ]

    def _take_range_fields(
        self,
        sep=None,
        slc_range=(0, 1, 1),
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        slc_obj = slice(*slc_range)

        return [col.split(sep)[slc_obj] for col in lines]

    def _to_dict_func(
        self,
        func,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        return [dict(func(line)) for line in lines if line]

    def _filter_func(
        self,
        func,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        if exclude:
            filtered_lines = [line for line in lines if not func(line)]
        else:
            filtered_lines = [line for line in lines if func(line)]
        return filtered_lines

    def _map_func(
        self,
        func,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        return [func(line) for line in lines]

    def _json_loads(self):
        if not self._s:
            return None
        d = {}
        try:
            d = json.loads(self._s)
        except json.JSONDecodeError:
            return None
        return d

    def _to_dict(self,
                 keys=None,
                 sep=None,
                 sub_pattern=None,
                 replacement=None,
                 pattern=None,
                 exclude=False):
        lines = self._lines_from_impl(sub_pattern=sub_pattern,
                                      replacement=replacement,
                                      pattern=pattern,
                                      exclude=exclude)
        return [
            dict(
                zip(
                    keys
                    if keys else [i for i in range(0, len(line.split(sep)))],
                    line.split(sep),
                )) for line in lines if line
        ]

    def _fold_funcs(
        self,
        funcs,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

        def compose(*functions):

            def compose2(f, g):
                return lambda x: f(g(x))

            return reduce(compose2, functions, lambda x: x)

        composed = compose(*funcs[::-1])
        return [composed(line) for line in lines]

    def _pairs(
        self,
        as_dict=False,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        if as_dict:
            return [
                dict(zip(line.split(sep)[::2],
                         line.split(sep)[1::2])) for line in lines
            ]
        else:
            return [
                tuple(zip(line.split(sep)[::2],
                          line.split(sep)[1::2])) for line in lines
            ]

    def _groupby(
        self,
        column=0,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        lines = self._lines_from_impl(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        d = {}

        def groupby_rec(column: int, sep: Sequence, d: dict, l: List) -> Dict:
            if not l:
                return d
            tokens = l[0].split(sep)
            key = tokens[column % len(tokens)]  # protects from bounds errors
            if key in d:
                d[key].append(l[0])  # key exists, append line to list
            else:
                d[key] = [l[0]]  # new key, create a list with this line
            # recursively call self until list is empty
            return groupby_rec(column, sep, d, l[1:])

        return groupby_rec(column, sep, d, lines)

    ### End String Processing Private Methods ###

    ### String Processing Public Methods Below ###

    @property
    def json_loads(self):
        """
        For JSON data written in input, attempt to convert to native data type.

        Returns:
            bool, int, string, dict, list: Unmarshaled JSON data.
        """
        return self._json_loads()

    def count(self, pattern=None, exclude=False):
        """
        Count number of lines in the supplied string.

        Args:
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            int: Count of lines in input.
        """
        return self._lines(pattern=pattern, exclude=exclude).__len__()

    def skip_lines(
        self,
        skip_head=0,
        skip_tail=0,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Skips some number of lines from the beginning, i.e. the head of the list
        and/or from the end, i.e. the tail of the list of lines from input.
        If a pattern results in some subset of original lines, this subset will
        be subject to application of 'skip_head' and/or 'skip_tail'. In other
        words, skipping of lines occurs after application of `pattern` and
        `exclude` parameters, not before. Think about this in terms of `grep`
        and `head` or `tail`, as in this example:
        ```
        $ some_command | head -5 | grep 'some string'
        ```

        Args:
            skip_head (int, optional): Number of lines to skip relative to beginning of data. Defaults to 0.
            skip_tail (int, optional): Number of lines to skip relative to the end of the data. Defaults to 0.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines from input with some lines skipped from head and tail.
        """
        if skip_head < 0:
            raise ValueError("skip_head cannot be less than 0")
        if skip_tail < 0:
            raise ValueError("skip_tail cannot be less than 0")
        lines = self._lines(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )
        return lines[skip_head:len(lines) - skip_tail]

    def to_dict_func(
        self,
        func,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Applies `func` to each line from input, adding resulting tuple
        to dict. It is expected that result from `func` is a single
        two-element tuple object, where first element becomes dict key and
        second value for given key.

        Args:
            func (str): Conversion function from string to two-element tuple.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            dict: Dict made from tuples for each line over which `func`
            was applied.
        """
        return self._to_dict_func(
            func=func,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def to_dict(self, keys=None, sep=None, pattern=None, exclude=False):
        """
        Converts input lines into dicts, where `keys` is a list of keys which 
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
        return self._to_dict(keys=keys,
                             sep=sep,
                             pattern=pattern,
                             exclude=exclude)

    def firstn(self, n=1, pattern=None, exclude=None):
        """
        Select first n lines from input.

        Args:
            n (int, optional): Number of lines to select. Defaults to 1.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines 0 through n.
        """
        return self._first_last_n(n=n, pattern=pattern, exclude=exclude)

    def lastn(self, n=1, pattern=None, exclude=None):
        """
        Select last n lines from input.

        Args:
            n (int, optional): Number of lines to select. Defaults to 1.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines len(lines) - n through len(lines).
        """
        return self._first_last_n(n=n,
                                  first=False,
                                  pattern=pattern,
                                  exclude=exclude)

    def head(
        self,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Select first column of each line from input, after splitting on `sep`.
        Substitution of all `sub_pattern` matches for `replacement` occurs
        after lines have been filtered based on `pattern`, not before.

        This method is meant to be similar to recursive list iteration in
        functional languages. Where a list is a combination of a _head_, first
        element, and _rest_ or _tail_, which is the remainder of the list.
        ```
        >>> import integraty
        >>> s = integraty.xstring.String('123 abc def\\n456 ghi jkl\\n789 mno pqr\\n') 
        >>> s.head()
        ['123', '456', '789']
        >>> s.head(pattern='123')
        ['123']
        >>> s.head(pattern='123', exclude=True)
        ['456', '789']

        ```
        Args:
            sep (str, optional): Separator character. Defaults to None.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of first element of each split line.
        """
        return self._head(
            sep=sep,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def tail(
        self,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Select all but first column of each line from input, after splitting on 
        `sep`. Substitution of all `sub_pattern` matches for `replacement`
        occurs after lines have been filtered based on `pattern`, not before.

        This method is meant to be similar to recursive list iteration in
        functional languages. Where a list is a combination of a _head_, first
        element, and _rest_ or _tail_, which is the remainder of the list.
        ```
        >>> import integraty
        >>> s = integraty.xstring.String('123 abc def\\n456 ghi jkl\\n789 mno pqr\\n') 
        >>> s.tail()
        [('abc', 'def'), ('ghi', 'jkl'), ('mno', 'pqr')]
        >>> s.tail(pattern='mno')
        [('mno', 'pqr')]
        >>> s.tail(pattern='123', exclude=True)
        [('ghi', 'jkl'), ('mno', 'pqr')]

        ```
        Args:
            sep (str, optional): Separator character. Defaults to None.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples with all but first element of each split line.
        """
        return self._tail(
            sep=sep,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def fields(
        self,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Split each line from input into fields and join each column into a
        tuple. This is meant to be used with text where multiple lines contain
        same number of fields (sub-strings), and result of this is a list of
        tuples where each tuple contains elements from a given position across
        all lines.
        Given a string: 'alpha beta gamma\\ndelta epsilon zeta\\n',
        this produces: [('alpha', 'delta'), ('beta', 'epsilon'), ('gamma', 
        'zeta')].

        Args:
            sep (str, optional): Separator character. Defaults to None.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples from each split line.
        """
        return self._fields(
            sep=sep,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def take_column(
        self,
        sep=None,
        column=0,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Select a single column of each line from input, after splitting the
        line on `sep`.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            column (int, optional): Select column matching this index. Defaults to 0.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of elements extracted from each split line.
        """
        return self._take_column(
            sep=sep,
            column=column,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def compress(
        self,
        sep=None,
        indexes=(),
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Select one or more fields from each line from input, after splitting
        the line on `sep`.
        To make this more concrete let's take this example.
        Given the line: `The quick brown fox jumps over the lazy dog`
        to select words _quick_, _jumps_, _lazy_ and _dog_, indexes field
        would be set to (1, 4, 7, 8).

        Each line of text consists of zero or more substrings. An empty line
        consists of zero substrings and cannot be indexed into. Any line with
        one or more substrings, once split on `sep` is going to have 
        `len(line)-1` positions or indexes if you think of this line as a list
        of tokens. By specifying only certain indexes one can extract
        substrings of interest.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            indexes (tuple, optional): Sequence of column indexes. Defaults to ().
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples, where each tuple contains one or more fields from each split line.
        """
        return self._compress(
            sep=sep,
            indexes=indexes,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def take_range_fields(
        self,
        sep=None,
        slc_range=(0, 1, 1),
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Select multiple fields within the 'slc_range' range from each line
        from input, after splitting the line on `sep`.

        Args:
            sep (str, optional): Separator character. Defaults to None.
            slc_range (tuple, optional): Range (start, end, stride). Defaults to (0, 1, 1).
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples, where each tuple contains one or more fields from each split line.
        """
        return self._take_range_fields(
            sep=sep,
            slc_range=slc_range,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def line_tuples(
        self,
        sep=None,
        strip_punct=False,
        strip_chars=PCHARS,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Split lines in supplied string into tuples with `sep` as optional
        separator, where each line is converted into a N-tuple containing
        all (N) tokens after the split of that line.
        ```
        >>> from integraty.xstring import String
        >>> s = String('# alpha Ω\\n# beta Ω\\n# gamma Ω\\n# delta Δ\\n') 
        >>> s.line_tuples()
        [('#', 'alpha', 'Ω'), ('#', 'beta', 'Ω'), ('#', 'gamma', 'Ω'), ('#', 'delta', 'Δ')]
        >>> s.line_tuples(pattern='ta')
        [('#', 'beta', 'Ω'), ('#', 'delta', 'Δ')]
        >>> s.line_tuples(pattern='ta', exclude=True)
        [('#', 'alpha', 'Ω'), ('#', 'gamma', 'Ω')]

        >>> s = String('alpha Ω,# beta Ω,# gamma Ω,# delta Δ')
        >>> s.lines()
        ['alpha Ω,# beta Ω,# gamma Ω,# delta Δ']
        >>> s.line_tuples(sep=',')
        [('alpha Ω', '# beta Ω', '# gamma Ω', '# delta Δ')]

        ```
        Args:
            sep (str, optional): Separator character. Defaults to None.
            strip_punct (bool, optional): Enable punctuation stripping. Defaults to False.
            strip_chars (str, optional): Characters to strip if 'strip_punct' is True. Defaults to PCHARS.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples, where each tuple contains fields from each split line.
        """
        return self._line_tuples(
            sep=sep,
            strip_punct=strip_punct,
            strip_chars=strip_chars,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def lines(self,
              sub_pattern=None,
              replacement=None,
              pattern=None,
              exclude=False):
        """
        Lines from supplied string, optionally filtered with regular expression
        in `pattern`.
        ```
        >>> from integraty.xstring import String
        >>> s = String('2020-01-02 alpha Ω\\n2020-01-02 beta Ω\\n2020-02-01 gamma Ω\\n2020-02-03 delta Δ\\n')
        >>> s.lines(sub_pattern=r'\\d{4}-\\d{2}-\\d{2} ', replacement='')
        ['alpha Ω', 'beta Ω', 'gamma Ω', 'delta Δ']
        >>> s.lines(sub_pattern=r'^\\S+ ', replacement='')
        ['alpha Ω', 'beta Ω', 'gamma Ω', 'delta Δ']
        >>> s.lines(sub_pattern=r'^\\S+', replacement='*'*5)
        ['***** alpha Ω', '***** beta Ω', '***** gamma Ω', '***** delta Δ']
        >>> s.lines(sub_pattern=r'^\\S+', replacement='*'*5, pattern='ha')
        ['***** alpha Ω']
        >>> s.lines(sub_pattern=r'^\\S+', replacement='*'*5, pattern='ha', exclude=True)
        ['***** beta Ω', '***** gamma Ω', '***** delta Δ']

        ```
        Args:
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.
        
        Returns:
            list: List of lines from input.
        """
        return self._lines(
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def trim_prefix(
        self,
        prefix,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Trim substring in `prefix` from beginning of each line from input,
        assuming substring is present.

        Args:
            prefix (str): Prefix to trim from beginning of each line.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines with prefix trimmed from each.
        """
        return self._trim_prefix(
            prefix=prefix,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def trim_suffix(
        self,
        suffix,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Trim substring in `suffix` from end of each line from input,
        assuming substring is present.

        Args:
            suffix (str): Suffix to trim from end of each line.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of lines with suffix trimmed from each.
        """
        return self._trim_suffix(
            suffix=suffix,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def with_prefix(
        self,
        prefix,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Limits included lines from input to those matching given prefix.
        If a pattern results in some subset of original lines, this subset
        will be subject to application of `prefix`. In other words, lines with
        `prefix` may be excluded as a result of pattern matching, because
        prefix checking occurs after application of `pattern` and `exclude`
        parameters, not before.
        ```
        >>> from integraty.xstring import String
        >>> s = String('# alpha Ω\\n# beta Ω\\n# gamma Ω\\n# delta Δ\\n')
        >>> s.with_prefix('#')
        ['# alpha Ω', '# beta Ω', '# gamma Ω', '# delta Δ']
        >>> s.with_prefix(prefix='%', sub_pattern='#', replacement='%')  
        ['% alpha Ω', '% beta Ω', '% gamma Ω', '% delta Δ']

        ```
        Args:
            prefix (str): Lines with given prefix should be included.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: Lines matching given prefix.
        """
        return self._with_prefix(
            prefix=prefix,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def with_suffix(
        self,
        suffix,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Limits included lines from input to those matching given suffix.
        If a pattern results in some subset of original lines, this subset
        will be subject to application of `suffix`. In other words, lines with
        `suffix` may be excluded as a result of pattern matching, because
        suffix checking occurs after application of `pattern` and `exclude`
        parameters, not before.

        Args:
            suffix (str): Lines with given prefix should be included.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: Lines matching given suffix.
        """
        return self._with_suffix(
            suffix=suffix,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def count_substrs(self, substr=None, pattern=None, exclude=False):
        """
        Counts lines in supplied string where at least one match for substring
        given in `substr` is found. This is a count of matching lines, not a
        total count of substrings, which could be greater if any given line
        contains more than a single matching substring.
        ```
        >>> from integraty.xstring import String
        >>> s = String('alpha Ω\\nbeta Ω\\ngamma Ω\\ndelta Δ\\n')
        >>> s.count_substrs(substr='Ω')
        3
        >>> s.count_substrs(substr='Ω', pattern='alpha', exclude=True)
        2
        >>> s.count_substrs(substr='Ω', pattern='alpha')
        1

        ```
        Args:
            substr (str, optional): Substring to find in each line. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            int: Count of lines with at least one substring match.
        """
        return self._count_substrs(substr=substr,
                                   pattern=pattern,
                                   exclude=exclude)

    def at_least_n_substr(self, substr=None, n=0):
        return self._at_least_n_substr(substr, n)

    def at_most_n_substr(self, substr=None, n=0):
        return self._at_most_n_substr(substr, n)

    def filter_func(
        self,
        func,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Filters lines from supplied string with a filtering function in
        `func` argument. This function should expect a single string argument
        which will be a line and return a boolean. Any lines that cause this
        function to return `True` will be included in the resulting list, and
        those that result in `False` will be excluded, unless `exclude` is
        `True`, which inverts this logic.
        ```
        from integraty.xstring import String
        >>> s = String('alpha beta gamma\\ndelta epsilon zeta\\n')
        >>> s.filter_func(lambda x: 'zeta' in x.split())
        ['delta epsilon zeta']
        >>> s.filter_func(lambda x: 'zeta' in x.split(), exclude=True) 
        ['alpha beta gamma']

        ```
        Args:
            func ((s: str) -> bool): Filtering function emitting a boolean.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert filtering logic. Defaults to False.
        Returns:
            list: List of lines after filtering function is applied.
        """
        return self._filter_func(
            func=func,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def map_func(
        self,
        func,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Applies function in 'func' to each line written in input.
        Transformations from these map operations will be included in
        the resulting list. Result of calling 'func' should not be None.

        Args:
            func ((s: str) -> Any): Mapping function receiving a string and emitting Any other type.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of results from application of mapping function.
        """
        return self._map_func(
            func=func,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def fold_funcs(
        self,
        *funcs,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=None,
    ):
        """
        Higher-order function taking one or more functions composing them
        together, then applying the composed function over each line from
        input.
        This method is meant to emulate a unix pipeline, where information
        is piped through multiple programs and possibly mutated throughout the
        pipeline. Each function passed in is assumed to have a single argument.
        First function in the chain will receive a single complete line, but
        every other function will receive output of previous function.

        Assuming there are three functions that must be applied to each line
        and these functions are called `a`, `b`, and `c`, where `a` is the
        first function, `b` second, and `c` last, the sequence as a pipeline
        looks like this: `line |> a |> b |> c`, or in mathematical terms it
        looks like this:
        ```
        a(line)
        b(a(line))
        c(b(a(line)))
        ```

        Args:
            *funcs (Sequence[Callable[(s: str) -> string]]): A sequence of functions, each with a single argument, returning a single value.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of results from application of sequence of callables.
        """
        return self._fold_funcs(
            funcs,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def pairs(
        self,
        as_dict=False,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        Break-up each line from input into pairs, optionally placing these
        pairs into dicts, with one dict per line. Pairs are effectively
        adjacent strings. To make this more clear, given this line:
        `name abc path /var/log/abc.log`, result is a tuple of 2-tuples:
        `(('name', 'abc'), ('path', '/var/log/abc.log'))`, and converted to
        dict it becomes: {'name': 'abc', 'path': '/var/log/abc.log'}.

        If a line contains odd number of tokens after being split, last token
        in the split line will be discarded.

        Args:
            as_dict (bool, optional): Should pairs be inserted into a dict. Defaults to False.
            sep (str, optional): Separator character. Defaults to None.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            list: List of tuples of tuples or list of dicts.
        """
        return self._pairs(
            as_dict=as_dict,
            sep=sep,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    def groupby(
        self,
        column=0,
        sep=None,
        sub_pattern=None,
        replacement=None,
        pattern=None,
        exclude=False,
    ):
        """
        For each line from input, split line on `sep` and treat the substring
        with index specified in `column` as the key for grouping lines with
        matching key(s). The final product is a dictionary where each key maps
        to a list of all lines where this key is a substring with the same index
        specified in `column`.

        Args:
            column (int, optional): Index of column to perform groupby. Defaults to 0.
            sep (str, optional): Separator character. Defaults to None.
            sub_pattern (string, optional): Substitution regex pattern. Defaults to None.
            replacement (string, optional): Text with which to replace all matches of `sub_pattern`. Defaults to None.
            pattern (str, optional): Select lines matching pattern. Defaults to None.
            exclude (bool, optional): Invert pattern matching. Defaults to False.

        Returns:
            dict: A dictionary of str -> List[str] with grouped lines.
        """
        return self._groupby(
            column=column,
            sep=sep,
            sub_pattern=sub_pattern,
            replacement=replacement,
            pattern=pattern,
            exclude=exclude,
        )

    ### End String Processing Public Methods ###
