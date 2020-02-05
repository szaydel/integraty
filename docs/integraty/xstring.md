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
    - [apply_filtered](#apply_filtered)
    - [map_if_possible](#map_if_possible)
    - [stripper](#stripper)

## String

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L58)

```python
class String(str):
    def __init__(string: str):
```

### String().at_least_n_substr

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1226)

```python
def at_least_n_substr(substr=None, n=0):
```

### String().at_most_n_substr

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1229)

```python
def at_most_n_substr(substr=None, n=0):
```

### String().compress

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L892)

```python
def compress(
    sep=None,
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

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `indexes` *tuple, optional* - Sequence of column indexes. Defaults to ().
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### String().count

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L577)

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

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1197)

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

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L823)

```python
def fields(
    sep=None,
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

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples from each split line.

### String().filter_func

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1232)

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
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert filtering logic. Defaults to False.

#### Returns

- `list` - List of lines after filtering function is applied.

### String().filtered_map

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1304)

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
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of filtered results over which mapping function was applied.

### String().firstn

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L702)

```python
def firstn(n=1, pattern=None, exclude=None):
```

Select first n lines from input.

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines 0 through n.

### String().fold_funcs

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1343)

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
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of results from application of sequence of callables.

### String().groupby

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1430)

```python
def groupby(
    column=0,
    sep=None,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

For each line from input, split line on `sep` and treat the substring
with index specified in `column` as the key for grouping lines with
matching key(s). The final product is a dictionary where each key maps
to a list of all lines where this key is a substring with the same index
specified in `column`.

#### Arguments

- `column` *int, optional* - Index of column to perform groupby. Defaults to 0.
- `sep` *str, optional* - Separator character. Defaults to None.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - A dictionary of str -> List[str] with grouped lines.

### String().head

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L733)

```python
def head(
    sep=None,
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
>>> import integraty
>>> s = integraty.xstring.String('123 abc def\n456 ghi jkl\n789 mno pqr\n')
>>> s.head()
['123', '456', '789']
>>> s.head(pattern='123')
['123']
>>> s.head(pattern='123', exclude=True)
['456', '789']

```

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of first element of each split line.

### String().json_loads

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L567)

```python
@property
def json_loads():
```

For JSON data written in input, attempt to convert to native data type.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### String().lastn

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L716)

```python
def lastn(n=1, pattern=None, exclude=None):
```

Select last n lines from input.

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines len(lines) - n through len(lines).

### String().line_tuples

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L969)

```python
def line_tuples(
    sep=None,
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
- `strip_punct` *bool, optional* - Enable punctuation stripping. Defaults to False.
- `strip_chars` *str, optional* - Characters to strip if 'strip_punct' is True. Defaults to PCHARS.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains fields from each split line.

#### See also

- [PCHARS](#pchars)

### String().lines

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1022)

```python
def lines(sub_pattern=None, replacement=None, pattern=None, exclude=False):
```

Lines from supplied string, optionally filtered with regular expression
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

- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines from input.

### String().map_func

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1273)

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
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of results from application of mapping function.

### String().pairs

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1390)

```python
def pairs(
    as_dict=False,
    sep=None,
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
- `sep` *str, optional* - Separator character. Defaults to None.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples of tuples or list of dicts.

### String().skip_lines

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L590)

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

Skips some number of lines from the beginning, i.e. the head of the list
and/or from the end, i.e. the tail of the list of lines from input.
If a pattern results in some subset of original lines, this subset will
be subject to application of 'skip_head' and/or 'skip_tail'. In other
words, skipping of lines occurs after application of `pattern` and
`exclude` parameters, not before. Think about this in terms of `grep`
and [String().head](#stringhead) or [String().tail](#stringtail), as in this example:

```
$ some_command | head -5 | grep 'some string'
```

#### Arguments

- `skip_head` *int, optional* - Number of lines to skip relative to beginning of data. Defaults to 0.
- `skip_tail` *int, optional* - Number of lines to skip relative to the end of the data. Defaults to 0.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines from input with some lines skipped from head and tail.

### String().tail

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L778)

```python
def tail(
    sep=None,
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
>>> import integraty
>>> s = integraty.xstring.String('123 abc def\n456 ghi jkl\n789 mno pqr\n')
>>> s.tail()
[('abc', 'def'), ('ghi', 'jkl'), ('mno', 'pqr')]
>>> s.tail(pattern='mno')
[('mno', 'pqr')]
>>> s.tail(pattern='123', exclude=True)
[('ghi', 'jkl'), ('mno', 'pqr')]

```

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples with all but first element of each split line.

### String().take_column

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L859)

```python
def take_column(
    sep=None,
    column=0,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Select a single column of each line from input, after splitting the
line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `column` *int, optional* - Select column matching this index. Defaults to 0.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of elements extracted from each split line.

### String().take_range_fields

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L936)

```python
def take_range_fields(
    sep=None,
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
- `slc_range` *tuple, optional* - Range (start, end, stride). Defaults to (0, 1, 1).
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### String().to_dict

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L675)

```python
def to_dict(keys=None, sep=None, pattern=None, exclude=False):
```

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

#### Arguments

- `keys` *hashable, optional* - A list of keys to build a dict from line. Defaults to None.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of dictionaries generated from lines.

### String().to_dict_func

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L634)

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
from integraty.xstring import String
>>> s1 = 'beta\nalpha beta\nbeta gamma\nalpha delta beta\nsigma epsilon\n'
>>> s = String(s1)
>>> f1 = lambda l: zip([l.split()[0]], [l.split()[1]])
>>> s.to_dict_func(f1)
[{'alpha': 'beta'}, {'beta': 'gamma'}, {'alpha': 'delta'}, {'sigma': 'epsilon'}]

```

#### Arguments

- `func` *str* - Conversion function from string to two-element tuple.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of dicts made from tuples for each line over which `func`
was applied.

### String().trim_prefix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1061)

```python
def trim_prefix(
    prefix,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Trim substring in `prefix` from beginning of each line from input,
assuming substring is present.

#### Arguments

- `prefix` *str* - Prefix to trim from beginning of each line.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with prefix trimmed from each.

### String().trim_suffix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1091)

```python
def trim_suffix(
    suffix,
    sub_pattern=None,
    replacement=None,
    pattern=None,
    exclude=False,
):
```

Trim substring in `suffix` from end of each line from input,
assuming substring is present.

#### Arguments

- `suffix` *str* - Suffix to trim from end of each line.
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with suffix trimmed from each.

### String().with_prefix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1121)

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
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given prefix.

### String().with_suffix

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L1163)

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
- `sub_pattern` *string, optional* - Substitution regex pattern. Defaults to None.
- `replacement` *string, optional* - Text with which to replace all matches of `sub_pattern`. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given suffix.

## apply_filtered

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L22)

```python
def apply_filtered(
    map_func: Callable[[Any], Any],
    filter_func: Callable[[Any], bool],
    lines: Iterable,
):
```

## map_if_possible

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L28)

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

[[find in source code]](https://github.com/szaydel/integratyintegraty/xstring.py#L15)

```python
def stripper(w, chars):
```
