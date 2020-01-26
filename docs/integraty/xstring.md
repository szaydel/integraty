# Xstring

> Auto-generated documentation for [integraty.xstring](../../integraty/xstring.py) module.

- [Integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / `Integraty` / Xstring
    - [String](#string)
        - [String().at_least_n_substr](#stringat_least_n_substr)
        - [String().at_most_n_substr](#stringat_most_n_substr)
        - [String().compress](#stringcompress)
        - [String().count](#stringcount)
        - [String().dict_from_line](#stringdict_from_line)
        - [String().fields](#stringfields)
        - [String().filter_func](#stringfilter_func)
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
        - [String().to_dict_func](#stringto_dict_func)
        - [String().trim_prefix](#stringtrim_prefix)
        - [String().trim_suffix](#stringtrim_suffix)
        - [String().with_prefix](#stringwith_prefix)
        - [String().with_suffix](#stringwith_suffix)
    - [stripper](#stripper)

## String

[[find in source code]](../../integraty/xstring.py#L20)

```python
class String():
    def __init__(string: str):
```

### String().at_least_n_substr

[[find in source code]](../../integraty/xstring.py#L649)

```python
def at_least_n_substr(substr=None, n=0):
```

### String().at_most_n_substr

[[find in source code]](../../integraty/xstring.py#L652)

```python
def at_most_n_substr(substr=None, n=0):
```

### String().compress

[[find in source code]](../../integraty/xstring.py#L500)

```python
def compress(sep=None, indexes=(), pattern=None, exclude=False):
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
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### String().count

[[find in source code]](../../integraty/xstring.py#L325)

```python
def count(pattern=None, exclude=False):
```

Count number of lines written in input.

#### Arguments

- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `int` - Count of lines.

### String().dict_from_line

[[find in source code]](../../integraty/xstring.py#L383)

```python
def dict_from_line(keys=None, sep=None, pattern=None, exclude=False):
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

### String().fields

[[find in source code]](../../integraty/xstring.py#L463)

```python
def fields(sep=None, pattern=None, exclude=False):
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
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples from each split line.

### String().filter_func

[[find in source code]](../../integraty/xstring.py#L655)

```python
def filter_func(func, exclude=False):
```

Filters lines written in input with a filtering function in
'func' argument. This function should expect a single string argument
which will be a line and return a boolean. Any lines that cause this
function to return `True` will be included in the resulting list, and
those that result in `False` will be excluded, unless `exclude` is
`True`, which inverts this logic.

#### Arguments

- `func` *((s* - str) -> bool): Filtering function emitting a boolean.
- `exclude` *bool, optional* - Invert filtering logic. Defaults to False.

#### Returns

- `list` - List of lines after filtering function is applied.

### String().firstn

[[find in source code]](../../integraty/xstring.py#L407)

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

[[find in source code]](../../integraty/xstring.py#L688)

```python
def fold_funcs(pattern=None, exclude=None, *funcs):
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

#### Returns

- `list` - List of results from application of sequence of callables.

### String().groupby

[[find in source code]](../../integraty/xstring.py#L741)

```python
def groupby(column=0, sep=None, pattern=None, exclude=False):
```

For each line from input, split line on `sep` and treat the substring
with index specified in `column` as the key for grouping lines with
matching key(s). The final product is a dictionary where each key maps
to a list of all lines where this key is a substring with the same index
specified in `column`.

#### Arguments

- `column` *int, optional* - Index of column to perform groupby. Defaults to 0.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - A dictionary of str -> List[str] with grouped lines.

### String().head

[[find in source code]](../../integraty/xstring.py#L435)

```python
def head(sep=None, pattern=None, exclude=False):
```

Select first column of each line from input, after splitting on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of first element of each split line.

### String().json_loads

[[find in source code]](../../integraty/xstring.py#L315)

```python
@property
def json_loads():
```

For JSON data written in input, attempt to convert to native data type.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### String().lastn

[[find in source code]](../../integraty/xstring.py#L421)

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

[[find in source code]](../../integraty/xstring.py#L545)

```python
def line_tuples(
    sep=None,
    pattern=None,
    exclude=False,
    strip_punct=False,
    strip_chars=PCHARS,
):
```

Split lines written in input into tuples on `sep`, where each line is
a tuple consisting of all split tokens from that line.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.
- `strip_punct` *bool, optional* - Enable punctuation stripping. Defaults to False.
- `strip_chars` *str, optional* - Characters to strip if 'strip_punct' is True. Defaults to PCHARS.

#### Returns

- `list` - List of tuples, where each tuple contains fields from each split line.

#### See also

- [PCHARS](#pchars)

### String().lines

[[find in source code]](../../integraty/xstring.py#L571)

```python
@property
def lines():
```

Unfiltered lines written in input.

#### Returns

- `list` - List of lines written in input.

### String().map_func

[[find in source code]](../../integraty/xstring.py#L672)

```python
def map_func(func, pattern=None, exclude=False):
```

Applies function in 'func' to each line written in input.
Transformations from these map operations will be included in
the resulting list. Result of calling 'func' should not be None.

#### Arguments

- `func` *((s* - str) -> Any): Mapping function receiving a string and emitting Any other type.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of results from application of mapping function.

### String().pairs

[[find in source code]](../../integraty/xstring.py#L718)

```python
def pairs(as_dict=False, sep=None, pattern=None, exclude=False):
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
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples of tuples or list of dicts.

### String().skip_lines

[[find in source code]](../../integraty/xstring.py#L338)

```python
def skip_lines(skip_head=0, skip_tail=0, pattern=None, exclude=False):
```

Skips some number of lines from the beginning, i.e. the head of the list
and/or from the end, i.e. the tail of the list of lines from input.
If a pattern results in some subset of original lines, this subset will
be subject to application of 'skip_head' and/or 'skip_tail'. In other
words, skipping of lines occurs after application of `pattern` and
`exclude` parameters, not before.

#### Arguments

- `skip_head` *int, optional* - Number of lines to skip relative to beginning of data. Defaults to 0.
- `skip_tail` *int, optional* - Number of lines to skip relative to the end of the data. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines written in input.

### String().tail

[[find in source code]](../../integraty/xstring.py#L449)

```python
def tail(sep=None, pattern=None, exclude=False):
```

Select all but first column of each line from input, after splitting on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples with all but first element of each split line.

### String().take_column

[[find in source code]](../../integraty/xstring.py#L484)

```python
def take_column(sep=None, column=0, pattern=None, exclude=False):
```

Select a single column of each line from input, after splitting the
line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `column` *int, optional* - Select column matching this index. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of elements extracted from each split line.

### String().take_range_fields

[[find in source code]](../../integraty/xstring.py#L527)

```python
def take_range_fields(
    sep=None,
    slc_range=(0, 1, 1),
    pattern=None,
    exclude=False,
):
```

Select multiple fields within the 'slc_range' range from each line
from input, after splitting the line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `slc_range` *tuple, optional* - Range (start, end, stride). Defaults to (0, 1, 1).
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### String().to_dict_func

[[find in source code]](../../integraty/xstring.py#L365)

```python
def to_dict_func(tuple_func, pattern=None, exclude=False):
```

Applies `tuple_func` to each line from input, adding resulting tuple
to dict. It is expected that result from `tuple_func` is a single
two-element tuple object, where first element becomes dict key and
second value for given key.

#### Arguments

- `tuple_func` *str* - Conversion function from string to two-element tuple.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - Dict made from tuples for each line over which `tuple_func`
was applied.

### String().trim_prefix

[[find in source code]](../../integraty/xstring.py#L581)

```python
def trim_prefix(prefix, pattern=None, exclude=False):
```

Trim substring in `prefix` from beginning of each line from input,
assuming substring is present.

#### Arguments

- `prefix` *str* - Prefix to trim from beginning of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with prefix trimmed from each.

### String().trim_suffix

[[find in source code]](../../integraty/xstring.py#L596)

```python
def trim_suffix(suffix, pattern=None, exclude=False):
```

Trim substring in `suffix` from end of each line from input,
assuming substring is present.

#### Arguments

- `suffix` *str* - Suffix to trim from end of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with suffix trimmed from each.

### String().with_prefix

[[find in source code]](../../integraty/xstring.py#L611)

```python
def with_prefix(prefix, pattern=None, exclude=False):
```

Limits included lines from input to those matching given prefix.
If a pattern results in some subset of original lines, this subset
will be subject to application of `prefix`. In other words, lines with
`prefix` may be excluded as a result of pattern matching, because
prefix checking occurs after application of `pattern` and `exclude`
parameters, not before.

#### Arguments

- `prefix` *str* - Lines with given prefix should be included.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given prefix.

### String().with_suffix

[[find in source code]](../../integraty/xstring.py#L630)

```python
def with_suffix(suffix, pattern=None, exclude=False):
```

Limits included lines from input to those matching given suffix.
If a pattern results in some subset of original lines, this subset
will be subject to application of `suffix`. In other words, lines with
`suffix` may be excluded as a result of pattern matching, because
suffix checking occurs after application of `pattern` and `exclude`
parameters, not before.

#### Arguments

- `suffix` *str* - Lines with given prefix should be included.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given suffix.

## stripper

[[find in source code]](../../integraty/xstring.py#L13)

```python
def stripper(w, chars):
```
