# integraty

> Auto-generated documentation index.

[![Build Status](https://travis-ci.org/szaydel/integraty.svg?branch=master)](https://travis-ci.org/szaydel/integraty)
[![CircleCI](https://circleci.com/gh/szaydel/integraty.svg?style=svg)](https://circleci.com/gh/szaydel/integraty)

Full integraty project documentation can be found in [Modules](MODULES.md#integraty-modules)

- [integraty](#integraty)
  - [integraty Modules](MODULES.md#integraty-modules)

An experimental integration testing framework, or perhaps building blocks for one. Don't use this unless you are ready for a lot of pain. :)

The main goal of this library is to provide just enough tooling to make integration testing a little less painful. Integration testing is normally the domain of shell scripts and tools like `awk`, `sed`, `grep`, `cut`, etc., etc. However, there are a number of problems with this traditional approach which tend to lead to tests which are difficult to maintain and often are hard to read and follow.

Without any doubt gluing commands together with pipes is an extremely powerful mechanism, which makes the shell amazingly flexible and infinitely extensible. But these very same attributes also make it difficult to write very standard looking code, which can be maintained by multiple people over long time intervals. This library aims to build on top of excellent tools already part of Python distribution and additionally makes possible to take advantage of the amazing `pytest` package. While `pytest` is actually optional, it is a very solid and mature package which could be used for anything from unit tests to functional and integration tests.

This library is actually a combination of a few loosely coupled components. Its aim is to reduce information and transform output from programs in the same way that would typically be done with filtering tools like `grep` and `awk`, etc., but instead do it with the Python, while also transforming reduced data into structures which are pleasant to work with. It is no secret that shell's strength is not its rich data structures. Conversely Python excels at data manipulation extraction and transformation. It is fast-becoming the lingua franca of data science, field rich with data and demanding flexibility, expressiveness and maintainability of code. Python is low-boilerplate, and scores highly in the readability test. My hope is to capture these strengths and substitute shell's weaknesses without losing very much of what makes using shell the defacto standard for integration testing on *nix* systems.

The following are high-level goals of the library:
- Make it as easy and as pleasant as possible to execute commands and collect their `stdout` and `stderr`
- With little boilerplate go from unstructured or loosely structured output most command line tools emit to Python data structures
- Provide convenience mechanisms which we frequently look for when we write tests, such as generating random strings, or dealing with various temporary files or directories, etc.
- Extend Python's wonderful, though unit test biased `unittest` module with additional assertions to make command line application testing more pleasant
- Extend the string type with a bunch of convenience methods to make it easy and convenient to go from a blob of text to native data structures such as tuples, dicts, ordered dicts, sets or custom defined types like classes, functions, etc.

There are several examples of how the library was intended to be used in the `tests` directory. It is a good place to start.

Here are a few basic Hello World of sorts examples for how the library is meant to be used. In this case we assert that a system must have a few IP addresses, some IPv4 and some IPv6, and we do some selections, comparisons and print(s) just to make some things a little more concrete. This is probably a fragile set of tests in real life, and meant to be illustrative more than realistic.

```
>>> from integraty.extprog import ExternalProgram

>>> expect = {'fe80::1%lo0', '192.168.66.1', '127.0.0.1', 'fe80::14ba:d08b:d6b9:ef33%en0', 'fe80::24d0:7bff:fec0:d43a%awdl0', '192.168.99.1', '10.11.3.1', 
... '192.168.1.194', 'fe80::2bee:6736:163:9ffa%utun0', '::1'}

>>> with ExternalProgram('ifconfig') as c:
...     c.exec() 
...     lines = c.out.fields(pattern='inet')
...     assert set(lines[1]).difference(expect) == set()

>>> with ExternalProgram('ifconfig') as c: 
...     c.exec() 
...     lines = c.out.take_column(column=1, pattern='ether')
...     assert '6a:00:01:92:1b:a1' in lines
...     assert '6a:00:01:92:1b:a0' in lines
...     assert len(lines) == 9

>>> with ExternalProgram('ifconfig') as c:
...     c.exec()
...     lines = c.out.pairs(pattern='inet')
...     print([dict(i) for i in lines])

[{'inet': '127.0.0.1', 'netmask': '0xff000000'}, {'inet6': '::1', 'prefixlen': '128'}, {'inet6': 'fe80::1%lo0', 'prefixlen': '64', 'scopeid': '0x1'}, {'ine
t6': 'fe80::14ba:d08b:d6b9:ef33%en0', 'prefixlen': '64', 'secured': 'scopeid'}, {'inet': '192.168.1.194', 'netmask': '0xfffffc00', 'broadcast': '192.168.3.
255'}, {'inet6': 'fe80::24d0:7bff:fec0:d43a%awdl0', 'prefixlen': '64', 'scopeid': '0xa'}, {'inet6': 'fe80::2bee:6736:163:9ffa%utun0', 'prefixlen': '64', 'scopeid': '0xb'}, {'inet': '192.168.99.1', 'netmask': '0xffffff00', 'broadcast': '192.168.99.255'}, {'inet': '10.11.3.1', 'netmask': '0xffffff00', 'broadcast': '10.11.3.255'}, {'inet': '192.168.66.1', 'netmask': '0xffffff00', 'broadcast': '192.168.66.255'}]

>>> with ExternalProgram('ifconfig') as c:
...     c.exec()
...     lines = c.out.fold_funcs(lambda l: l.split()[:2], lambda l: None if not 'inet' in l else l[1], pattern='inet') 
...     assert '192.168.99.1' in lines
...     print([l for l in lines if l])

['127.0.0.1', '192.168.1.194', '192.168.99.1', '10.11.3.1', '192.168.66.1']

>>> with ExternalProgram('ifconfig') as c:
...     c.exec()
...     lines = c.out.head(pattern='RUNNING', sub_pattern=':', replacement='')
...     assert set(lines).difference({'vboxnet1', 'p2p0', 'en2', 'vboxnet0', 'vboxnet2', 'bridge0', 'en1', 'en0', 'utun0', 'lo0', 'awdl0'}) == set()

```

The library does not attempt to dictate a particular style of testing, but assertion-style is sort of assumed. It is certainly possible to use tools such as `diff`, and `difflib`, etc. The intent of the library is to make explicit comparisons easier, fundamentally.
