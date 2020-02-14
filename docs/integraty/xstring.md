# Xstring

> Auto-generated documentation for [integraty.xstring](https://github.com/szaydel/integratyintegraty/xstring.py) module.

- [integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / [Integraty](index.md#integraty) / Xstring
    - [String](#string)
        - [String().at_least_n_substr](#stringat_least_n_substr)
        - [String().at_most_n_substr](#stringat_most_n_substr)
        - [String().compress](#stringcompress)
        - [String().count](#stringcount)
        - [String().count_substrs](#stringcount_substrs)
        - [String().fields](#stringfields)
        - [String().filter_func](#stringfilter_func)
        - [String().filtered_map](#stringfiltered_map)
        - [String().firstn](#stringfirstn)
        - [String().fold_funcs](#stringfold_funcs)
        - [String().groupby](#stringgroupby)
        - [String().groupby_count](#stringgroupby_count)
        - [String().head](#stringhead)
        - [String().json_loads](#stringjson_loads)
        - [String().lastn](#stringlastn)
        - [String().line_tuples](#stringline_tuples)
        - [String().lines](#stringlines)
        - [String().map_func](#stringmap_func)
        - [String().pairs](#stringpairs)
        - [String().skip_lines](#stringskip_lines)
        - [String().tail](#stringtail)
        - [String().take_column](#stringtake_column)
        - [String().take_range_fields](#stringtake_range_fields)
        - [String().to_dict](#stringto_dict)
        - [String().to_dict_func](#stringto_dict_func)
        - [String().trim_prefix](#stringtrim_prefix)
        - [String().trim_suffix](#stringtrim_suffix)
        - [String().with_prefix](#stringwith_prefix)
        - [String().with_suffix](#stringwith_suffix)

## String

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L18)

```python
class String(str):
    def __init__(string: str):
```

### String().at_least_n_substr

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1329)

```python
def at_least_n_substr(substr=None, n=0):
```

### String().at_most_n_substr

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1332)

```python
def at_most_n_substr(substr=None, n=0):
```

### String().compress

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L981)

```python
def compress(
    sep=None,
    maxsplit=-1,
    indexes=(),
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

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

```
>>> from integraty.xstring import String
>>> s1 = String('a b c d\ne f g h h i j k\nl m n o\n')
>>> s1.compress(indexes=(0,3))
[('a', 'd'), ('e', 'h'), ('l', 'o')]
>>> s1.compress(indexes=(0,2,3))
[('a', 'c', 'd'), ('e', 'g', 'h'), ('l', 'n', 'o')]

```

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `indexes` *tuple, optional* - Sequence of column indexes. Defaults to ().
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### String().count

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L584)

```python
def count(pattern=None, exclude=False):
```

Count number of lines in the supplied string.

#### Arguments

- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `int` - Count of lines in input.

### String().count_substrs

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1300)

```python
def count_substrs(substr=None, pattern=None, exclude=False):
```

Counts lines in supplied string where at least one match for substring
given in `substr` is found. This is a count of matching lines, not a
total count of substrings, which could be greater if any given line
contains more than a single matching substring.

```
>>> from integraty.xstring import String
>>> s = String('alpha Ω\nbeta Ω\ngamma Ω\ndelta Δ\n')
>>> s.count_substrs(substr='Ω')
3
>>> s.count_substrs(substr='Ω', pattern='alpha', exclude=True)
2
>>> s.count_substrs(substr='Ω', pattern='alpha')
1

```

#### Arguments

- `substr` *str, optional* - Substring to find in each line. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `int` - Count of lines with at least one substring match.

### String().fields

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L892)

```python
def fields(
    sep=None,
    maxsplit=-1,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Split each line from input into fields and join each column into a
tuple. This is meant to be used with text where multiple lines contain
same number of fields (sub-strings), and result of this is a list of
tuples where each tuple contains elements from a given position across
all lines.
Given a string: 'alpha beta gamma\ndelta epsilon zeta\n',
this produces: [('alpha', 'delta'), ('beta', 'epsilon'), ('gamma',
'zeta')].

```
>>> from integraty.xstring import String
>>> s1 = String('alpha beta gamma\ndelta epsilon zeta\n')
>>> s1.fields()
[('alpha', 'delta'), ('beta', 'epsilon'), ('gamma', 'zeta')]

```

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples from each split line.

### String().filter_func

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1335)

```python
def filter_func(
    func,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Filters lines from supplied string with a filtering function in
`func` argument. This function should expect a single string argument
which will be a line and return a boolean. Any lines that cause this
function to return `True` will be included in the resulting list, and
those that result in `False` will be excluded, unless `exclude` is
`True`, which inverts this logic.

```
from integraty.xstring import String
>>> s = String('alpha beta gamma\ndelta epsilon zeta\n')
>>> s.filter_func(lambda x: 'zeta' in x.split())
['delta epsilon zeta']
>>> s.filter_func(lambda x: 'zeta' in x.split(), exclude=True)
['alpha beta gamma']

```

#### Arguments

- `func` *((s* - str) -> bool): Filtering function emitting a boolean.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert filtering logic. Defaults to False.

#### Returns

- `list` - List of lines after filtering function is applied.

### String().filtered_map

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1407)

```python
def filtered_map(
    map_func,
    filter_func,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Higher-order function taking a mapping function and a filtering
function.
For every line for which [String().filter_func](#stringfilter_func) returns `True`, [String().map_func](#stringmap_func) is
applied over it, producing subset of transformed lines. Filtering and
mapping occur after optional substitution and selection or excludion
of lines matching a pattern. This method is meant to give user much
more control over how to select lines and what to do with them, before
having them returned as a list.

#### Arguments

map_func (Callable[[Any], Any]): Function to apply over given lines.
filter_func (Callable[[Any], bool]): Function to select lines.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of filtered results over which mapping function was applied.

### String().firstn

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L735)

```python
def firstn(
    n=1,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=None,
):
```

Select first n lines from input.

```
>>> from integraty.xstring import String
>>> s1 = String("first line\nsecond line\nthird line\nfourth line\nfifth line\n")
>>> s1.firstn(3)
['first line', 'second line', 'third line']

```

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines 0 through n.

### String().fold_funcs

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1446)

```python
def fold_funcs(
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=None,
    *funcs,
):
```

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

#### Arguments

- `*funcs` *(Sequence[Callable[(s* - str) -> string]]): A sequence of functions, each with a single argument, returning a single value.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of results from application of sequence of callables.

### String().groupby

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1535)

```python
def groupby(
    key_func,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

A groupby function, which for each line based on the key function in
`key_func` adds the line to an already existing group, or creates and
adds it to a new group if the derived key is first seen. The final
product is a dictionary where each key maps to a list of one or more
lines.

#### Arguments

key_func (Callable[[str], Any]): For each line generate a key to establish a group to which the line will be added.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - A dictionary of str -> List[str] with grouped lines.

### String().groupby_count

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1568)

```python
def groupby_count(
    key_func,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

A groupby histogram function, which for each line based on the key
function in `key_func` increments count of an existing group or adds a
new group to collection of groups. The intent of this function is to
give a flexible mechanism for group results without keeping all the
lines, and instead just a histogram of the data. This is most useful
when we know for example that we expect at least X number of items in
a particular group.

#### Arguments

key_func (Callable[[str], Any]): For each line generate a key to establish a group to which the line will be added.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - A dictionary of Any -> int with count for each distinct group.

### String().head

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L798)

```python
def head(
    sep=None,
    maxsplit=-1,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Select first column of each line from input, after splitting on `sep`.
Substitution of all `sub_pattern` matches for `replacement` occurs
after lines have been filtered based on `pattern`, not before.

This method is meant to be similar to recursive list iteration in
functional languages. Where a list is a combination of a _head_, first
element, and _rest_ or _tail_, which is the remainder of the list.

```
>>> from integraty.xstring import String
>>> s1 = String('123 abc def\n456 ghi jkl\n789 mno pqr\n')
>>> s1.head()
['123', '456', '789']
>>> s1.head(pattern='123')
['123']
>>> s1.head(pattern='123', exclude=True)
['456', '789']

```

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of first element of each split line.

### String().json_loads

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L574)

```python
@property
def json_loads():
```

For JSON data written in input, attempt to convert to native data type.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### String().lastn

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L766)

```python
def lastn(
    n=1,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=None,
):
```

Select last n lines from input.

```
>>> from integraty.xstring import String
>>> s1 = String("first line\nsecond line\nthird line\nfourth line\nfifth line\n")
>>> s1.lastn(3)
['third line', 'fourth line', 'fifth line']

```

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines len(lines) - n through len(lines).

### String().line_tuples

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1070)

```python
def line_tuples(
    sep=None,
    maxsplit=-1,
    strip_punct=False,
    strip_chars=PCHARS,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Split lines in supplied string into tuples with `sep` as optional
separator, where each line is converted into a N-tuple containing
all (N) tokens after the split of that line.

```
>>> from integraty.xstring import String
>>> s = String('# alpha Ω\n# beta Ω\n# gamma Ω\n# delta Δ\n')
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

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `strip_punct` *bool, optional* - Enable punctuation stripping. Defaults to False.
- `strip_chars` *str, optional* - Characters to strip if 'strip_punct' is True. Defaults to PCHARS.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains fields from each split line.

#### See also

- [PCHARS](#pchars)

### String().lines

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1125)

```python
def lines(sub_pattern=None, replacement=None, pattern=None, exclude=False):
```

Lines from supplied str, optionally filtered with regular expression
in `pattern`.

```
>>> from integraty.xstring import String
>>> s = String('2020-01-02 alpha Ω\n2020-01-02 beta Ω\n2020-02-01 gamma Ω\n2020-02-03 delta Δ\n')
>>> s.lines(sub_pattern=r'\d{4}-\d{2}-\d{2} ', replacement='')
['alpha Ω', 'beta Ω', 'gamma Ω', 'delta Δ']
>>> s.lines(sub_pattern=r'^\S+ ', replacement='')
['alpha Ω', 'beta Ω', 'gamma Ω', 'delta Δ']
>>> s.lines(sub_pattern=r'^\S+', replacement='*'*5)
['***** alpha Ω', '***** beta Ω', '***** gamma Ω', '***** delta Δ']
>>> s.lines(sub_pattern=r'^\S+', replacement='*'*5, pattern='ha')
['***** alpha Ω']
>>> s.lines(sub_pattern=r'^\S+', replacement='*'*5, pattern='ha', exclude=True)
['***** beta Ω', '***** gamma Ω', '***** delta Δ']

```

#### Arguments

- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines from input.

### String().map_func

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1376)

```python
def map_func(
    func,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Applies function in 'func' to each line written in input.
Transformations from these map operations will be included in
the resulting list. Result of calling 'func' should not be None.

#### Arguments

- `func` *((s* - str) -> Any): Mapping function receiving a string and emitting Any other type.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of results from application of mapping function.

### String().pairs

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1493)

```python
def pairs(
    as_dict=False,
    sep=None,
    maxsplit=-1,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Break-up each line from input into pairs, optionally placing these
pairs into dicts, with one dict per line. Pairs are effectively
adjacent strings. To make this more clear, given this line:
`name abc path /var/log/abc.log`, result is a tuple of 2-tuples:
`(('name', 'abc'), ('path', '/var/log/abc.log'))`, and converted to
dict it becomes: {'name': 'abc', 'path': '/var/log/abc.log'}.

If a line contains odd number of tokens after being split, last token
in the split line will be discarded.

#### Arguments

- `as_dict` *bool, optional* - Should pairs be inserted into a dict. Defaults to False.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `sep` *str, optional* - Separator character. Defaults to None.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples of tuples or list of dicts.

### String().skip_lines

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L597)

```python
def skip_lines(
    skip_head=0,
    skip_tail=0,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Skips some number of lines from the beginning, i.e. the head of the
list of lines, and/or from the end, i.e. the tail of the list of lines
from input. If a pattern results in some subset of original lines,
this subset will be subject to application of 'skip_head' and/or
'skip_tail'. In other words, skipping of lines occurs after application
of `pattern` and `exclude` parameters, not before. Think about this in
terms of `grep` and [String().head](#stringhead) or [String().tail](#stringtail), as in this example:
`$ some_command | head -5 | grep 'some string'`

```
>>> from integraty.xstring import String
>>> s1 = String('first line\nsecond line\nthird line\nfourth line\nfifth line\n')
>>> s1.skip_lines(skip_head=2)
['third line', 'fourth line', 'fifth line']
>>> s1.skip_lines(skip_tail=2)
['first line', 'second line', 'third line']
>>> s1.skip_lines(skip_head=1, skip_tail=1)
['second line', 'third line', 'fourth line']
>>> s1.skip_lines(skip_head=1, skip_tail=1, pattern='third', exclude=True)
['second line', 'fourth line']

```

#### Arguments

- `skip_head` *int, optional* - Number of lines to skip relative to beginning of data. Defaults to 0.
- `skip_tail` *int, optional* - Number of lines to skip relative to the end of the data. Defaults to 0.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines from input with some lines skipped from head and tail.

### String().tail

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L845)

```python
def tail(
    sep=None,
    maxsplit=-1,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Select all but first column of each line from input, after splitting on
`sep`. Substitution of all `sub_pattern` matches for `replacement`
occurs after lines have been filtered based on `pattern`, not before.

This method is meant to be similar to recursive list iteration in
functional languages. Where a list is a combination of a _head_, first
element, and _rest_ or _tail_, which is the remainder of the list.

```
>>> from integraty.xstring import String
>>> s = String('123 abc def\n456 ghi jkl\n789 mno pqr\n')
>>> s.tail()
[('abc', 'def'), ('ghi', 'jkl'), ('mno', 'pqr')]
>>> s.tail(pattern='mno')
[('mno', 'pqr')]
>>> s.tail(pattern='123', exclude=True)
[('ghi', 'jkl'), ('mno', 'pqr')]

```

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples with all but first element of each split line.

### String().take_column

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L936)

```python
def take_column(
    sep=None,
    maxsplit=-1,
    column=0,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Take a single column out of each line from input, after splitting the
line on `sep`.

```
>>> from integraty.xstring import String
>>> s1 = String('a b c d\ne f g h h i j k\nl m n o\n')
>>> s1.take_column(column=0)
['a', 'e', 'l']
>>> s1.take_column(column=1)
['b', 'f', 'm']
>>> s1.take_column(column=2)
['c', 'g', 'n']

```

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `column` *int, optional* - Select column matching this index. Defaults to 0.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of elements extracted from each split line.

### String().take_range_fields

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1035)

```python
def take_range_fields(
    sep=None,
    maxsplit=-1,
    slc_range=(0, 1, 1),
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Select multiple fields within the 'slc_range' range from each line
from input, after splitting the line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `slc_range` *tuple, optional* - Range (start, end, stride). Defaults to (0, 1, 1).
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### String().to_dict

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L692)

```python
def to_dict(keys=None, sep=None, maxsplit=-1, pattern=None, exclude=False):
```

Converts input lines into dicts, where `keys` is a list of keys which
should be zip(able) with contents of split line. This means that the
following expression should be true: len(keys) == len(Split(line)(sep=sep, maxsplit=maxsplit))
for each line. If len(line) > len(keys), only len(keys) elements are
taken from each split line. Reverse of this is true also. This is done
so that equal number of _key=value_ pairs was available for establishing
a mapping.
If keys == None, then after a line is split, it is zipped with a range
object generated from length of split line. In other words, if
len(line) == 3, resulting dict is {0: line[0], 1: line[1], 2: line[2]}.

```
>>> from integraty.xstring import String
>>> s1 = String('first line\nsecond line\nthird line\nfourth line\nfifth line\n')
>>> s1.to_dict(keys=('key', 'value'))
[{'key': 'first', 'value': 'line'}, {'key': 'second', 'value': 'line'}, {'key': 'third', 'value': 'line'}, {'key': 'fourth', 'value': 'line'}, {'key': 'fifth', 'value': 'line'}]
>>> s1.to_dict(keys=('key', 'value'), pattern='(first|second)')
[{'key': 'first', 'value': 'line'}, {'key': 'second', 'value': 'line'}]
>>> s1.to_dict()
[{0: 'first', 1: 'line'}, {0: 'second', 1: 'line'}, {0: 'third', 1: 'line'}, {0: 'fourth', 1: 'line'}, {0: 'fifth', 1: 'line'}]

```

#### Arguments

- `keys` *Sequence, optional* - A list of keys to build a dict from line. Defaults to None.
- `maxsplit` *int, optional* - Split line at most this many times. Defaults to `-1`, no limit.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of dictionaries generated from lines.

### String().to_dict_func

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L652)

```python
def to_dict_func(
    func,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Applies `func` to each line from input, adding resulting tuple
to dict. It is expected that result from `func` is a single
two-element tuple object, where first element becomes dict key and
second value for given key.

```
>>> from integraty.xstring import String
>>> s1 = String('beta\nalpha beta\nbeta gamma\nalpha delta beta\nsigma epsilon\n')
>>> f1 = lambda l: zip([l.split()[0]], [l.split()[1]])
>>> s1.to_dict_func(f1)
[{'alpha': 'beta'}, {'beta': 'gamma'}, {'alpha': 'delta'}, {'sigma': 'epsilon'}]

```

#### Arguments

- `func` *str* - Conversion function from string to two-element tuple.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of dicts made from tuples for each line over which `func`
was applied.

### String().trim_prefix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1164)

```python
def trim_prefix(
    prefix,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Trim substring in `prefix` from beginning of each line of input, after
splitting, assuming substring is present.

#### Arguments

- `prefix` *str* - Prefix to trim from beginning of each line.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with prefix trimmed from each.

### String().trim_suffix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1194)

```python
def trim_suffix(
    suffix,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Trim substring in `suffix` from beginning of each line of input, after
splitting, assuming substring is present.

#### Arguments

- `suffix` *str* - Suffix to trim from end of each line.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with suffix trimmed from each.

### String().with_prefix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1224)

```python
def with_prefix(
    prefix,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Limits included lines from input to those matching given prefix.
If a pattern results in some subset of original lines, this subset
will be subject to application of `prefix`. In other words, lines with
`prefix` may be excluded as a result of pattern matching, because
prefix checking occurs after application of `pattern` and `exclude`
parameters, not before.

```
>>> from integraty.xstring import String
>>> s = String('# alpha Ω\n# beta Ω\n# gamma Ω\n# delta Δ\n')
>>> s.with_prefix('#')
['# alpha Ω', '# beta Ω', '# gamma Ω', '# delta Δ']
>>> s.with_prefix(prefix='%', sub_pattern='#', replacement='%')
['% alpha Ω', '% beta Ω', '% gamma Ω', '% delta Δ']

```

#### Arguments

- `prefix` *str* - Lines with given prefix should be included.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given prefix.

### String().with_suffix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1266)

```python
def with_suffix(
    suffix,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Limits included lines from input to those matching given suffix.
If a pattern results in some subset of original lines, this subset
will be subject to application of `suffix`. In other words, lines with
`suffix` may be excluded as a result of pattern matching, because
suffix checking occurs after application of `pattern` and `exclude`
parameters, not before.

#### Arguments

- `suffix` *str* - Lines with given prefix should be included.
- `sub_pattern` *str, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *str, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given suffix.
