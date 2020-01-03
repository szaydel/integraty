import json
import re
import sys

from unittest import TestCase
from unittest import main as run_integra_tests

from delegator import run, chain

PCHARS = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


def stripper(w, chars):
    if chars:
        return stripper(w.replace(chars[0], ""), chars[1:])
    else:
        return w


class NoCommandException(Exception):
    pass


class InvalidStream(Exception):
    pass


class IntegraTestCase(TestCase):
    def __init__(self, methodName="runTest"):
        self._cmd_results = {}
        self._cmd_results_list = []
        self._last_cmd = None
        self._chained = False
        super(IntegraTestCase, self).__init__(methodName)

    def shell(self, cmd=None, chained=False, alias=None):
        if cmd and not chained:
            self._last_cmd = cmd
            r = run(cmd)
            self._cmd_results_list.append(r)
            index = len(self._cmd_results_list) - 1
            self._cmd_results[alias if alias else cmd] = self._cmd_results_list[index]
            self._cmd_succeeded = r.ok
        elif cmd and chained:
            self._last_cmd = cmd
            self._cmd_results = chain(cmd)
        else:
            raise NoCommandException
        return r

    def cmd_results(self, key=None):
        if not key:
            return None
        if not key in self._cmd_results:
            raise KeyError
        return self._cmd_results[key]

    def _splitlines(self, key=None, stream="stdout"):
        if not key:
            return None
        if not key in self._cmd_results:
            raise KeyError
        if stream == "stdout":
            return [l.strip() for l in self._cmd_results[key].out.splitlines()]
        elif stream == "stderr":
            return [l.strip() for l in self._cmd_results[key].err.splitlines()]
        else:
            raise InvalidStream

    def _stdout_lines(self, key=None):
        return self._splitlines(key)

    def _stderr_lines(self, key=None):
        return self._splitlines(key, stream="stderr")

    def _list_of_lines(
        self, key=None, strip_punct=False, strip_chars=PCHARS, stream="stdout"
    ):
        if not key:
            return None
        if not key in self._cmd_results:
            raise KeyError
        lines = []
        if stream == "stdout":
            for l in self._cmd_results[key].out.split("\n"):
                tokens = l.split()
                if tokens:
                    if strip_punct:
                        tokens = tuple(stripper(tok, strip_chars) for tok in tokens)
                    lines.append(tokens)
        elif stream == "stderr":
            for l in self._cmd_results[key].err.split("\n"):
                tokens = l.split()
                if tokens:
                    if strip_punct:
                        tokens = [stripper(tok, strip_chars) for tok in tokens]
                    lines.append(tokens)
        else:
            raise InvalidStream
        return lines

    def _json_loads(self, key=None):
        d = {}
        try:
            d = json.loads(self._cmd_results[key].out)
        except json.JSONDecodeError:
            return None
        return d

    def json_loads(self, key=None):
        if not key:
            return None
        if not key in self._cmd_results:
            raise KeyError
        return self._json_loads(key)

    def stdout_lines_count(self, key=None, pattern=None, exclude=False):
        lines = self._stdout_lines(key)
        if not pattern:
            return lines.__len__()
        if exclude:
            return [l for l in lines if not re.search(pattern, l)].__len__()
        return [l for l in lines if re.search(pattern, l)].__len__()

    def stderr_lines_count(self, key=None, pattern=None, exclude=False):
        lines = self._stderr_lines(key)
        if not pattern:
            return lines.__len__()
        if exclude:
            return [l for l in lines if not re.search(pattern, l)].__len__()
        return [l for l in lines if re.search(pattern, l)].__len__()

    def stdout_lines_with_prefix(self, key=None, prefix=None, exclude=False):
        return self._lines_with_prefix(key, prefix, exclude)

    def stderr_lines_with_prefix(self, key=None, prefix=None, exclude=False):
        return self._lines_with_prefix(key, prefix, exclude, stream="stderr")

    def _lines_with_prefix(self, key=None, prefix=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines(key)
        elif stream == "stderr":
            lines = self._stderr_lines(key)
        else:
            raise InvalidStream
        if not prefix:
            return lines
        if exclude:
            return [l for l in lines if not l.startswith(prefix)]
        return [l for l in lines if l.startswith(prefix)]

    def _lines_with_suffix(self, key=None, suffix=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines(key)
        elif stream == "stderr":
            lines = self._stderr_lines(key)
        else:
            raise InvalidStream
        if not suffix:
            return lines
        if exclude:
            return [l for l in lines if not l.endswith(suffix)]
        return [l for l in lines if l.endswith(suffix)]

    def _lines_with_substr(self, key=None, substr=None, exclude=False, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines(key)
        elif stream == "stderr":
            lines = self._stderr_lines(key)
        else:
            raise InvalidStream
        if not substr:
            return lines
        if exclude:
            return [l for l in lines if l.find(substr) == -1]
        return [l for l in lines if l.find(substr) >= 0]

    def _lines_with_at_least_n_substr(
        self, key=None, substr=None, n=0, stream="stdout"
    ):
        if stream == "stdout":
            lines = self._stdout_lines(key)
        elif stream == "stderr":
            lines = self._stderr_lines(key)
        else:
            raise InvalidStream
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) >= n]

    def stdout_lines_with_at_least_n_substr(self, key=None, substr=None, n=0):
        return self._lines_with_at_least_n_substr(key, substr, n)

    def stderr_lines_with_at_least_n_substr(self, key=None, substr=None, n=0):
        return self._lines_with_at_least_n_substr(key, substr, n, stream="stderr")

    def _lines_with_at_most_n_substr(self, key=None, substr=None, n=0, stream="stdout"):
        if stream == "stdout":
            lines = self._stdout_lines(key)
        elif stream == "stderr":
            lines = self._stderr_lines(key)
        else:
            raise InvalidStream
        if not substr:
            return lines
        return [l for l in lines if l.count(substr) <= n]

    def stdout_lines_with_at_most_n_substr(self, key=None, substr=None, n=0):
        return self._lines_with_at_most_n_substr(key, substr, n)

    def stderr_lines_with_at_most_n_substr(self, key=None, substr=None, n=0):
        return self._lines_with_at_most_n_substr(key, substr, n, stream="stderr")

    def stdout_lines(self, key=None, pattern=None, exclude=False):
        lines = self._stdout_lines(key)
        if not pattern:
            return lines
        if exclude:
            return [l for l in lines if not re.search(pattern, l)]
        return [l for l in lines if re.search(pattern, l)]

    def stderr_lines(self, key=None, pattern=None, exclude=False):
        lines = self._stderr_lines(key)
        if not pattern:
            return lines
        if exclude:
            return [l for l in lines if not re.search(pattern, l)]
        return [l for l in lines if re.search(pattern, l)]

    def stdout_line_tuples(self, key=None, strip_punct=False, strip_chars=PCHARS):
        return self._list_of_lines(key, strip_punct, strip_chars, stream="stdout")

    def stderr_line_tuples(self, key=None, strip_punct=False, strip_chars=PCHARS):
        return self._list_of_lines(key, strip_punct, strip_chars, stream="stderr")

    def stdout_splitlines(self, key=None):
        return self._splitlines(key)

    def stderr_splitlines(self, key=None):
        return self._splitlines(key, stream="stderr")

    def assertAllCommandsAreOK(self, msg=None):
        """Check that the all previously executed command are OK."""
        for item in self._cmd_results_list:
            if not item.ok:
                msg = self._formatMessage(
                    msg,
                    f"Command '{item.cmd}' failed with exit code {item.return_code}\n{item.err}",
                )
                raise self.failureException(msg)

    def assertLastCommandIsOK(self, msg=None):
        """Check that the last executed command is OK."""
        if self._last_cmd:
            if not self._cmd_results[self._last_cmd].ok:
                msg = self._formatMessage(
                    msg,
                    f"Command '{self._last_cmd}' failed with exit code {self._cmd_results[self._last_cmd].return_code}\n{self._cmd_results[self._last_cmd].err}",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")

    def assertLastCommandNoStdout(self, msg=None):
        """Check that the last executed command produced nothing to stdout."""
        if self._last_cmd:
            if self._cmd_results[self._last_cmd].out:
                msg = self._formatMessage(
                    msg,
                    f"Command '{self._last_cmd}' expected no output; got {self._cmd_results[self._last_cmd].out}",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")

    def assertLastCommandNoStderr(self, msg=None):
        """Check that the last executed command produced nothing to stderr."""
        if self._last_cmd:
            if self._cmd_results[self._last_cmd].out:
                msg = self._formatMessage(
                    msg,
                    f"Command '{self._last_cmd}' expected no error output; got {self._cmd_results[self._last_cmd].err}",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")

    def assertLastCommandStdOutEqual(self, second, msg=None):
        """Assert that output from last command and 'second' are equal."""
        return self.assertMultiLineEqual(self._cmd_results[self._last_cmd].out, second)

    def assertLastCommandStdOutContains(self, substr, msg=None):
        """Assert that last command contains a given substring"""
        self.assertIsInstance(substr, str, "Text argument is not a string")

        if self._last_cmd:
            if not re.search(substr, self._cmd_results[self._last_cmd].out):
                msg = self._formatMessage(
                    msg,
                    f"Output from command '{self._last_cmd}' does not contain '{substr}'",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")


__all__ = ["IntegraTestCase"]
