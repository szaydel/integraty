# Productivity

> Auto-generated documentation for [integraty.productivity](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py) module.

- [integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / [Integraty](index.md#integraty) / Productivity
    - [ChecksumBytesIO](#checksumbytesio)
        - [ChecksumBytesIO().md5](#checksumbytesiomd5)
        - [ChecksumBytesIO().sha1](#checksumbytesiosha1)
        - [ChecksumBytesIO().sha256](#checksumbytesiosha256)
    - [ChecksumFile](#checksumfile)
    - [ChecksumStream](#checksumstream)
        - [ChecksumStream().base64_dec](#checksumstreambase64_dec)
        - [ChecksumStream().base64_enc](#checksumstreambase64_enc)
        - [ChecksumStream().md5](#checksumstreammd5)
        - [ChecksumStream().sha1](#checksumstreamsha1)
        - [ChecksumStream().sha256](#checksumstreamsha256)
    - [ChecksumStringIO](#checksumstringio)
        - [ChecksumStringIO().md5](#checksumstringiomd5)
        - [ChecksumStringIO().sha1](#checksumstringiosha1)
        - [ChecksumStringIO().sha256](#checksumstringiosha256)
    - [RandomStrings](#randomstrings)
        - [RandomStrings().iter_string](#randomstringsiter_string)
        - [RandomStrings().string](#randomstringsstring)
    - [TemporaryFile](#temporaryfile)
        - [TemporaryFile().abspath](#temporaryfileabspath)
        - [TemporaryFile().content](#temporaryfilecontent)
        - [TemporaryFile().fp](#temporaryfilefp)
        - [TemporaryFile().md5](#temporaryfilemd5)
        - [TemporaryFile().read](#temporaryfileread)
        - [TemporaryFile().sha1](#temporaryfilesha1)
        - [TemporaryFile().sha256](#temporaryfilesha256)
        - [TemporaryFile().write](#temporaryfilewrite)

## ChecksumBytesIO

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L85)

```python
class ChecksumBytesIO():
    def __init__(stream: io.BytesIO):
```

### ChecksumBytesIO().md5

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L102)

```python
@property
def md5():
```

### ChecksumBytesIO().sha1

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L90)

```python
@property
def sha1():
```

### ChecksumBytesIO().sha256

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L96)

```python
@property
def sha256():
```

## ChecksumFile

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L215)

```python
class ChecksumFile(ChecksumStream):
    def __init__(path):
```

#### See also

- [ChecksumStream](#checksumstream)

## ChecksumStream

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L109)

```python
class ChecksumStream():
    def __init__(stream: io.IOBase):
```

### ChecksumStream().base64_dec

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L196)

```python
@property
def base64_dec():
```

Decode base64 encoded bytes from stream

#### Returns

- `bytes` - Decode contents as bytestring

### ChecksumStream().base64_enc

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L178)

```python
@property
def base64_enc():
```

Generate base64 encoded bytes for stream

#### Returns

- `bytes` - Encoded contents as bytestring

### ChecksumStream().md5

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L158)

```python
@property
def md5():
```

Generate MD5 checksum for stream

#### Returns

- `string` - Hexadecimal checksum value

### ChecksumStream().sha1

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L118)

```python
@property
def sha1():
```

Generate SHA1 checksum for stream

#### Returns

- `string` - Hexadecimal checksum value

### ChecksumStream().sha256

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L138)

```python
@property
def sha256():
```

Generate SHA256 checksum for stream

#### Returns

- `string` - Hexadecimal checksum value

## ChecksumStringIO

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L48)

```python
class ChecksumStringIO():
    def __init__(stream: io.StringIO):
```

### ChecksumStringIO().md5

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L74)

```python
@property
def md5():
```

### ChecksumStringIO().sha1

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L53)

```python
@property
def sha1():
```

### ChecksumStringIO().sha256

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L64)

```python
@property
def sha256():
```

## RandomStrings

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L13)

```python
class RandomStrings():
    def __init__(seed=None, urandom=False, include_digits=True):
```

### RandomStrings().iter_string

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L38)

```python
def iter_string(length=10, count=100):
```

### RandomStrings().string

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L32)

```python
def string(length=10):
```

## TemporaryFile

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L228)

```python
class TemporaryFile():
    def __init__(
        initial_content: bytes = None,
        virtual=False,
        suffix=None,
        prefix=None,
        dir=None,
        delete=True,
    ):
```

Temporary file with automatic deletion.

### TemporaryFile().abspath

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L263)

```python
@property
def abspath():
```

### TemporaryFile().content

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L301)

```python
@property
def content():
```

### TemporaryFile().fp

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L267)

```python
@property
def fp():
```

### TemporaryFile().md5

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L291)

```python
@property
def md5():
```

MD5 checksum of file content.

#### Returns

- `str` - Hexadecimal checksum string.

### TemporaryFile().read

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L257)

```python
def read(size=-1):
```

### TemporaryFile().sha1

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L271)

```python
@property
def sha1():
```

SHA1 checksum of file content.

#### Returns

- `str` - Hexadecimal checksum string.

### TemporaryFile().sha256

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L281)

```python
@property
def sha256():
```

SHA256 checksum of file content.

#### Returns

- `str` - Hexadecimal checksum string.

### TemporaryFile().write

[[find in source code]](https://github.com/szaydel/integraty/blob/master/integraty/productivity.py#L260)

```python
def write(b):
```
