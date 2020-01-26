# -*- coding: utf-8 -*-

import itertools
import json
import os
import re
import subprocess
import shlex
import signal
import sys
import locale
import errno

from functools import reduce
from typing import Callable, Dict, List, TypeVar, Sequence, Sequence

from integraty.xstring import String

from pexpect.popen_spawn import PopenSpawn
import pexpect

pexpect.EOF.__module__ = "pexpect.exceptions"

# Include `unicode` in STR_TYPES for Python 2.X
try:
    STR_TYPES = (str, unicode)
except NameError:
    STR_TYPES = (str,)


class ExternalProgramException(Exception):
    pass


def pid_exists(pid):
    """Check whether pid exists in the current process table."""
    if pid == 0:
        # According to "man 2 kill" PID 0 has a special meaning:
        # it refers to <<every process in the process group of the
        # calling process>> so we don't want to go any further.
        # If we get here it means this UNIX platform *does* have
        # a process with id 0.
        return True
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH) therefore we should never get
            # here. If we do let's be explicit in considering this
            # an error.
            raise err
    else:
        return True


class ExternalProgram(object):
    """
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

    Try this out with `python3 -m doctest integraty/extprog.py` if you have
    sources checked out in a convenient place.
    """

    def __init__(self, cmd, timeout=None):
        super(ExternalProgram, self).__init__()
        self.cmd = cmd
        self.timeout = timeout
        self.subprocess = None
        self.blocking = None
        self.was_run = False
        self.__out = None
        self.__err = None

    def __repr__(self):
        return "ExternalProgram({!r}, timeout={})".format(
            self.cmd, self.timeout
        )

    def __enter__(self):
        return self

    # FIXME: Do something useful with exc_* args.
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.std_out.closed:
            self.std_out.close()
        if not self.std_err.closed:
            self.std_err.close()

    @property
    def _popen_args(self):
        return self.cmd

    @property
    def _default_popen_kwargs(self):
        return {
            "env": os.environ.copy(),
            "stdin": subprocess.PIPE,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "shell": True,
            "universal_newlines": True,
            "bufsize": 0,
        }

    @property
    def _default_pexpect_kwargs(self):
        encoding = "utf-8"
        if sys.platform == "win32":
            default_encoding = locale.getdefaultlocale()[1]
            if default_encoding is not None:
                encoding = default_encoding
        return {
            "env": os.environ.copy(),
            "encoding": encoding,
            "timeout": self.timeout,
        }

    @property
    def _uses_subprocess(self):
        return isinstance(self.subprocess, subprocess.Popen)

    @property
    def _uses_pexpect(self):
        return isinstance(self.subprocess, PopenSpawn)

    @property
    def std_out(self):
        return self.subprocess.stdout

    @property
    def ok(self):
        return self.return_code == 0

    @property
    def _pexpect_out(self):
        if self.subprocess.encoding:
            result = ""
        else:
            result = b""

        if self.subprocess.before:
            result += self.subprocess.before

        if self.subprocess.after and self.subprocess.after is not pexpect.EOF:
            result += self.subprocess.after

        result += self.subprocess.read()
        return result

    @property
    def out(self):
        """Std/out output (cached)"""
        if self.__out:
            return String(self.__out)

        if self._uses_subprocess:
            if not self.std_out.closed:
                self.__out = self.std_out.read()
                self.std_out.close()
        else:
            self.__out = self._pexpect_out

        return String(self.__out)

    @property
    def std_err(self):
        return self.subprocess.stderr

    @property
    def err(self):
        """Std/err output (cached)"""
        if self.__err:
            return String(self.__err)

        if self._uses_subprocess:
            if not self.std_err.closed:
                self.__err = self.std_err.read()
                self.std_err.close()
        else:
            self.__err = self._pexpect_out

        return String(self.__err)

    @property
    def pid(self):
        """The process' PID."""
        # Support for pexpect's functionality.
        if hasattr(self.subprocess, "proc"):
            return self.subprocess.proc.pid
        # Standard subprocess method.
        return self.subprocess.pid

    @property
    def is_alive(self):
        """Is the process alive?"""
        return pid_exists(self.pid)

    @property
    def return_code(self):
        # Support for pexpect's functionality.
        if self._uses_pexpect:
            return self.subprocess.exitstatus
        # Standard subprocess method.
        return self.subprocess.returncode

    @property
    def std_in(self):
        return self.subprocess.stdin

    def run(self, block=True, binary=False, cwd=None, env=None, shell=True):
        """Runs the given command, with or without pexpect functionality enabled."""
        self.blocking = block

        # Use subprocess.
        if self.blocking:
            popen_kwargs = self._default_popen_kwargs.copy()
            del popen_kwargs["stdin"]
            popen_kwargs["universal_newlines"] = not binary
            if cwd:
                popen_kwargs["cwd"] = cwd
            if env:
                popen_kwargs["env"].update(env)
            if not shell:
                popen_kwargs["shell"] = False
            s = subprocess.Popen(self._popen_args, **popen_kwargs)
        # Otherwise, use pexpect.
        else:
            pexpect_kwargs = self._default_pexpect_kwargs.copy()
            if binary:
                pexpect_kwargs["encoding"] = None
            if cwd:
                pexpect_kwargs["cwd"] = cwd
            if env:
                pexpect_kwargs["env"].update(env)
            # Enable Python subprocesses to work with expect functionality.
            pexpect_kwargs["env"]["PYTHONUNBUFFERED"] = "1"
            s = PopenSpawn(self._popen_args, **pexpect_kwargs)
        self.subprocess = s
        self.was_run = True

    def exec(self, env=None, shell=True):
        """ Runs the command and blocks (waits) until the command is complete. """
        if not shell and not isinstance(self._popen_args, list):
            raise ExternalProgramException(
                "With 'shell=False' command must be a sequence not a string"
            )
        self.run(env=env, shell=shell)
        self.block()

    def expect(self, pattern, timeout=-1):
        """Waits on the given pattern to appear in std_out"""

        if self.blocking:
            raise RuntimeError(
                "expect can only be used on non-blocking commands."
            )

        try:
            self.subprocess.expect(pattern=pattern, timeout=timeout)
        except pexpect.EOF:
            pass

    def send(self, s, end=os.linesep, signal=False):
        """Sends the given string or signal to std_in."""

        if self.blocking:
            raise RuntimeError(
                "send can only be used on non-blocking commands."
            )

        if not signal:
            if self._uses_subprocess:
                return self.subprocess.communicate(s + end)
            else:
                return self.subprocess.send(s + end)
        else:
            self.subprocess.send_signal(s)

    def terminate(self):
        self.subprocess.terminate()

    def kill(self):
        if self._uses_pexpect:
            self.subprocess.kill(signal.SIGINT)
        else:
            self.subprocess.send_signal(signal.SIGINT)

    def block(self):
        """Blocks until process is complete."""
        if self._uses_subprocess:
            # consume stdout and stderr
            if self.blocking:
                try:
                    stdout, stderr = self.subprocess.communicate(
                        timeout=self.timeout if self.timeout else None
                    )
                    self.__out = stdout
                    self.__err = stderr
                except ValueError:
                    pass  # Don't read from finished subprocesses.
            else:
                self.subprocess.stdin.close()
                self.std_out.close()
                self.std_err.close()
                # self.subprocess.wait(self.timeout if self.timeout else None)
                self.subprocess.wait()
        else:
            self.subprocess.sendeof()
            try:
                self.subprocess.wait()
            finally:
                if self.subprocess.proc.stdout:
                    self.subprocess.proc.stdout.close()

    def poll(self):
        if self._uses_subprocess:
            if self.blocking:
                if self.subprocess.poll() == 0:
                    return True
                return False
            return False
        else:
            raise ExternalProgramException("Do not combine poll() with expect")

    def pipe(self, command, timeout=None, cwd=None):
        """Runs the current command and passes its output to the next
        given process.
        """
        if not timeout:
            timeout = self.timeout

        if not self.was_run:
            self.run(block=False, cwd=cwd)

        data = self.out

        if timeout:
            c = ExternalProgram(command, timeout)
        else:
            c = ExternalProgram(command)

        c.run(block=False, cwd=cwd)
        if data:
            c.send(data)
        c.block()
        return c


def _expand_args(command):
    """Parses command strings and returns a Popen-ready list."""

    # Prepare arguments.
    if isinstance(command, STR_TYPES):
        if sys.version_info[0] == 2:
            splitter = shlex.shlex(command.encode("utf-8"))
        elif sys.version_info[0] == 3:
            splitter = shlex.shlex(command)
        else:
            splitter = shlex.shlex(command.encode("utf-8"))
        splitter.whitespace = "|"
        splitter.whitespace_split = True
        command = []

        while True:
            token = splitter.get_token()
            if token:
                command.append(token)
            else:
                break

        command = list(map(shlex.split, command))

    return command


def chain(command, timeout=None, cwd=None, env=None):
    commands = _expand_args(command)
    data = None

    for command in commands:

        c = run(command, block=False, timeout=timeout, cwd=cwd, env=env)

        if data:
            c.send(data, end="")
            c.subprocess.sendeof()

        data = c.out

    return c


def run(command, block=True, binary=False, timeout=None, cwd=None, env=None):
    c = ExternalProgram(command, timeout=timeout)
    c.run(block=block, binary=binary, cwd=cwd, env=env)

    if block:
        c.block()

    return c
