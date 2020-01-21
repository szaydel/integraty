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
        - [ExternalProgram().stderr_columns](#externalprogramstderr_columns)
        - [ExternalProgram().stderr_count](#externalprogramstderr_count)
        - [ExternalProgram().stderr_dict_from_line](#externalprogramstderr_dict_from_line)
        - [ExternalProgram().stderr_filter_func](#externalprogramstderr_filter_func)
        - [ExternalProgram().stderr_firstn](#externalprogramstderr_firstn)
        - [ExternalProgram().stderr_funcs_pipeline](#externalprogramstderr_funcs_pipeline)
        - [ExternalProgram().stderr_head](#externalprogramstderr_head)
        - [ExternalProgram().stderr_json_loads](#externalprogramstderr_json_loads)
        - [ExternalProgram().stderr_lastn](#externalprogramstderr_lastn)
        - [ExternalProgram().stderr_line_tuples](#externalprogramstderr_line_tuples)
        - [ExternalProgram().stderr_lines](#externalprogramstderr_lines)
        - [ExternalProgram().stderr_map_func](#externalprogramstderr_map_func)
        - [ExternalProgram().stderr_skip_lines](#externalprogramstderr_skip_lines)
        - [ExternalProgram().stderr_tail](#externalprogramstderr_tail)
        - [ExternalProgram().stderr_take_column](#externalprogramstderr_take_column)
        - [ExternalProgram().stderr_take_range_columns](#externalprogramstderr_take_range_columns)
        - [ExternalProgram().stderr_take_some_columns](#externalprogramstderr_take_some_columns)
        - [ExternalProgram().stderr_to_dict_func](#externalprogramstderr_to_dict_func)
        - [ExternalProgram().stderr_to_tuple_func](#externalprogramstderr_to_tuple_func)
        - [ExternalProgram().stderr_trim_prefix](#externalprogramstderr_trim_prefix)
        - [ExternalProgram().stderr_trim_suffix](#externalprogramstderr_trim_suffix)
        - [ExternalProgram().stderr_with_prefix](#externalprogramstderr_with_prefix)
        - [ExternalProgram().stderr_with_suffix](#externalprogramstderr_with_suffix)
        - [ExternalProgram().stdout_at_least_n_substr](#externalprogramstdout_at_least_n_substr)
        - [ExternalProgram().stdout_at_most_n_substr](#externalprogramstdout_at_most_n_substr)
        - [ExternalProgram().stdout_columns](#externalprogramstdout_columns)
        - [ExternalProgram().stdout_count](#externalprogramstdout_count)
        - [ExternalProgram().stdout_dict_from_line](#externalprogramstdout_dict_from_line)
        - [ExternalProgram().stdout_filter_func](#externalprogramstdout_filter_func)
        - [ExternalProgram().stdout_firstn](#externalprogramstdout_firstn)
        - [ExternalProgram().stdout_funcs_pipeline](#externalprogramstdout_funcs_pipeline)
        - [ExternalProgram().stdout_head](#externalprogramstdout_head)
        - [ExternalProgram().stdout_json_loads](#externalprogramstdout_json_loads)
        - [ExternalProgram().stdout_lastn](#externalprogramstdout_lastn)
        - [ExternalProgram().stdout_line_tuples](#externalprogramstdout_line_tuples)
        - [ExternalProgram().stdout_lines](#externalprogramstdout_lines)
        - [ExternalProgram().stdout_map_func](#externalprogramstdout_map_func)
        - [ExternalProgram().stdout_skip_lines](#externalprogramstdout_skip_lines)
        - [ExternalProgram().stdout_tail](#externalprogramstdout_tail)
        - [ExternalProgram().stdout_take_column](#externalprogramstdout_take_column)
        - [ExternalProgram().stdout_take_range_columns](#externalprogramstdout_take_range_columns)
        - [ExternalProgram().stdout_take_some_columns](#externalprogramstdout_take_some_columns)
        - [ExternalProgram().stdout_to_dict_func](#externalprogramstdout_to_dict_func)
        - [ExternalProgram().stdout_to_tuple_func](#externalprogramstdout_to_tuple_func)
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

[[find in source code]](../../integraty/extprog.py#L1481)

```python
def block():
```

Blocks until process is complete.

### ExternalProgram().do_shell

[[find in source code]](../../integraty/extprog.py#L1434)

```python
def do_shell(env=None, shell=True):
```

Runs the command and blocks (waits) until the command is complete.

### ExternalProgram().err

[[find in source code]](../../integraty/extprog.py#L1362)

```python
@property
def err():
```

Std/err output (cached)

### ExternalProgram().expect

[[find in source code]](../../integraty/extprog.py#L1443)

```python
def expect(pattern, timeout=-1):
```

Waits on the given pattern to appear in std_out

### ExternalProgram().is_alive

[[find in source code]](../../integraty/extprog.py#L1386)

```python
@property
def is_alive():
```

Is the process alive?

### ExternalProgram().kill

[[find in source code]](../../integraty/extprog.py#L1475)

```python
def kill():
```

### ExternalProgram().ok

[[find in source code]](../../integraty/extprog.py#L1323)

```python
@property
def ok():
```

### ExternalProgram().out

[[find in source code]](../../integraty/extprog.py#L1343)

```python
@property
def out():
```

Std/out output (cached)

### ExternalProgram().pid

[[find in source code]](../../integraty/extprog.py#L1377)

```python
@property
def pid():
```

The process' PID.

### ExternalProgram().pipe

[[find in source code]](../../integraty/extprog.py#L1518)

```python
def pipe(command, timeout=None, cwd=None):
```

Runs the current command and passes its output to the next
given process.

### ExternalProgram().poll

[[find in source code]](../../integraty/extprog.py#L1508)

```python
def poll():
```

### ExternalProgram().return_code

[[find in source code]](../../integraty/extprog.py#L1391)

```python
@property
def return_code():
```

### ExternalProgram().run

[[find in source code]](../../integraty/extprog.py#L1403)

```python
def run(block=True, binary=False, cwd=None, env=None, shell=True):
```

Runs the given command, with or without pexpect functionality enabled.

### ExternalProgram().send

[[find in source code]](../../integraty/extprog.py#L1456)

```python
def send(s, end=os.linesep, signal=False):
```

Sends the given string or signal to std_in.

### ExternalProgram().std_err

[[find in source code]](../../integraty/extprog.py#L1358)

```python
@property
def std_err():
```

### ExternalProgram().std_in

[[find in source code]](../../integraty/extprog.py#L1399)

```python
@property
def std_in():
```

### ExternalProgram().std_out

[[find in source code]](../../integraty/extprog.py#L1319)

```python
@property
def std_out():
```

### ExternalProgram().stderr_at_least_n_substr

[[find in source code]](../../integraty/extprog.py#L1186)

```python
def stderr_at_least_n_substr(substr=None, n=0):
```

### ExternalProgram().stderr_at_most_n_substr

[[find in source code]](../../integraty/extprog.py#L1192)

```python
def stderr_at_most_n_substr(substr=None, n=0):
```

### ExternalProgram().stderr_columns

[[find in source code]](../../integraty/extprog.py#L842)

```python
def stderr_columns(sep=None, pattern=None, exclude=False):
```

Split each line from stderr into columns and join each column into a
tuple. This is meant to be used with text where multiple lines contain
same number of fields (columns), and result of this is a list of tuples
where each tuple contains elements from a given position across all
lines. Given a string: 'alpha beta gamma\ndelta epsilon zeta\n', this
produces: [('alpha', 'delta'), ('beta', 'epsilon'), ('gamma', 'zeta')].

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples from each split line.

### ExternalProgram().stderr_count

[[find in source code]](../../integraty/extprog.py#L515)

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

[[find in source code]](../../integraty/extprog.py#L681)

```python
def stderr_dict_from_line(keys=None, sep=None, pattern=None, exclude=False):
```

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

#### Arguments

- `keys` *hashable, optional* - A list of keys to build a dict from line. Defaults to None.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of dictionaries generated from lines.

### ExternalProgram().stderr_filter_func

[[find in source code]](../../integraty/extprog.py#L1212)

```python
def stderr_filter_func(func, exclude=False):
```

Filters lines written to stderr with a filtering function in
'func' argument. This function should expect a single string argument
which will be a line and return a boolean. Any lines that cause this
function to return `True` will be included in the resulting list, and
those that result in `False` will be excluded, unless 'exclude' is
`True`, which inverts this logic.

#### Arguments

- `func` *((s* - str) -> bool): Filtering function emitting a boolean.
- `exclude` *bool, optional* - Invert filtering logic. Defaults to False.

#### Returns

- `list` - List of lines after filtering function is applied.

### ExternalProgram().stderr_firstn

[[find in source code]](../../integraty/extprog.py#L723)

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

### ExternalProgram().stderr_funcs_pipeline

[[find in source code]](../../integraty/extprog.py#L1290)

```python
def stderr_funcs_pipeline(*funcs):
```

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

#### Arguments

- `*funcs` *(Sequence[Callable[(s* - str) -> string]]): A sequence of functions, each receiving a string and emitting a string.

#### Returns

- `list` - List of results from application of sequence of callables.

### ExternalProgram().stderr_head

[[find in source code]](../../integraty/extprog.py#L781)

```python
def stderr_head(sep=None, pattern=None, exclude=False):
```

Select first column of each line from stderr, after splitting on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of first element of each split line.

### ExternalProgram().stderr_json_loads

[[find in source code]](../../integraty/extprog.py#L492)

```python
@property
def stderr_json_loads():
```

For JSON data written to stderr, attempt to convert to native data type.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### ExternalProgram().stderr_lastn

[[find in source code]](../../integraty/extprog.py#L751)

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

[[find in source code]](../../integraty/extprog.py#L1001)

```python
def stderr_line_tuples(
    sep=None,
    pattern=None,
    exclude=False,
    strip_punct=False,
    strip_chars=PCHARS,
):
```

Split lines written to stdout into tuples on 'sep', where each line is
a tuple consisting of all split tokens from that line.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.
- `strip_punct` *bool, optional* - Enable punctuation stripping. Defaults to False.
- `strip_chars` *str, optional* - Characters to strip if 'strip_punct' is True. Defaults to PCHARS.

#### Returns

- `list` - List of tuples, where each tuple contains columns from each split line.

#### See also

- [PCHARS](#pchars)

### ExternalProgram().stderr_lines

[[find in source code]](../../integraty/extprog.py#L1037)

```python
@property
def stderr_lines():
```

Unfiltered lines written to stderr.

#### Returns

- `list` - List of lines written to stderr.

### ExternalProgram().stderr_map_func

[[find in source code]](../../integraty/extprog.py#L1245)

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

### ExternalProgram().stderr_skip_lines

[[find in source code]](../../integraty/extprog.py#L555)

```python
def stderr_skip_lines(skip_head=0, skip_tail=0, pattern=None, exclude=False):
```

Skips some number of lines from the beginning, i.e. the head of the list
and/or from the end, i.e. the tail of the list of lines from stderr.
If a pattern results in some subset of original lines, this subset will
be subject to application of 'skip_head' and/or 'skip_tail'. In other
words, skipping of lines occurs after application of 'pattern' and
'exclude' parameters, not before.

#### Arguments

- `skip_head` *int, optional* - Number of lines to skip relative to beginning of data. Defaults to 0.
- `skip_tail` *int, optional* - Number of lines to skip relative to the end of the data. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines written to stderr.

### ExternalProgram().stderr_tail

[[find in source code]](../../integraty/extprog.py#L809)

```python
def stderr_tail(sep=None, pattern=None, exclude=False):
```

Select all but first column of each line from stderr, after splitting on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples with all but first element of each split line.

### ExternalProgram().stderr_take_column

[[find in source code]](../../integraty/extprog.py#L879)

```python
def stderr_take_column(sep=None, column=0, pattern=None, exclude=False):
```

Select a single column from each line from stderr, after splitting the
line on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `column` *int, optional* - [description]. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of elements extracted, one from each split line.

### ExternalProgram().stderr_take_range_columns

[[find in source code]](../../integraty/extprog.py#L955)

```python
def stderr_take_range_columns(
    sep=None,
    slc_range=(0, 1, 1),
    pattern=None,
    exclude=False,
):
```

Select multiple columns within the 'slc_range' range from each line
from stderr, after splitting the line on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `slc_range` *tuple, optional* - Range (start, end, stride). Defaults to (0, 1, 1).
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more columns from each split line.

### ExternalProgram().stderr_take_some_columns

[[find in source code]](../../integraty/extprog.py#L917)

```python
def stderr_take_some_columns(
    sep=None,
    selectors=(),
    pattern=None,
    exclude=False,
):
```

Select multiple columns from each line from stderr, after splitting the
line on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `selectors` *tuple, optional* - Sequence of column indexes. Defaults to ().
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more columns from each split line.

### ExternalProgram().stderr_to_dict_func

[[find in source code]](../../integraty/extprog.py#L635)

```python
def stderr_to_dict_func(tuple_func, pattern=None, exclude=False):
```

Applies 'tuple_func' to each line from stdout, adding resulting tuple
to dict. It is expected that result from 'tuple_func' is a single
two-element tuple object, where first element becomes dict key and
second value for given key.

#### Arguments

- `tuple_func` *str* - Conversion function from string to two-element tuple.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - Dict made from tuples for each line over which 'tuple_func'
was applied.

### ExternalProgram().stderr_to_tuple_func

[[find in source code]](../../integraty/extprog.py#L599)

```python
def stderr_to_tuple_func(tuple_func, pattern=None, exclude=False):
```

Applies 'tuple_func' to each line from stderr, adding resulting tuple
to list. It is expected that result from 'tuple_func' is a single tuple
object.

#### Arguments

- `tuple_func` *str* - Conversion function from string to N-element tuple.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list(tuple)` - List of tuples for each line over which 'tuple_func' was applied.

### ExternalProgram().stderr_trim_prefix

[[find in source code]](../../integraty/extprog.py#L1062)

```python
def stderr_trim_prefix(prefix, pattern=None, exclude=False):
```

Trim substring in 'prefix' from beginning of each line from stderr,
assuming substring is present.

#### Arguments

- `prefix` *str* - Prefix to trim from beginning of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with prefix trimmed from each.

### ExternalProgram().stderr_trim_suffix

[[find in source code]](../../integraty/extprog.py#L1092)

```python
def stderr_trim_suffix(suffix, pattern=None, exclude=False):
```

Trim substring in 'suffix' from end of each line from stderr,
assuming substring is present.

#### Arguments

- `suffix` *str* - Suffix to trim from end of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with suffix trimmed from each.

### ExternalProgram().stderr_with_prefix

[[find in source code]](../../integraty/extprog.py#L1126)

```python
def stderr_with_prefix(prefix, pattern=None, exclude=False):
```

Limits included lines from stderr to those matching given prefix.
If a pattern results in some subset of original lines, this subset
will be subject to application of 'prefix'. In other words, lines with
'prefix' may be excluded as a result of pattern matching, because
prefix checking occurs after application of 'pattern' and 'exclude'
parameters, not before.

#### Arguments

- `prefix` *str* - Lines with given prefix should be included.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given prefix.

### ExternalProgram().stderr_with_suffix

[[find in source code]](../../integraty/extprog.py#L1164)

```python
def stderr_with_suffix(suffix, pattern=None, exclude=False):
```

Limits included lines from stderr to those matching given suffix.
If a pattern results in some subset of original lines, this subset
will be subject to application of 'suffix'. In other words, lines with
'suffix' may be excluded as a result of pattern matching, because
suffix checking occurs after application of 'pattern' and 'exclude'
parameters, not before.

#### Arguments

- `suffix` *str* - Lines with given prefix should be included.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given suffix.

### ExternalProgram().stdout_at_least_n_substr

[[find in source code]](../../integraty/extprog.py#L1183)

```python
def stdout_at_least_n_substr(substr=None, n=0):
```

### ExternalProgram().stdout_at_most_n_substr

[[find in source code]](../../integraty/extprog.py#L1189)

```python
def stdout_at_most_n_substr(substr=None, n=0):
```

### ExternalProgram().stdout_columns

[[find in source code]](../../integraty/extprog.py#L823)

```python
def stdout_columns(sep=None, pattern=None, exclude=False):
```

Split each line from stdout into columns and join each column into a
tuple. This is meant to be used with text where multiple lines contain
same number of fields (columns), and result of this is a list of tuples
where each tuple contains elements from a given position across all
lines. Given a string: 'alpha beta gamma\ndelta epsilon zeta\n', this
produces: [('alpha', 'delta'), ('beta', 'epsilon'), ('gamma', 'zeta')].

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples from each split line.

### ExternalProgram().stdout_count

[[find in source code]](../../integraty/extprog.py#L502)

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

[[find in source code]](../../integraty/extprog.py#L655)

```python
def stdout_dict_from_line(keys=None, sep=None, pattern=None, exclude=False):
```

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

#### Arguments

- `keys` *hashable, optional* - A list of keys to build a dict from line. Defaults to None.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of dictionaries generated from lines.

### ExternalProgram().stdout_filter_func

[[find in source code]](../../integraty/extprog.py#L1195)

```python
def stdout_filter_func(func, exclude=False):
```

Filters lines written to stdout with a filtering function in
'func' argument. This function should expect a single string argument
which will be a line and return a boolean. Any lines that cause this
function to return `True` will be included in the resulting list, and
those that result in `False` will be excluded, unless 'exclude' is
`True`, which inverts this logic.

#### Arguments

- `func` *((s* - str) -> bool): Filtering function emitting a boolean.
- `exclude` *bool, optional* - Invert filtering logic. Defaults to False.

#### Returns

- `list` - List of lines after filtering function is applied.

### ExternalProgram().stdout_firstn

[[find in source code]](../../integraty/extprog.py#L709)

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

### ExternalProgram().stdout_funcs_pipeline

[[find in source code]](../../integraty/extprog.py#L1263)

```python
def stdout_funcs_pipeline(*funcs):
```

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

#### Arguments

- `*funcs` *(Sequence[Callable[(s* - str) -> string]]): A sequence of functions, each receiving a string and emitting a string.

#### Returns

- `list` - List of results from application of sequence of callables.

### ExternalProgram().stdout_head

[[find in source code]](../../integraty/extprog.py#L767)

```python
def stdout_head(sep=None, pattern=None, exclude=False):
```

Select first column of each line from stdout, after splitting on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of first element of each split line.

### ExternalProgram().stdout_json_loads

[[find in source code]](../../integraty/extprog.py#L482)

```python
@property
def stdout_json_loads():
```

For JSON data written to stdout, attempt to convert to native data type.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### ExternalProgram().stdout_lastn

[[find in source code]](../../integraty/extprog.py#L737)

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

[[find in source code]](../../integraty/extprog.py#L975)

```python
def stdout_line_tuples(
    sep=None,
    pattern=None,
    exclude=False,
    strip_punct=False,
    strip_chars=PCHARS,
):
```

Split lines written to stdout into tuples on 'sep', where each line is
a tuple consisting of all split tokens from that line.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.
- `strip_punct` *bool, optional* - Enable punctuation stripping. Defaults to False.
- `strip_chars` *str, optional* - Characters to strip if 'strip_punct' is True. Defaults to PCHARS.

#### Returns

- `list` - List of tuples, where each tuple contains columns from each split line.

#### See also

- [PCHARS](#pchars)

### ExternalProgram().stdout_lines

[[find in source code]](../../integraty/extprog.py#L1027)

```python
@property
def stdout_lines():
```

Unfiltered lines written to stdout.

#### Returns

- `list` - List of lines written to stdout.

### ExternalProgram().stdout_map_func

[[find in source code]](../../integraty/extprog.py#L1229)

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

### ExternalProgram().stdout_skip_lines

[[find in source code]](../../integraty/extprog.py#L528)

```python
def stdout_skip_lines(skip_head=0, skip_tail=0, pattern=None, exclude=False):
```

Skips some number of lines from the beginning, i.e. the head of the list
and/or from the end, i.e. the tail of the list of lines from stdout.
If a pattern results in some subset of original lines, this subset will
be subject to application of 'skip_head' and/or 'skip_tail'. In other
words, skipping of lines occurs after application of 'pattern' and
'exclude' parameters, not before.

#### Arguments

- `skip_head` *int, optional* - Number of lines to skip relative to beginning of data. Defaults to 0.
- `skip_tail` *int, optional* - Number of lines to skip relative to the end of the data. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines written to stdout.

### ExternalProgram().stdout_tail

[[find in source code]](../../integraty/extprog.py#L795)

```python
def stdout_tail(sep=None, pattern=None, exclude=False):
```

Select all but first column of each line from stdout, after splitting on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples with all but first element of each split line.

### ExternalProgram().stdout_take_column

[[find in source code]](../../integraty/extprog.py#L861)

```python
def stdout_take_column(sep=None, column=0, pattern=None, exclude=False):
```

Select a single column of each line from stdout, after splitting the
line on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `column` *int, optional* - Select column matching this index. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of elements extracted from each split line.

### ExternalProgram().stdout_take_range_columns

[[find in source code]](../../integraty/extprog.py#L937)

```python
def stdout_take_range_columns(
    sep=None,
    slc_range=(0, 1, 1),
    pattern=None,
    exclude=False,
):
```

Select multiple columns within the 'slc_range' range from each line
from stdout, after splitting the line on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `slc_range` *tuple, optional* - Range (start, end, stride). Defaults to (0, 1, 1).
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more columns from each split line.

### ExternalProgram().stdout_take_some_columns

[[find in source code]](../../integraty/extprog.py#L899)

```python
def stdout_take_some_columns(
    sep=None,
    selectors=(),
    pattern=None,
    exclude=False,
):
```

Select multiple columns from each line from stdout, after splitting the
line on 'sep'.

#### Arguments

- `sep` *str, optional* - Separator character. Defaults to None.
- `selectors` *tuple, optional* - Sequence of column indexes. Defaults to ().
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of tuples, where each tuple contains one or more columns from each split line.

### ExternalProgram().stdout_to_dict_func

[[find in source code]](../../integraty/extprog.py#L617)

```python
def stdout_to_dict_func(tuple_func, pattern=None, exclude=False):
```

Applies 'tuple_func' to each line from stdout, adding resulting tuple
to dict. It is expected that result from 'tuple_func' is a single
two-element tuple object, where first element becomes dict key and
second value for given key.

#### Arguments

- `tuple_func` *str* - Conversion function from string to two-element tuple.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - Dict made from tuples for each line over which 'tuple_func'
was applied.

### ExternalProgram().stdout_to_tuple_func

[[find in source code]](../../integraty/extprog.py#L582)

```python
def stdout_to_tuple_func(tuple_func, pattern=None, exclude=False):
```

Applies 'tuple_func' to each line from stdout, adding resulting tuple
to list. It is expected that result from 'tuple_func' is a single tuple
object.

#### Arguments

- `tuple_func` *str* - Conversion function from string to N-element tuple.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list(tuple)` - List of tuples for each line over which 'tuple_func'
was applied.

### ExternalProgram().stdout_trim_prefix

[[find in source code]](../../integraty/extprog.py#L1047)

```python
def stdout_trim_prefix(prefix, pattern=None, exclude=False):
```

Trim substring in 'prefix' from beginning of each line from stdout,
assuming substring is present.

#### Arguments

- `prefix` *str* - Prefix to trim from beginning of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with prefix trimmed from each.

### ExternalProgram().stdout_trim_suffix

[[find in source code]](../../integraty/extprog.py#L1077)

```python
def stdout_trim_suffix(suffix, pattern=None, exclude=False):
```

Trim substring in 'suffix' from end of each line from stdout,
assuming substring is present.

#### Arguments

- `suffix` *str* - Suffix to trim from end of each line.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines with suffix trimmed from each.

### ExternalProgram().stdout_with_prefix

[[find in source code]](../../integraty/extprog.py#L1107)

```python
def stdout_with_prefix(prefix, pattern=None, exclude=False):
```

Limits included lines from stdout to those matching given prefix.
If a pattern results in some subset of original lines, this subset
will be subject to application of 'prefix'. In other words, lines with
'prefix' may be excluded as a result of pattern matching, because
prefix checking occurs after application of 'pattern' and 'exclude'
parameters, not before.

#### Arguments

- `prefix` *str* - Lines with given prefix should be included.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given prefix.

### ExternalProgram().stdout_with_suffix

[[find in source code]](../../integraty/extprog.py#L1145)

```python
def stdout_with_suffix(suffix, pattern=None, exclude=False):
```

Limits included lines from stdout to those matching given suffix.
If a pattern results in some subset of original lines, this subset
will be subject to application of 'suffix'. In other words, lines with
'suffix' may be excluded as a result of pattern matching, because
suffix checking occurs after application of 'pattern' and 'exclude'
parameters, not before.

#### Arguments

- `suffix` *str* - Lines with given prefix should be included.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - Lines matching given suffix.

### ExternalProgram().terminate

[[find in source code]](../../integraty/extprog.py#L1472)

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

[[find in source code]](../../integraty/extprog.py#L1569)

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

[[find in source code]](../../integraty/extprog.py#L1586)

```python
def run(command, block=True, binary=False, timeout=None, cwd=None, env=None):
```

## stripper

[[find in source code]](../../integraty/extprog.py#L31)

```python
def stripper(w, chars):
```
