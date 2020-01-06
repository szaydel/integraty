import json
import re
import sys

from unittest import TestCase
from unittest import main as run_integra_tests

from extprog import ExternalProgram

class NoCommandException(Exception):
    pass


class InvalidStream(Exception):
    pass


class IntegraTestCase(TestCase):
    def __init__(self, methodName="runTest"):
        super(IntegraTestCase, self).__init__(methodName)

    def assertCommandSucceeded(self, extprog: ExternalProgram=None, msg=None):
        msg = self._formatMessage(
            msg,
            f"Command '{extprog.cmd}' expected to return '0'; got {extprog.return_code}",
        )
        if extprog:
            if extprog.return_code: 
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")

    def assertNoStdout(self, extprog: ExternalProgram=None, msg=None):
        """Check that the last executed command produced nothing to stdout."""
        if extprog:
            if extprog.out:
                msg = self._formatMessage(
                    msg,
                    f"Command '{extprog.cmd}' expected no output; got:\n{extprog.out}",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")

    def assertNoStderr(self, extprog: ExternalProgram=None, msg=None):
        """Check that the last executed command produced nothing to stderr."""
        if extprog:
            if extprog.err:
                msg = self._formatMessage(
                    msg,
                    f"Command '{extprog.cmd}' expected no error output; got\n{extprog.err}",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")

    def assertStdOutEqual(self, extprog: ExternalProgram=None, second=None, msg=None):
        """Assert that output from last command and 'second' are equal."""
        return self.assertMultiLineEqual(extprog.out, second)

    def assertStdOutContains(self, extprog: ExternalProgram=None, substr=None, msg=None):
        """Assert that last command contains a given substring"""
        self.assertIsInstance(substr, str, "Parameter 'substr' is not a string")

        if extprog:
            if not re.search(substr, extprog.out):
                msg = self._formatMessage(
                    msg,
                    f"Output from command '{extprog.cmd}' does not contain '{substr}'",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("No previously called command found")


__all__ = ["IntegraTestCase"]
