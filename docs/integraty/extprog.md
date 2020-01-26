# Extprog

> Auto-generated documentation for [integraty.extprog](../../integraty/extprog.py) module.

- [Integraty](../README.md#integraty) / [Modules](../MODULES.md#integraty-modules) / `Integraty` / Extprog
    - [ExternalProgram](#externalprogram)
        - [ExternalProgram().block](#externalprogramblock)
        - [ExternalProgram().err](#externalprogramerr)
        - [ExternalProgram().exec](#externalprogramexec)
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
        - [ExternalProgram().terminate](#externalprogramterminate)
    - [ExternalProgramException](#externalprogramexception)
    - [chain](#chain)
    - [pid_exists](#pid_exists)
    - [run](#run)

## ExternalProgram

[[find in source code]](../../integraty/extprog.py#L63)

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
...     c.exec()
...     res = c.out.map_func(lambda l: dict(zip(('name', 'ttl', 'class','q_type', 'address'), l.split())), pattern='^microsoft.com')
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

[[find in source code]](../../integraty/extprog.py#L322)

```python
def block():
```

Blocks until process is complete.

### ExternalProgram().err

[[find in source code]](../../integraty/extprog.py#L203)

```python
@property
def err():
```

Std/err output (cached)

### ExternalProgram().exec

[[find in source code]](../../integraty/extprog.py#L275)

```python
def exec(env=None, shell=True):
```

Runs the command and blocks (waits) until the command is complete.

### ExternalProgram().expect

[[find in source code]](../../integraty/extprog.py#L284)

```python
def expect(pattern, timeout=-1):
```

Waits on the given pattern to appear in std_out

### ExternalProgram().is_alive

[[find in source code]](../../integraty/extprog.py#L227)

```python
@property
def is_alive():
```

Is the process alive?

### ExternalProgram().kill

[[find in source code]](../../integraty/extprog.py#L316)

```python
def kill():
```

### ExternalProgram().ok

[[find in source code]](../../integraty/extprog.py#L164)

```python
@property
def ok():
```

### ExternalProgram().out

[[find in source code]](../../integraty/extprog.py#L184)

```python
@property
def out():
```

Std/out output (cached)

### ExternalProgram().pid

[[find in source code]](../../integraty/extprog.py#L218)

```python
@property
def pid():
```

The process' PID.

### ExternalProgram().pipe

[[find in source code]](../../integraty/extprog.py#L359)

```python
def pipe(command, timeout=None, cwd=None):
```

Runs the current command and passes its output to the next
given process.

### ExternalProgram().poll

[[find in source code]](../../integraty/extprog.py#L349)

```python
def poll():
```

### ExternalProgram().return_code

[[find in source code]](../../integraty/extprog.py#L232)

```python
@property
def return_code():
```

### ExternalProgram().run

[[find in source code]](../../integraty/extprog.py#L244)

```python
def run(block=True, binary=False, cwd=None, env=None, shell=True):
```

Runs the given command, with or without pexpect functionality enabled.

### ExternalProgram().send

[[find in source code]](../../integraty/extprog.py#L297)

```python
def send(s, end=os.linesep, signal=False):
```

Sends the given string or signal to std_in.

### ExternalProgram().std_err

[[find in source code]](../../integraty/extprog.py#L199)

```python
@property
def std_err():
```

### ExternalProgram().std_in

[[find in source code]](../../integraty/extprog.py#L240)

```python
@property
def std_in():
```

### ExternalProgram().std_out

[[find in source code]](../../integraty/extprog.py#L160)

```python
@property
def std_out():
```

### ExternalProgram().terminate

[[find in source code]](../../integraty/extprog.py#L313)

```python
def terminate():
```

## ExternalProgramException

[[find in source code]](../../integraty/extprog.py#L31)

```python
class ExternalProgramException(Exception):
```

## chain

[[find in source code]](../../integraty/extprog.py#L410)

```python
def chain(command, timeout=None, cwd=None, env=None):
```

## pid_exists

[[find in source code]](../../integraty/extprog.py#L35)

```python
def pid_exists(pid):
```

Check whether pid exists in the current process table.

## run

[[find in source code]](../../integraty/extprog.py#L427)

```python
def run(command, block=True, binary=False, timeout=None, cwd=None, env=None):
```
