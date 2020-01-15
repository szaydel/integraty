# Extprog

> Auto-generated documentation for [integraty.extprog](../../integraty/extprog.py) module.

- [Integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / `Integraty` / Extprog
    - [ExternalProgram](#externalprogram)
        - [ExternalProgram().block](#externalprogramblock)
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
        - [ExternalProgram().run_wait](#externalprogramrun_wait)
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
        - [ExternalProgram().stderr_filtered_lines](#externalprogramstderr_filtered_lines)
        - [ExternalProgram().stderr_firstn](#externalprogramstderr_firstn)
        - [ExternalProgram().stderr_head](#externalprogramstderr_head)
        - [ExternalProgram().stderr_json_loads](#externalprogramstderr_json_loads)
        - [ExternalProgram().stderr_lastn](#externalprogramstderr_lastn)
        - [ExternalProgram().stderr_line_tuples](#externalprogramstderr_line_tuples)
        - [ExternalProgram().stderr_lines](#externalprogramstderr_lines)
        - [ExternalProgram().stderr_map_func](#externalprogramstderr_map_func)
        - [ExternalProgram().stderr_tail](#externalprogramstderr_tail)
        - [ExternalProgram().stderr_take_column](#externalprogramstderr_take_column)
        - [ExternalProgram().stderr_take_range_columns](#externalprogramstderr_take_range_columns)
        - [ExternalProgram().stderr_take_some_columns](#externalprogramstderr_take_some_columns)
        - [ExternalProgram().stderr_to_dict_map_func](#externalprogramstderr_to_dict_map_func)
        - [ExternalProgram().stderr_trim_prefix](#externalprogramstderr_trim_prefix)
        - [ExternalProgram().stderr_trim_suffix](#externalprogramstderr_trim_suffix)
        - [ExternalProgram().stderr_tuple_transform_func](#externalprogramstderr_tuple_transform_func)
        - [ExternalProgram().stderr_with_prefix](#externalprogramstderr_with_prefix)
        - [ExternalProgram().stderr_with_suffix](#externalprogramstderr_with_suffix)
        - [ExternalProgram().stdout_at_least_n_substr](#externalprogramstdout_at_least_n_substr)
        - [ExternalProgram().stdout_at_most_n_substr](#externalprogramstdout_at_most_n_substr)
        - [ExternalProgram().stdout_columns](#externalprogramstdout_columns)
        - [ExternalProgram().stdout_count](#externalprogramstdout_count)
        - [ExternalProgram().stdout_dict_from_line](#externalprogramstdout_dict_from_line)
        - [ExternalProgram().stdout_filter_func](#externalprogramstdout_filter_func)
        - [ExternalProgram().stdout_filtered_lines](#externalprogramstdout_filtered_lines)
        - [ExternalProgram().stdout_firstn](#externalprogramstdout_firstn)
        - [ExternalProgram().stdout_head](#externalprogramstdout_head)
        - [ExternalProgram().stdout_json_loads](#externalprogramstdout_json_loads)
        - [ExternalProgram().stdout_lastn](#externalprogramstdout_lastn)
        - [ExternalProgram().stdout_line_tuples](#externalprogramstdout_line_tuples)
        - [ExternalProgram().stdout_lines](#externalprogramstdout_lines)
        - [ExternalProgram().stdout_map_func](#externalprogramstdout_map_func)
        - [ExternalProgram().stdout_tail](#externalprogramstdout_tail)
        - [ExternalProgram().stdout_take_column](#externalprogramstdout_take_column)
        - [ExternalProgram().stdout_take_range_columns](#externalprogramstdout_take_range_columns)
        - [ExternalProgram().stdout_take_some_columns](#externalprogramstdout_take_some_columns)
        - [ExternalProgram().stdout_to_dict_map_func](#externalprogramstdout_to_dict_map_func)
        - [ExternalProgram().stdout_trim_prefix](#externalprogramstdout_trim_prefix)
        - [ExternalProgram().stdout_trim_suffix](#externalprogramstdout_trim_suffix)
        - [ExternalProgram().stdout_tuple_transform_func](#externalprogramstdout_tuple_transform_func)
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

[[find in source code]](../../integraty/extprog.py#L75)

```python
class ExternalProgram(object):
    def __init__(cmd, timeout=None):
```

### ExternalProgram().block

[[find in source code]](../../integraty/extprog.py#L1345)

```python
def block():
```

Blocks until process is complete.

### ExternalProgram().err

[[find in source code]](../../integraty/extprog.py#L1230)

```python
@property
def err():
```

Std/err output (cached)

### ExternalProgram().expect

[[find in source code]](../../integraty/extprog.py#L1311)

```python
def expect(pattern, timeout=-1):
```

Waits on the given pattern to appear in std_out

### ExternalProgram().is_alive

[[find in source code]](../../integraty/extprog.py#L1254)

```python
@property
def is_alive():
```

Is the process alive?

### ExternalProgram().kill

[[find in source code]](../../integraty/extprog.py#L1339)

```python
def kill():
```

### ExternalProgram().ok

[[find in source code]](../../integraty/extprog.py#L1191)

```python
@property
def ok():
```

### ExternalProgram().out

[[find in source code]](../../integraty/extprog.py#L1211)

```python
@property
def out():
```

Std/out output (cached)

### ExternalProgram().pid

[[find in source code]](../../integraty/extprog.py#L1245)

```python
@property
def pid():
```

The process' PID.

### ExternalProgram().pipe

[[find in source code]](../../integraty/extprog.py#L1382)

```python
def pipe(command, timeout=None, cwd=None):
```

Runs the current command and passes its output to the next
given process.

### ExternalProgram().poll

[[find in source code]](../../integraty/extprog.py#L1372)

```python
def poll():
```

### ExternalProgram().return_code

[[find in source code]](../../integraty/extprog.py#L1259)

```python
@property
def return_code():
```

### ExternalProgram().run

[[find in source code]](../../integraty/extprog.py#L1271)

```python
def run(block=True, binary=False, cwd=None, env=None, shell=True):
```

Runs the given command, with or without pexpect functionality enabled.

### ExternalProgram().run_wait

[[find in source code]](../../integraty/extprog.py#L1302)

```python
def run_wait(env=None, shell=True):
```

Runs the command and blocks (waits) until the command is complete.

### ExternalProgram().send

[[find in source code]](../../integraty/extprog.py#L1322)

```python
def send(s, end=os.linesep, signal=False):
```

Sends the given string or signal to std_in.

### ExternalProgram().std_err

[[find in source code]](../../integraty/extprog.py#L1226)

```python
@property
def std_err():
```

### ExternalProgram().std_in

[[find in source code]](../../integraty/extprog.py#L1267)

```python
@property
def std_in():
```

### ExternalProgram().std_out

[[find in source code]](../../integraty/extprog.py#L1187)

```python
@property
def std_out():
```

### ExternalProgram().stderr_at_least_n_substr

[[find in source code]](../../integraty/extprog.py#L1164)

```python
def stderr_at_least_n_substr(substr=None, n=0):
```

### ExternalProgram().stderr_at_most_n_substr

[[find in source code]](../../integraty/extprog.py#L1170)

```python
def stderr_at_most_n_substr(substr=None, n=0):
```

### ExternalProgram().stderr_columns

[[find in source code]](../../integraty/extprog.py#L892)

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

[[find in source code]](../../integraty/extprog.py#L559)

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

[[find in source code]](../../integraty/extprog.py#L737)

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

[[find in source code]](../../integraty/extprog.py#L1176)

```python
def stderr_filter_func(func):
```

### ExternalProgram().stderr_filtered_lines

[[find in source code]](../../integraty/extprog.py#L604)

```python
def stderr_filtered_lines(
    skip_head=0,
    skip_tail=0,
    pattern=None,
    exclude=False,
):
```

Stderr text produced by the program.

#### Arguments

- `skip_head` *int, optional* - Number of lines to skip relative to beginning of data. Defaults to 0.
- `skip_tail` *int, optional* - Number of lines to skip relative to the end of the data. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines written to stderr.

### ExternalProgram().stderr_firstn

[[find in source code]](../../integraty/extprog.py#L775)

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

### ExternalProgram().stderr_head

[[find in source code]](../../integraty/extprog.py#L831)

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

[[find in source code]](../../integraty/extprog.py#L531)

```python
@property
def stderr_json_loads():
```

Deserialized to native a native datatype JSON data written to stderr.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### ExternalProgram().stderr_lastn

[[find in source code]](../../integraty/extprog.py#L803)

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

[[find in source code]](../../integraty/extprog.py#L1043)

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

[[find in source code]](../../integraty/extprog.py#L1079)

```python
@property
def stderr_lines():
```

Unfiltered lines written to stderr.

#### Returns

- `list` - List of lines.

### ExternalProgram().stderr_map_func

[[find in source code]](../../integraty/extprog.py#L1182)

```python
def stderr_map_func(func):
```

### ExternalProgram().stderr_tail

[[find in source code]](../../integraty/extprog.py#L859)

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

[[find in source code]](../../integraty/extprog.py#L927)

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

[[find in source code]](../../integraty/extprog.py#L999)

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

[[find in source code]](../../integraty/extprog.py#L961)

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

### ExternalProgram().stderr_to_dict_map_func

[[find in source code]](../../integraty/extprog.py#L690)

```python
def stderr_to_dict_map_func(
    tuple_func,
    sep=None,
    pattern=None,
    exclude=False,
):
```

Applies 'tuple_func' to each line from stdout, adding resulting tuple
to dict. It is expected that result from 'tuple_func' is a single
two-element tuple object, where first element becomes dict key and
second value for given key.

#### Arguments

- `tuple_func` *str* - Conversion function from string to two-element tuple.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - Dict made from tuples for each line over which 'tuple_func'
was applied.

### ExternalProgram().stderr_trim_prefix

[[find in source code]](../../integraty/extprog.py#L1104)

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

[[find in source code]](../../integraty/extprog.py#L1134)

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

### ExternalProgram().stderr_tuple_transform_func

[[find in source code]](../../integraty/extprog.py#L649)

```python
def stderr_tuple_transform_func(
    tuple_func,
    sep=None,
    pattern=None,
    exclude=False,
):
```

Applies 'tuple_func' over each line, adding resulting tuple to list.
It is expected that result from 'tuple_func' is a single tuple object.

#### Arguments

- `tuple_func` *str* - Conversion function from string to two-element tuple.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list(tuple)` - List of tuples for each line over which 'tuple_func' was applied.

### ExternalProgram().stderr_with_prefix

[[find in source code]](../../integraty/extprog.py#L1152)

```python
def stderr_with_prefix(prefix, exclude=False):
```

### ExternalProgram().stderr_with_suffix

[[find in source code]](../../integraty/extprog.py#L1158)

```python
def stderr_with_suffix(suffix=None, exclude=False):
```

### ExternalProgram().stdout_at_least_n_substr

[[find in source code]](../../integraty/extprog.py#L1161)

```python
def stdout_at_least_n_substr(substr=None, n=0):
```

### ExternalProgram().stdout_at_most_n_substr

[[find in source code]](../../integraty/extprog.py#L1167)

```python
def stdout_at_most_n_substr(substr=None, n=0):
```

### ExternalProgram().stdout_columns

[[find in source code]](../../integraty/extprog.py#L873)

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

[[find in source code]](../../integraty/extprog.py#L541)

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

[[find in source code]](../../integraty/extprog.py#L713)

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

[[find in source code]](../../integraty/extprog.py#L1173)

```python
def stdout_filter_func(func):
```

### ExternalProgram().stdout_filtered_lines

[[find in source code]](../../integraty/extprog.py#L577)

```python
def stdout_filtered_lines(
    skip_head=0,
    skip_tail=0,
    pattern=None,
    exclude=False,
):
```

Stdout text produced by the program.

#### Arguments

- `skip_head` *int, optional* - Number of lines to skip relative to beginning of data. Defaults to 0.
- `skip_tail` *int, optional* - Number of lines to skip relative to the end of the data. Defaults to 0.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list` - List of lines written to stdout.

### ExternalProgram().stdout_firstn

[[find in source code]](../../integraty/extprog.py#L761)

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

### ExternalProgram().stdout_head

[[find in source code]](../../integraty/extprog.py#L817)

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

[[find in source code]](../../integraty/extprog.py#L521)

```python
@property
def stdout_json_loads():
```

Deserialized to native a native datatype JSON data written to stdout.

#### Returns

bool, int, string, dict, list: Unmarshaled JSON data.

### ExternalProgram().stdout_lastn

[[find in source code]](../../integraty/extprog.py#L789)

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

[[find in source code]](../../integraty/extprog.py#L1019)

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

[[find in source code]](../../integraty/extprog.py#L1069)

```python
@property
def stdout_lines():
```

Unfiltered lines written to stdout.

#### Returns

- `list` - List of lines.

### ExternalProgram().stdout_map_func

[[find in source code]](../../integraty/extprog.py#L1179)

```python
def stdout_map_func(func):
```

### ExternalProgram().stdout_tail

[[find in source code]](../../integraty/extprog.py#L845)

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

[[find in source code]](../../integraty/extprog.py#L911)

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

[[find in source code]](../../integraty/extprog.py#L981)

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

[[find in source code]](../../integraty/extprog.py#L943)

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

### ExternalProgram().stdout_to_dict_map_func

[[find in source code]](../../integraty/extprog.py#L669)

```python
def stdout_to_dict_map_func(
    tuple_func,
    sep=None,
    pattern=None,
    exclude=False,
):
```

Applies 'tuple_func' to each line from stdout, adding resulting tuple
to dict. It is expected that result from 'tuple_func' is a single
two-element tuple object, where first element becomes dict key and
second value for given key.

#### Arguments

- `tuple_func` *str* - Conversion function from string to two-element tuple.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `dict` - Dict made from tuples for each line over which 'tuple_func'
was applied.

### ExternalProgram().stdout_trim_prefix

[[find in source code]](../../integraty/extprog.py#L1089)

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

[[find in source code]](../../integraty/extprog.py#L1119)

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

### ExternalProgram().stdout_tuple_transform_func

[[find in source code]](../../integraty/extprog.py#L631)

```python
def stdout_tuple_transform_func(
    tuple_func,
    sep=None,
    pattern=None,
    exclude=False,
):
```

Applies 'tuple_func' over each line, adding resulting tuple to list.

#### Arguments

- `tuple_func` *str* - Conversion function from string to two-element tuple.
- `sep` *str, optional* - Separator character. Defaults to None.
- `pattern` *str, optional* - Select lines matching pattern. Defaults to None.
- `exclude` *bool, optional* - Invert pattern matching. Defaults to False.

#### Returns

- `list(tuple)` - List of tuples for each line over which 'tuple_func'
was applied.

### ExternalProgram().stdout_with_prefix

[[find in source code]](../../integraty/extprog.py#L1149)

```python
def stdout_with_prefix(prefix, exclude=False):
```

### ExternalProgram().stdout_with_suffix

[[find in source code]](../../integraty/extprog.py#L1155)

```python
def stdout_with_suffix(suffix=None, exclude=False):
```

### ExternalProgram().terminate

[[find in source code]](../../integraty/extprog.py#L1336)

```python
def terminate():
```

## ExternalProgramException

[[find in source code]](../../integraty/extprog.py#L43)

```python
class ExternalProgramException(Exception):
```

## InvalidStream

[[find in source code]](../../integraty/extprog.py#L39)

```python
class InvalidStream(Exception):
```

## NoCommandException

[[find in source code]](../../integraty/extprog.py#L35)

```python
class NoCommandException(Exception):
```

## chain

[[find in source code]](../../integraty/extprog.py#L1433)

```python
def chain(command, timeout=None, cwd=None, env=None):
```

## pid_exists

[[find in source code]](../../integraty/extprog.py#L47)

```python
def pid_exists(pid):
```

Check whether pid exists in the current process table.

## run

[[find in source code]](../../integraty/extprog.py#L1450)

```python
def run(command, block=True, binary=False, timeout=None, cwd=None, env=None):
```

## stripper

[[find in source code]](../../integraty/extprog.py#L28)

```python
def stripper(w, chars):
```
