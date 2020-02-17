# Case

> Auto-generated documentation for [integraty.case](https://github.com/szaydel/integratyintegraty/case.py) module.

- [integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / [Integraty](index.md#integraty) / Case
    - [IntegraTestCase](#integratestcase)
        - [IntegraTestCase().assertCommandSucceeded](#integratestcaseassertcommandsucceeded)
        - [IntegraTestCase().assertDirExists](#integratestcaseassertdirexists)
        - [IntegraTestCase().assertDirModifiedAfter](#integratestcaseassertdirmodifiedafter)
        - [IntegraTestCase().assertFileMD5Equals](#integratestcaseassertfilemd5equals)
        - [IntegraTestCase().assertFileModifiedAfter](#integratestcaseassertfilemodifiedafter)
        - [IntegraTestCase().assertFileSHA1Equals](#integratestcaseassertfilesha1equals)
        - [IntegraTestCase().assertFileSHA256Equals](#integratestcaseassertfilesha256equals)
        - [IntegraTestCase().assertNoStderr](#integratestcaseassertnostderr)
        - [IntegraTestCase().assertNoStdout](#integratestcaseassertnostdout)
        - [IntegraTestCase().assertPathDoesNotExist](#integratestcaseassertpathdoesnotexist)
        - [IntegraTestCase().assertRegFileExists](#integratestcaseassertregfileexists)
        - [IntegraTestCase().assertStdErrContains](#integratestcaseassertstderrcontains)
        - [IntegraTestCase().assertStdErrEqual](#integratestcaseassertstderrequal)
        - [IntegraTestCase().assertStdOutContains](#integratestcaseassertstdoutcontains)
        - [IntegraTestCase().assertStdOutEqual](#integratestcaseassertstdoutequal)
        - [IntegraTestCase().assertStdoutIsJSONArray](#integratestcaseassertstdoutisjsonarray)
        - [IntegraTestCase().assertStringsAlmostEqual](#integratestcaseassertstringsalmostequal)
        - [IntegraTestCase().assertStringsAlmostEqualCosine](#integratestcaseassertstringsalmostequalcosine)
        - [IntegraTestCase().assertStringsAlmostEqualDiffLib](#integratestcaseassertstringsalmostequaldifflib)
        - [IntegraTestCase().get_class_var](#integratestcaseget_class_var)

## IntegraTestCase

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L93)

```python
class IntegraTestCase(TestCase):
    def __init__(methodName='runTest'):
```

### IntegraTestCase().assertCommandSucceeded

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L120)

```python
def assertCommandSucceeded(extprog: ExternalProgram = None, msg=None):
```

Assert that the executed command ran successfully.

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertDirExists

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L313)

```python
def assertDirExists(path, msg=None):
```

Assert that given path is an existing directory.

### IntegraTestCase().assertDirModifiedAfter

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L344)

```python
def assertDirModifiedAfter(path, timestamp: float, msg=None):
```

Assert that given directory path is more recent than timestamp.

### IntegraTestCase().assertFileMD5Equals

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L378)

```python
def assertFileMD5Equals(path, checksum: str, msg=None):
```

Assert that MD5 checksum is correct.

### IntegraTestCase().assertFileModifiedAfter

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L330)

```python
def assertFileModifiedAfter(path, timestamp: float, msg=None):
```

Assert that given file path is more recent than timestamp.

### IntegraTestCase().assertFileSHA1Equals

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L358)

```python
def assertFileSHA1Equals(path, checksum: str, msg=None):
```

Assert that SHA1 checksum is correct.

### IntegraTestCase().assertFileSHA256Equals

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L368)

```python
def assertFileSHA256Equals(path, checksum: str, msg=None):
```

Assert that SHA256 checksum is correct.

### IntegraTestCase().assertNoStderr

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L146)

```python
def assertNoStderr(extprog: ExternalProgram = None, msg=None):
```

Assert that the executed command produced nothing to stderr.

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertNoStdout

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L134)

```python
def assertNoStdout(extprog: ExternalProgram = None, msg=None):
```

Assert that the executed command produced nothing to stdout.

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertPathDoesNotExist

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L304)

```python
def assertPathDoesNotExist(path, msg=None):
```

Assert that given path does not exist.

### IntegraTestCase().assertRegFileExists

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L287)

```python
def assertRegFileExists(path, msg=None):
```

Assert that given path is an existing regular file.

### IntegraTestCase().assertStdErrContains

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L190)

```python
def assertStdErrContains(
    extprog: ExternalProgram = None,
    substr=None,
    msg=None,
):
```

Assert that stderr from command contains a given substring

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertStdErrEqual

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L165)

```python
def assertStdErrEqual(extprog: ExternalProgram = None, second=None, msg=None):
```

Assert that stderr from command and 'second' are equal.

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertStdOutContains

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L172)

```python
def assertStdOutContains(
    extprog: ExternalProgram = None,
    substr=None,
    msg=None,
):
```

Assert that stdout from command contains a given substring

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertStdOutEqual

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L158)

```python
def assertStdOutEqual(extprog: ExternalProgram = None, second=None, msg=None):
```

Assert that stdout from command and 'second' are equal.

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertStdoutIsJSONArray

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L208)

```python
def assertStdoutIsJSONArray(extprog: ExternalProgram = None, msg=None):
```

Assert that stdout from command contains JSON Array

#### See also

- [ExternalProgram](extprog.md#externalprogram)

### IntegraTestCase().assertStringsAlmostEqual

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L233)

```python
def assertStringsAlmostEqual(
    str1,
    str2,
    ratio: float = 0.8,
    max_distance: int = None,
    msg=None,
):
```

Assert that two strings are similar enough; by default 80% in common using Levenshtein Distance

### IntegraTestCase().assertStringsAlmostEqualCosine

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L271)

```python
def assertStringsAlmostEqualCosine(str1, str2, ratio: float = 0.8, msg=None):
```

Assert that two strings are similar enough; by default 80% in common using Cosine Similarity

### IntegraTestCase().assertStringsAlmostEqualDiffLib

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L256)

```python
def assertStringsAlmostEqualDiffLib(str1, str2, ratio: float = 0.8, msg=None):
```

Assert that two strings are similar enough; by default 80% in common using Difflib SequenceMatcher

### IntegraTestCase().get_class_var

[[find in source code]](https://github.com/szaydel/integratyintegraty/case.py#L107)

```python
def get_class_var(name):
```

Access class variables by their name without explicitly referring to
name of class. This is really just a convenience method.

#### Arguments

- `name` *str* - Name of class variable to lookup.

#### Returns

- `any` - Value of the class variable.
