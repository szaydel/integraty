# -*- coding: utf-8 -*-
import re

from typing import Any, Callable, Dict, Iterable, Iterator, List, TypeVar, Sequence, Sequence


def stripper(w, chars):
    if not chars:
        return w
    return stripper(w.replace(chars[0], ""), chars[1:])


def apply_filtered(map_func: Callable[[Any], Any],
                   filter_func: Callable[[Any], bool], lines: Iterable):
    for line in filter(filter_func, lines):
        yield map_func(line)


def map_if_possible(func: Callable[[Any], Any], source: Iterable) -> Iterator:
    """
    Silently drops any data which causes `func` calls with given data to raise
    any Exception. The intention is to allow messy data to be processed where
    certain data may be incomplete, fields missing, etc. For example, a string
    with newlines is split on `\\n`, and each resulting line is further
    tokenized. If `func` can only be successfully called with a subset of these
    lines, while the other lines would normally cause an exception to be raised,
    we let those exceptional cases fall out, yielding results of calling `func`
    on each item in `source` that does not cause `func` to raise an exception.
    
    Args:
        func (Callable[[Any], Any]): Function being mapped over data in `source`.
        source (Iterable): Sequence of data over which `func` is getting called.
    
    Returns:
        Iterator: All results from applying `func` which were not discarded due to Exception.
    
    Yields:
        Iterator: Function `func` applied over an item from `source`.
    """
    for x in source:
        try:
            yield func(x)
        except Exception as e:  # pylint: disable=unused-variable
            # to debug uncomment this print statement
            # print(e)
            pass


class Map:
    """
    Generic implementation of a Callable class which takes an iterable and for
    each element applies `func` Callable, unless the element was filtered out
    by the `filter` function.
    
    Returns:
        map: An iterable object with filtered elements after filter function.
    """
    __slots__ = ["filter", "func"]

    def __init__(self, filter: Callable[[Any], bool], func: Callable[[Any],
                                                                     Any]):
        self.filter = filter
        self.func = func

    def __call__(self, iterable: Iterable) -> Any:
        # FIXME: I have not yet settled on which approach is better.
        # Alternative approach is commented out for now.
        # for i in iterable:
        #     if self.filter(i):
        #         yield self.func(i)
        return map(self.func, (i for i in iterable if self.filter(i)))


class Split:
    """
    A more comprehensive implementation of a split method. Splits a string
    into tokens, using either default method on a string or, if the `sep`
    argument is multiple characters long, treat it as a regex pattern and use
    `re.split` method instead to do a more sophisticated split operation.
    If the `sep` argument is a callable, it is assumed to be a splitting
    function, and the string argument is instead passed to this function. This
    function must be a Callable[[str], List[str]]. In other words, it takes a
    single argument, a string to split, and it returns a list with zero or
    more tokens after splitting the string. Resulting tokens are filtered to
    eliminate any empty strings.

    Returns:
        list[str]: A list of tokens after splitting a string on `sep`.
    """
    __slots__ = ["_s"]

    def __init__(self, string):
        self._s = string

    def __call__(self, sep=None, maxsplit=-1):
        if isinstance(sep, Callable):
            return [i for i in sep(self._s) if i]
        if not sep or len(sep) == 1:
            return [i for i in self._s.split(sep=sep, maxsplit=maxsplit) if i]
        else:
            pat = re.compile(sep)  # Assumes a regex pattern
            return [
                i for i in re.split(
                    pat, self._s, maxsplit=0 if maxsplit == -1 else maxsplit)
                if i
            ]
