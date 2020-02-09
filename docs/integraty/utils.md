# Utils

> Auto-generated documentation for [integraty.utils](https://github.com/szaydel/integratyintegraty/utils.py) module.

- [integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / [Integraty](index.md#integraty) / Utils
    - [Map](#map)
    - [Split](#split)
    - [apply_filtered](#apply_filtered)
    - [map_if_possible](#map_if_possible)
    - [stripper](#stripper)

## Map

[[find in source code]](https://github.com/szaydel/integratyintegraty/utils.py#L50)

```python
class Map():
    def __init__(filter: Callable[[Any], bool], func: Callable[[Any], Any]):
```

Generic implementation of a Callable class which takes an iterable and for
each element applies `func` Callable, unless the element was filtered out
by the `filter` function.

#### Returns

- `map` - An iterable object with filtered elements after filter function.

## Split

[[find in source code]](https://github.com/szaydel/integratyintegraty/utils.py#L75)

```python
class Split():
    def __init__(string):
```

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

#### Returns

- `list[str]` - A list of tokens after splitting a string on `sep`.

## apply_filtered

[[find in source code]](https://github.com/szaydel/integratyintegraty/utils.py#L14)

```python
def apply_filtered(
    map_func: Callable[[Any], Any],
    filter_func: Callable[[Any], bool],
    lines: Iterable,
):
```

## map_if_possible

[[find in source code]](https://github.com/szaydel/integratyintegraty/utils.py#L20)

```python
def map_if_possible(func: Callable[[Any], Any], source: Iterable) -> Iterator:
```

Silently drops any data which causes `func` calls with given data to raise
any Exception. The intention is to allow messy data to be processed where
certain data may be incomplete, fields missing, etc. For example, a string
with newlines is split on `\n`, and each resulting line is further
tokenized. If `func` can only be successfully called with a subset of these
lines, while the other lines would normally cause an exception to be raised,
we let those exceptional cases fall out, yielding results of calling `func`
on each item in `source` that does not cause `func` to raise an exception.

#### Arguments

func (Callable[[Any], Any]): Function being mapped over data in `source`.
- `source` *Iterable* - Sequence of data over which `func` is getting called.

#### Returns

- `Iterator` - All results from applying `func` which were not discarded due to Exception.

#### Yields

- `Iterator` - Function `func` applied over an item from `source`.

## stripper

[[find in source code]](https://github.com/szaydel/integratyintegraty/utils.py#L7)

```python
def stripper(w, chars):
```
