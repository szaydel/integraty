# Extprog

> Auto-generated documentation for [integraty.extprog](../../integraty/extprog.py) module.

- [Integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / `Integraty` / Extprog
    - [ExternalProgram](#externalprogram)
        - [ExternalProgram().block](#externalprogramblock)
        - [ExternalProgram().do_shell](#externalprogramdo_shell)
        - [ExternalProgram().err](#externalprogramerr)
        - [ExternalProgram().expect](#externalprogramexpect)
        - [ExternalProgram().is_alive](#externalprogramis_alive)
        - [ExternalProgram().kill](#externalprogramkill)
        - [ExternalProgram().ok](#externalprogramok)
        - [ExternalProgram().out](#externalprogramout)
        - [ExternalProgram().pid](#externalprogrampid)
        - [ExternalProgram().pipe](#externalprogrampipe)
        - [ExternalProgram().poll](#externalprogrampoll)
        - [ExternalProgram().return_code](#externalprogramreturn_code)
        - [ExternalProgram().run](#externalprogramrun)
        - [ExternalProgram().send](#externalprogramsend)
        - [ExternalProgram().std_err](#externalprogramstd_err)
        - [ExternalProgram().std_in](#externalprogramstd_in)
        - [ExternalProgram().std_out](#externalprogramstd_out)
        - [ExternalProgram().stderr_at_least_n_substr](#externalprogramstderr_at_least_n_substr)
        - [ExternalProgram().stderr_at_most_n_substr](#externalprogramstderr_at_most_n_substr)
        - [ExternalProgram().stderr_compress](#externalprogramstderr_compress)
        - [ExternalProgram().stderr_count](#externalprogramstderr_count)
        - [ExternalProgram().stderr_dict_from_line](#externalprogramstderr_dict_from_line)
        - [ExternalProgram().stderr_fields](#externalprogramstderr_fields)
        - [ExternalProgram().stderr_filter_func](#externalprogramstderr_filter_func)
        - [ExternalProgram().stderr_firstn](#externalprogramstderr_firstn)
        - [ExternalProgram().stderr_fold_funcs](#externalprogramstderr_fold_funcs)
        - [ExternalProgram().stderr_groupby](#externalprogramstderr_groupby)
        - [ExternalProgram().stderr_head](#externalprogramstderr_head)
        - [ExternalProgram().stderr_json_loads](#externalprogramstderr_json_loads)
        - [ExternalProgram().stderr_lastn](#externalprogramstderr_lastn)
        - [ExternalProgram().stderr_line_tuples](#externalprogramstderr_line_tuples)
        - [ExternalProgram().stderr_lines](#externalprogramstderr_lines)
        - [ExternalProgram().stderr_map_func](#externalprogramstderr_map_func)
        - [ExternalProgram().stderr_pairs](#externalprogramstderr_pairs)
        - [ExternalProgram().stderr_skip_lines](#externalprogramstderr_skip_lines)
        - [ExternalProgram().stderr_tail](#externalprogramstderr_tail)
        - [ExternalProgram().stderr_take_column](#externalprogramstderr_take_column)
        - [ExternalProgram().stderr_take_range_fields](#externalprogramstderr_take_range_fields)
        - [ExternalProgram().stderr_to_dict_func](#externalprogramstderr_to_dict_func)
        - [ExternalProgram().stderr_trim_prefix](#externalprogramstderr_trim_prefix)
        - [ExternalProgram().stderr_trim_suffix](#externalprogramstderr_trim_suffix)
        - [ExternalProgram().stderr_with_prefix](#externalprogramstderr_with_prefix)
        - [ExternalProgram().stderr_with_suffix](#externalprogramstderr_with_suffix)
        - [ExternalProgram().stdout_at_least_n_substr](#externalprogramstdout_at_least_n_substr)
        - [ExternalProgram().stdout_at_most_n_substr](#externalprogramstdout_at_most_n_substr)
        - [ExternalProgram().stdout_compress](#externalprogramstdout_compress)
        - [ExternalProgram().stdout_count](#externalprogramstdout_count)
        - [ExternalProgram().stdout_dict_from_line](#externalprogramstdout_dict_from_line)
        - [ExternalProgram().stdout_fields](#externalprogramstdout_fields)
        - [ExternalProgram().stdout_filter_func](#externalprogramstdout_filter_func)
        - [ExternalProgram().stdout_firstn](#externalprogramstdout_firstn)
        - [ExternalProgram().stdout_fold_funcs](#externalprogramstdout_fold_funcs)
        - [ExternalProgram().stdout_groupby](#externalprogramstdout_groupby)
        - [ExternalProgram().stdout_head](#externalprogramstdout_head)
        - [ExternalProgram().stdout_json_loads](#externalprogramstdout_json_loads)
        - [ExternalProgram().stdout_lastn](#externalprogramstdout_lastn)
        - [ExternalProgram().stdout_line_tuples](#externalprogramstdout_line_tuples)
        - [ExternalProgram().stdout_lines](#externalprogramstdout_lines)
        - [ExternalProgram().stdout_map_func](#externalprogramstdout_map_func)
        - [ExternalProgram().stdout_pairs](#externalprogramstdout_pairs)
        - [ExternalProgram().stdout_skip_lines](#externalprogramstdout_skip_lines)
        - [ExternalProgram().stdout_tail](#externalprogramstdout_tail)
        - [ExternalProgram().stdout_take_column](#externalprogramstdout_take_column)
        - [ExternalProgram().stdout_take_range_fields](#externalprogramstdout_take_range_fields)
        - [ExternalProgram().stdout_to_dict_func](#externalprogramstdout_to_dict_func)
        - [ExternalProgram().stdout_trim_prefix](#externalprogramstdout_trim_prefix)
        - [ExternalProgram().stdout_trim_suffix](#externalprogramstdout_trim_suffix)
        - [ExternalProgram().stdout_with_prefix](#externalprogramstdout_with_prefix)
        - [ExternalProgram().stdout_with_suffix](#externalprogramstdout_with_suffix)
        - [ExternalProgram().terminate](#externalprogramterminate)
    - [ExternalProgramException](#externalprogramexception)
    - [InvalidStream](#invalidstream)
    - [NoCommandException](#nocommandexception)
    - [chain](#chain)
    - [pid_exists](#pid_exists)
    - [run](#run)
    - [stripper](#stripper)

## ExternalProgram

[[find in source code]](../../integraty/extprog.py#L78)

```python
class ExternalProgram(object):
    def __init__(cmd, timeout=None):
```

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

```python
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
```

Try this out with `python3 -m doctest integraty/extprog.py` if you have
sources checked out in a convenient place.

### ExternalProgram().block

[[find in source code]](../../integraty/extprog.py#L1616)

```python
def block():
```

Blocks until process is complete.

### ExternalProgram().do_shell

[[find in source code]](../../integraty/extprog.py#L1569)

```python
def do_shell(env=None, shell=True):
```

Runs the command and blocks (waits) until the command is complete.

### ExternalProgram().err

[[find in source code]](../../integraty/extprog.py#L1497)

```python
@property
def err():
```

Std/err output (cached)

### ExternalProgram().expect

[[find in source code]](../../integraty/extprog.py#L1578)

```python
def expect(pattern, timeout=-1):
```

Waits on the given pattern to appear in std_out

### ExternalProgram().is_alive

[[find in source code]](../../integraty/extprog.py#L1521)

```python
@property
def is_alive():
```

Is the process alive?

### ExternalProgram().kill

[[find in source code]](../../integraty/extprog.py#L1610)

```python
def kill():
```

### ExternalProgram().ok

[[find in source code]](../../integraty/extprog.py#L1458)

```python
@property
def ok():
```

### ExternalProgram().out

[[find in source code]](../../integraty/extprog.py#L1478)

```python
@property
def out():
```

Std/out output (cached)

### ExternalProgram().pid

[[find in source code]](../../integraty/extprog.py#L1512)

```python
@property
def pid():
```

The process' PID.

### ExternalProgram().pipe

[[find in source code]](../../integraty/extprog.py#L1653)

```python
def pipe(command, timeout=None, cwd=None):
```

Runs the current command and passes its output to the next
given process.

### ExternalProgram().poll

[[find in source code]](../../integraty/extprog.py#L1643)

```python
def poll():
```

### ExternalProgram().return_code

[[find in source code]](../../integraty/extprog.py#L1526)

```python
@property
def return_code():
```

### ExternalProgram().run

[[find in source code]](../../integraty/extprog.py#L1538)

```python
def run(block=True, binary=False, cwd=None, env=None, shell=True):
```

Runs the given command, with or without pexpect functionality enabled.

### ExternalProgram().send

[[find in source code]](../../integraty/extprog.py#L1591)

```python
def send(s, end=os.linesep, signal=False):
```

Sends the given string or signal to std_in.

### ExternalProgram().std_err

[[find in source code]](../../integraty/extprog.py#L1493)

```python
@property
def std_err():
```

### ExternalProgram().std_in

[[find in source code]](../../integraty/extprog.py#L1534)

```python
@property
def std_in():
```

### ExternalProgram().std_out

[[find in source code]](../../integraty/extprog.py#L1454)

```python
@property
def std_out():
```

### ExternalProgram().stderr_at_least_n_substr

[[find in source code]](../../integraty/extprog.py#L1217)

```python
def stderr_at_least_n_substr(substr=None, n=0):
```

### ExternalProgram().stderr_at_most_n_substr

[[find in source code]](../../integraty/extprog.py#L1223)

```python
def stderr_at_most_n_substr(substr=None, n=0):
```

### ExternalProgram().stderr_compress

[[find in source code]](../../integraty/extprog.py#L939)

```python
def stderr_compress(sep=None, indexes=(), pattern=None, exclude=False):
```

Select one or more fields from each line from stderr, after splitting
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

### ExternalProgram().stderr_count

[[find in source code]](../../integraty/extprog.py#L557)

```python
def stderr_count(pattern=None, exclude=False):
```

Count number of lines written to stderr.

#### Arguments

- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `int` - Count of lines.

### ExternalProgram().stderr_dict_from_line

[[find in source code]](../../integraty/extprog.py#L688)

```python
def stderr_dict_from_line(keys=None, sep=None, pattern=None, exclude=False):
```

Converts stderr lines into dicts, where `keys` is a list of keys which
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

### ExternalProgram().stderr_fields

[[find in source code]](../../integraty/extprog.py#L851)

```python
def stderr_fields(sep=None, pattern=None, exclude=False):
```

Split each line from stderr into fields and join each column into a
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

### ExternalProgram().stderr_filter_func

[[find in source code]](../../integraty/extprog.py#L1243)

```python
def stderr_filter_func(func, exclude=False):
```

Filters lines written to stderr with a filtering function in
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

### ExternalProgram().stderr_firstn

[[find in source code]](../../integraty/extprog.py#L730)

```python
def stderr_firstn(n=1, pattern=None, exclude=None):
```

Select first n lines from stderr.

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines 0 through n.

### ExternalProgram().stderr_fold_funcs

[[find in source code]](../../integraty/extprog.py#L1324)

```python
def stderr_fold_funcs(pattern=None, exclude=None, *funcs):
```

Higher-order function taking one or more functions composing them
together, then applying the composed function over each line from
stderr.
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

- `*funcs` *(Sequence[Callable[(s* - str) -> string]]): A sequence of functions, each receiving a string and emitting a string.

#### Returns

- `list` - List of results from application of sequence of callables.

### ExternalProgram().stderr_groupby

[[find in source code]](../../integraty/extprog.py#L1427)

```python
def stderr_groupby(column=0, sep=None, pattern=None, exclude=False):
```

For each line from stderr, split line on `sep` and treat the substring
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

### ExternalProgram().stderr_head

[[find in source code]](../../integraty/extprog.py#L788)

```python
def stderr_head(sep=None, pattern=None, exclude=False):
```

Select first column of each line from stderr, after splitting on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of first element of each split line.

### ExternalProgram().stderr_json_loads

[[find in source code]](../../integraty/extprog.py#L534)

```python
@property
def stderr_json_loads():
```

For JSON data written to stderr, attempt to convert to native data type.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### ExternalProgram().stderr_lastn

[[find in source code]](../../integraty/extprog.py#L758)

```python
def stderr_lastn(n=1, pattern=None, exclude=None):
```

Select last n lines from stderr.

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines len(lines) - n through len(lines).

### ExternalProgram().stderr_line_tuples

[[find in source code]](../../integraty/extprog.py#L1032)

```python
def stderr_line_tuples(
    sep=None,
    pattern=None,
    exclude=False,
    strip_punct=False,
    strip_chars=PCHARS,
):
```

Split lines written to stdout into tuples on `sep`, where each line is
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

### ExternalProgram().stderr_lines

[[find in source code]](../../integraty/extprog.py#L1068)

```python
@property
def stderr_lines():
```

Unfiltered lines written to stderr.

#### Returns

- `list` - List of lines written to stderr.

### ExternalProgram().stderr_map_func

[[find in source code]](../../integraty/extprog.py#L1276)

```python
def stderr_map_func(func, pattern=None, exclude=None):
```

Applies function in 'func' to each line written to stderr.
Transformations from these map operations will be included in
the resulting list. Result of calling 'func' should not be None.

#### Arguments

- `func` *((s* - str) -> Any): Mapping function receiving a string and emitting Any other type.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of results from application of mapping function.

### ExternalProgram().stderr_pairs

[[find in source code]](../../integraty/extprog.py#L1381)

```python
def stderr_pairs(as_dict=False, sep=None, pattern=None, exclude=False):
```

Break-up each line from stderr into pairs, optionally placing these
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

### ExternalProgram().stderr_skip_lines

[[find in source code]](../../integraty/extprog.py#L597)

```python
def stderr_skip_lines(skip_head=0, skip_tail=0, pattern=None, exclude=False):
```

Skips some number of lines from the beginning, i.e. the head of the list
and/or from the end, i.e. the tail of the list of lines from stderr.
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

- `list` - List of lines written to stderr.

### ExternalProgram().stderr_tail

[[find in source code]](../../integraty/extprog.py#L816)

```python
def stderr_tail(sep=None, pattern=None, exclude=False):
```

Select all but first column of each line from stderr, after splitting on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples with all but first element of each split line.

### ExternalProgram().stderr_take_column

[[find in source code]](../../integraty/extprog.py#L890)

```python
def stderr_take_column(sep=None, column=0, pattern=None, exclude=False):
```

Select a single column from each line from stderr, after splitting the
line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `column` *int, optional* - [description]. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of elements extracted, one from each split line.

### ExternalProgram().stderr_take_range_fields

[[find in source code]](../../integraty/extprog.py#L986)

```python
def stderr_take_range_fields(
    sep=None,
    slc_range=(0, 1, 1),
    pattern=None,
    exclude=False,
):
```

Select multiple fields within the 'slc_range' range from each line
from stderr, after splitting the line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `slc_range` *tuple, optional* - Range (start, end, stride). Defaults to (0, 1, 1).
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### ExternalProgram().stderr_to_dict_func

[[find in source code]](../../integraty/extprog.py#L642)

```python
def stderr_to_dict_func(tuple_func, pattern=None, exclude=False):
```

Applies `tuple_func` to each line from stdout, adding resulting tuple
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

### ExternalProgram().stderr_trim_prefix

[[find in source code]](../../integraty/extprog.py#L1093)

```python
def stderr_trim_prefix(prefix, pattern=None, exclude=False):
```

Trim substring in `prefix` from beginning of each line from stderr,
assuming substring is present.

#### Arguments

- `prefix` *str* - Prefix to trim from beginning of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with prefix trimmed from each.

### ExternalProgram().stderr_trim_suffix

[[find in source code]](../../integraty/extprog.py#L1123)

```python
def stderr_trim_suffix(suffix, pattern=None, exclude=False):
```

Trim substring in `suffix` from end of each line from stderr,
assuming substring is present.

#### Arguments

- `suffix` *str* - Suffix to trim from end of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with suffix trimmed from each.

### ExternalProgram().stderr_with_prefix

[[find in source code]](../../integraty/extprog.py#L1157)

```python
def stderr_with_prefix(prefix, pattern=None, exclude=False):
```

Limits included lines from stderr to those matching given prefix.
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

### ExternalProgram().stderr_with_suffix

[[find in source code]](../../integraty/extprog.py#L1195)

```python
def stderr_with_suffix(suffix, pattern=None, exclude=False):
```

Limits included lines from stderr to those matching given suffix.
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

### ExternalProgram().stdout_at_least_n_substr

[[find in source code]](../../integraty/extprog.py#L1214)

```python
def stdout_at_least_n_substr(substr=None, n=0):
```

### ExternalProgram().stdout_at_most_n_substr

[[find in source code]](../../integraty/extprog.py#L1220)

```python
def stdout_at_most_n_substr(substr=None, n=0):
```

### ExternalProgram().stdout_compress

[[find in source code]](../../integraty/extprog.py#L910)

```python
def stdout_compress(sep=None, indexes=(), pattern=None, exclude=False):
```

Select one or more fields from each line from stdout, after splitting
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

### ExternalProgram().stdout_count

[[find in source code]](../../integraty/extprog.py#L544)

```python
def stdout_count(pattern=None, exclude=False):
```

Count number of lines written to stdout.

#### Arguments

- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `int` - Count of lines.

### ExternalProgram().stdout_dict_from_line

[[find in source code]](../../integraty/extprog.py#L662)

```python
def stdout_dict_from_line(keys=None, sep=None, pattern=None, exclude=False):
```

Converts stdout lines into dicts, where `keys` is a list of keys which
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

### ExternalProgram().stdout_fields

[[find in source code]](../../integraty/extprog.py#L830)

```python
def stdout_fields(sep=None, pattern=None, exclude=False):
```

Split each line from stdout into fields and join each column into a
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

### ExternalProgram().stdout_filter_func

[[find in source code]](../../integraty/extprog.py#L1226)

```python
def stdout_filter_func(func, exclude=False):
```

Filters lines written to stdout with a filtering function in
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

### ExternalProgram().stdout_firstn

[[find in source code]](../../integraty/extprog.py#L716)

```python
def stdout_firstn(n=1, pattern=None, exclude=None):
```

Select first n lines from stdout.

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines 0 through n.

### ExternalProgram().stdout_fold_funcs

[[find in source code]](../../integraty/extprog.py#L1294)

```python
def stdout_fold_funcs(pattern=None, exclude=None, *funcs):
```

Higher-order function taking one or more functions composing them
together, then applying the composed function over each line from
stdout.
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

### ExternalProgram().stdout_groupby

[[find in source code]](../../integraty/extprog.py#L1406)

```python
def stdout_groupby(column=0, sep=None, pattern=None, exclude=False):
```

For each line from stdout, split line on `sep` and treat the substring
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

### ExternalProgram().stdout_head

[[find in source code]](../../integraty/extprog.py#L774)

```python
def stdout_head(sep=None, pattern=None, exclude=False):
```

Select first column of each line from stdout, after splitting on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of first element of each split line.

### ExternalProgram().stdout_json_loads

[[find in source code]](../../integraty/extprog.py#L524)

```python
@property
def stdout_json_loads():
```

For JSON data written to stdout, attempt to convert to native data type.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### ExternalProgram().stdout_lastn

[[find in source code]](../../integraty/extprog.py#L744)

```python
def stdout_lastn(n=1, pattern=None, exclude=None):
```

Select last n lines from stdout.

#### Arguments

- `n` *int, optional* - Number of lines to select. Defaults to 1.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines len(lines) - n through len(lines).

### ExternalProgram().stdout_line_tuples

[[find in source code]](../../integraty/extprog.py#L1006)

```python
def stdout_line_tuples(
    sep=None,
    pattern=None,
    exclude=False,
    strip_punct=False,
    strip_chars=PCHARS,
):
```

Split lines written to stdout into tuples on `sep`, where each line is
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

### ExternalProgram().stdout_lines

[[find in source code]](../../integraty/extprog.py#L1058)

```python
@property
def stdout_lines():
```

Unfiltered lines written to stdout.

#### Returns

- `list` - List of lines written to stdout.

### ExternalProgram().stdout_map_func

[[find in source code]](../../integraty/extprog.py#L1260)

```python
def stdout_map_func(func, pattern=None, exclude=False):
```

Applies function in 'func' to each line written to stdout.
Transformations from these map operations will be included in
the resulting list. Result of calling 'func' should not be None.

#### Arguments

- `func` *((s* - str) -> Any): Mapping function receiving a string and emitting Any other type.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of results from application of mapping function.

### ExternalProgram().stdout_pairs

[[find in source code]](../../integraty/extprog.py#L1356)

```python
def stdout_pairs(as_dict=False, sep=None, pattern=None, exclude=False):
```

Break-up each line from stdout into pairs, optionally placing these
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

### ExternalProgram().stdout_skip_lines

[[find in source code]](../../integraty/extprog.py#L570)

```python
def stdout_skip_lines(skip_head=0, skip_tail=0, pattern=None, exclude=False):
```

Skips some number of lines from the beginning, i.e. the head of the list
and/or from the end, i.e. the tail of the list of lines from stdout.
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

- `list` - List of lines written to stdout.

### ExternalProgram().stdout_tail

[[find in source code]](../../integraty/extprog.py#L802)

```python
def stdout_tail(sep=None, pattern=None, exclude=False):
```

Select all but first column of each line from stdout, after splitting on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples with all but first element of each split line.

### ExternalProgram().stdout_take_column

[[find in source code]](../../integraty/extprog.py#L872)

```python
def stdout_take_column(sep=None, column=0, pattern=None, exclude=False):
```

Select a single column of each line from stdout, after splitting the
line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `column` *int, optional* - Select column matching this index. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of elements extracted from each split line.

### ExternalProgram().stdout_take_range_fields

[[find in source code]](../../integraty/extprog.py#L968)

```python
def stdout_take_range_fields(
    sep=None,
    slc_range=(0, 1, 1),
    pattern=None,
    exclude=False,
):
```

Select multiple fields within the 'slc_range' range from each line
from stdout, after splitting the line on `sep`.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `slc_range` *tuple, optional* - Range (start, end, stride). Defaults to (0, 1, 1).
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more fields from each split line.

### ExternalProgram().stdout_to_dict_func

[[find in source code]](../../integraty/extprog.py#L624)

```python
def stdout_to_dict_func(tuple_func, pattern=None, exclude=False):
```

Applies `tuple_func` to each line from stdout, adding resulting tuple
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

### ExternalProgram().stdout_trim_prefix

[[find in source code]](../../integraty/extprog.py#L1078)

```python
def stdout_trim_prefix(prefix, pattern=None, exclude=False):
```

Trim substring in `prefix` from beginning of each line from stdout,
assuming substring is present.

#### Arguments

- `prefix` *str* - Prefix to trim from beginning of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with prefix trimmed from each.

### ExternalProgram().stdout_trim_suffix

[[find in source code]](../../integraty/extprog.py#L1108)

```python
def stdout_trim_suffix(suffix, pattern=None, exclude=False):
```

Trim substring in `suffix` from end of each line from stdout,
assuming substring is present.

#### Arguments

- `suffix` *str* - Suffix to trim from end of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with suffix trimmed from each.

### ExternalProgram().stdout_with_prefix

[[find in source code]](../../integraty/extprog.py#L1138)

```python
def stdout_with_prefix(prefix, pattern=None, exclude=False):
```

Limits included lines from stdout to those matching given prefix.
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

### ExternalProgram().stdout_with_suffix

[[find in source code]](../../integraty/extprog.py#L1176)

```python
def stdout_with_suffix(suffix, pattern=None, exclude=False):
```

Limits included lines from stdout to those matching given suffix.
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

### ExternalProgram().terminate

[[find in source code]](../../integraty/extprog.py#L1607)

```python
def terminate():
```

## ExternalProgramException

[[find in source code]](../../integraty/extprog.py#L46)

```python
class ExternalProgramException(Exception):
```

## InvalidStream

[[find in source code]](../../integraty/extprog.py#L42)

```python
class InvalidStream(Exception):
```

## NoCommandException

[[find in source code]](../../integraty/extprog.py#L38)

```python
class NoCommandException(Exception):
```

## chain

[[find in source code]](../../integraty/extprog.py#L1704)

```python
def chain(command, timeout=None, cwd=None, env=None):
```

## pid_exists

[[find in source code]](../../integraty/extprog.py#L50)

```python
def pid_exists(pid):
```

Check whether pid exists in the current process table.

## run

[[find in source code]](../../integraty/extprog.py#L1721)

```python
def run(command, block=True, binary=False, timeout=None, cwd=None, env=None):
```

## stripper

[[find in source code]](../../integraty/extprog.py#L31)

```python
def stripper(w, chars):
```
