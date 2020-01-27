# -*- coding: utf-8 -*-

import json
import logging
import os
import re
import stat
import sys

from unittest import TestCase
from unittest import main as run_integra_tests

from integraty.extprog import ExternalProgram
from integraty.productivity import ChecksumFile


class NoCommandException(Exception):
    pass


class InvalidStream(Exception):
    pass


class IntegraTestCase(TestCase):

    def __init__(self, methodName="runTest"):
        logger = logging.getLogger("IntegraTestCase")
        logger.setLevel(logging.DEBUG)
        hndlr = logging.StreamHandler(sys.stderr)
        hndlr.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "|%(levelname)s|\t%(funcName)s[%(lineno)d]: %(message)s")
        hndlr.setFormatter(formatter)
        logger.addHandler(hndlr)
        self.log = logger
        super(IntegraTestCase, self).__init__(methodName)

    def get_class_var(self, name):
        """
        Access class variables by their name without explicitly referring to
        name of class. This is really just a convenience method.
        
        Args:
            name (str): Name of class variable to lookup.
        
        Returns:
            any: Value of the class variable.
        """
        return self.__class__.__getattribute__(self, name)

    def assertCommandSucceeded(self, extprog: ExternalProgram = None, msg=None):
        """Assert that the executed command ran successfully."""
        msg = self._formatMessage(
            msg,
            f"Command '{extprog.cmd}' expected to return '0'; got {extprog.return_code}",
        )
        if extprog:
            if extprog.return_code:
                raise self.failureException(msg)
        else:
            raise NoCommandException("ExternalProgram cannot be None")

    def assertNoStdout(self, extprog: ExternalProgram = None, msg=None):
        """Assert that the executed command produced nothing to stdout."""
        if extprog:
            if extprog.out:
                msg = self._formatMessage(
                    msg,
                    f"Command '{extprog.cmd}' expected no output; got:\n{extprog.out}",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("ExternalProgram cannot be None")

    def assertNoStderr(self, extprog: ExternalProgram = None, msg=None):
        """Assert that the executed command produced nothing to stderr."""
        if extprog:
            if extprog.err:
                msg = self._formatMessage(
                    msg,
                    f"Command '{extprog.cmd}' expected no error output; got\n{extprog.err}",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("ExternalProgram cannot be None")

    def assertStdOutEqual(self,
                          extprog: ExternalProgram = None,
                          second=None,
                          msg=None):
        """Assert that stdout from command and 'second' are equal."""
        return self.assertMultiLineEqual(extprog.out, second)

    def assertStdErrEqual(self,
                          extprog: ExternalProgram = None,
                          second=None,
                          msg=None):
        """Assert that stderr from command and 'second' are equal."""
        return self.assertMultiLineEqual(extprog.err, second)

    def assertStdOutContains(self,
                             extprog: ExternalProgram = None,
                             substr=None,
                             msg=None):
        """Assert that stdout from command contains a given substring"""
        self.assertIsInstance(substr, str, "Parameter 'substr' is not a string")

        if extprog:
            if not re.search(substr, extprog.out):
                msg = self._formatMessage(
                    msg,
                    f"Output from command '{extprog.cmd}' does not contain '{substr}'",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("ExternalProgram cannot be None")

    def assertStdErrContains(self,
                             extprog: ExternalProgram = None,
                             substr=None,
                             msg=None):
        """Assert that stderr from command contains a given substring"""
        self.assertIsInstance(substr, str, "Parameter 'substr' is not a string")

        if extprog:
            if not re.search(substr, extprog.err):
                msg = self._formatMessage(
                    msg,
                    f"Output from command '{extprog.cmd}' does not contain '{substr}'",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("ExternalProgram cannot be None")

    def assertStdoutIsJSONArray(self,
                                extprog: ExternalProgram = None,
                                msg=None):
        """Assert that stdout from command contains JSON Array"""
        if extprog:
            data = None
            try:
                data = json.dumps(extprog.out)
            except json.JSONDecodeError:
                msg = self._formatMessage(
                    msg,
                    f"Output from command '{extprog.cmd}' does not contain valid JSON content",
                )
                raise self.failureException(msg)
            # We do not assume content must be present, i.e. an empty array is
            # still an array.
            if not isinstance(data, list):
                msg = self._formatMessage(
                    msg,
                    f"Output from command '{extprog.cmd}' does not contain a JSON Array",
                )
                raise self.failureException(msg)
        else:
            raise NoCommandException("ExternalProgram cannot be None")

    def assertRegFileExists(self, path, msg=None):
        """Assert that given path is an existing regular file."""
        if os.path.exists(path):
            s = os.stat(path)
            if not stat.S_ISREG(s.st_mode):
                msg = self._formatMessage(
                    msg,
                    f"Expected '{path}' to be a regular file",
                )
                raise self.failureException(msg)
        else:
            msg = self._formatMessage(
                msg,
                f"File '{path}' does not exist",
            )
            raise self.failureException(msg)

    def assertPathDoesNotExist(self, path, msg=None):
        """Assert that given path does not exist."""
        if os.path.exists(path):
            msg = self._formatMessage(
                msg,
                f"Expected '{path}' not to exist",
            )
            raise self.failureException(msg)

    def assertDirExists(self, path, msg=None):
        """Assert that given path is an existing directory."""
        if os.path.exists(path):
            s = os.stat(path)
            if not stat.S_ISDIR(s.st_mode):
                msg = self._formatMessage(
                    msg,
                    f"Expected '{path}' to be a directory",
                )
                raise self.failureException(msg)
        else:
            msg = self._formatMessage(
                msg,
                f"Directory '{path}' does not exist",
            )
            raise self.failureException(msg)

    def assertFileModifiedAfter(self, path, timestamp: float, msg=None):
        """Assert that given file path is more recent than timestamp."""
        if not os.path.exists(path):
            raise self.failureException(f"File '{path}' does not exist")
        s = os.stat(path)
        if not stat.S_ISREG(s.st_mode):
            raise self.failureException(f"Path '{path}' is not a regular file")
        if not s.st_mtime > timestamp:
            msg = self._formatMessage(
                msg,
                f"Expected file '{path}' to be newer than '{timestamp}'; actual modified time {s.st_mtime} < {timestamp}",
            )
            raise self.failureException(msg)

    def assertDirModifiedAfter(self, path, timestamp: float, msg=None):
        """Assert that given directory path is more recent than timestamp."""
        if not os.path.exists(path):
            raise self.failureException(f"Directory '{path}' does not exist")
        s = os.stat(path)
        if not stat.S_ISDIR(s.st_mode):
            raise self.failureException(f"Path '{path}' is not a directory")
        if not s.st_mtime > timestamp:
            msg = self._formatMessage(
                msg,
                f"Expected directory '{path}' to be newer than '{timestamp}'; actual modified time {s.st_mtime} < {timestamp}",
            )
            raise self.failureException(msg)

    def assertFileSHA1Equals(self, path, checksum: str, msg=None):
        """Assert that SHA1 checksum is correct."""
        actual = ChecksumFile(path).sha1
        if actual != checksum:
            msg = self._formatMessage(
                msg,
                f"SHA1 validation for '{path}' failed, want {checksum}; got {actual}",
            )
            raise self.failureException(msg)

    def assertFileSHA256Equals(self, path, checksum: str, msg=None):
        """Assert that SHA256 checksum is correct."""
        actual = ChecksumFile(path).sha256
        if actual != checksum:
            msg = self._formatMessage(
                msg,
                f"SHA256 validation for '{path}' failed, want {checksum}; got {actual}",
            )
            raise self.failureException(msg)

    def assertFileMD5Equals(self, path, checksum: str, msg=None):
        """Assert that MD5 checksum is correct."""
        actual = ChecksumFile(path).md5
        if actual != checksum:
            msg = self._formatMessage(
                msg,
                f"MD5 validation for '{path}' failed, want {checksum}; got {actual}",
            )
            raise self.failureException(msg)


__all__ = ["IntegraTestCase"]
