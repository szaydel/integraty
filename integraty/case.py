# -*- coding: utf-8 -*-

import json
import logging
import math
import os
import re
import stat
import sys

from collections import Counter
from difflib import SequenceMatcher
from unittest import TestCase
from unittest import main as run_integra_tests

from integraty.extprog import ExternalProgram
from integraty.productivity import ChecksumFile


def is_equal(num1: float, num2: float, ε: float = 0.0000001) -> bool:
    if abs(num1 - num2) < ε:
        return True
    return False


class NoCommandException(Exception):
    pass


class InvalidStream(Exception):
    pass


class Similarity:

    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2

    @staticmethod
    def _cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum(vec1[x] * vec2[x] for x in intersection)
        sum1 = sum(vec1[x]**2 for x in vec1.keys())
        sum2 = sum(vec2[x]**2 for x in vec2.keys())
        denom = math.sqrt(sum1) * math.sqrt(sum2)

        return float(numerator) / denom if denom else 0.0

    @staticmethod
    def _text2vec(text):
        word = re.compile(r'\w+')
        words = word.findall(text)
        return Counter(words)

    @staticmethod
    def _levenshtein_distance(str1, str2):
        m = len(str1)
        n = len(str2)
        lensum = float(m + n)
        d = []
        for i in range(m + 1):
            d.append([i])
        del d[0][0]
        for j in range(n + 1):
            d[0].append(j)
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                if str1[i - 1] == str2[j - 1]:
                    d[i].insert(j, d[i - 1][j - 1])
                else:
                    minimum = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                                  d[i - 1][j - 1] + 2)
                    d[i].insert(j, minimum)
        ldist = d[-1][-1]
        ratio = (lensum - ldist) / lensum
        return ldist, ratio

    def consine_distance(self):
        vec1 = self._text2vec(self.str1)
        vec2 = self._text2vec(self.str2)
        return self._cosine(vec1, vec2)

    def levenshtein_distance(self):
        return self._levenshtein_distance(self.str1, self.str2)

    @property
    def levenshtein_dist_ratio(self):
        _, ratio = self._levenshtein_distance(self.str1, self.str2)
        return ratio


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

    def assertCommandSucceeded(self,
                               extprog: ExternalProgram = None,
                               msg=None):
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
        self.assertIsInstance(substr, str,
                              "Parameter 'substr' is not a string")

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
        self.assertIsInstance(substr, str,
                              "Parameter 'substr' is not a string")

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

    def assertStringsAlmostEqual(self,
                                 str1,
                                 str2,
                                 ratio: float = 0.8,
                                 max_distance: int = None,
                                 msg=None):
        """Assert that two strings are similar enough; by default 80% in common using Levenshtein Distance"""
        sim = Similarity(str1, str2)
        actual_distance, actual_ratio = sim.levenshtein_distance()
        if max_distance and actual_distance > max_distance:
            msg = self._formatMessage(
                msg,
                f"Expected distance between '{str1}' and '{str2}', to be less than {max_distance}, instead distance is {actual_distance}",
            )
            raise self.failureException(msg)
        if is_equal(actual_ratio, ratio) or actual_ratio > ratio:
            return
        msg = self._formatMessage(
            msg,
            f"Expected '{str1}' to be at least {100*ratio:.4f}% similar to '{str2}', instead similarity is only {100*actual_ratio:.4f}%",
        )
        raise self.failureException(msg)

    def assertStringsAlmostEqualDiffLib(self,
                                 str1,
                                 str2,
                                 ratio: float = 0.8,
                                 msg=None):
        """Assert that two strings are similar enough; by default 80% in common using Difflib SequenceMatcher"""
        actual_ratio = SequenceMatcher(None, str1, str2).quick_ratio()
        if is_equal(actual_ratio, ratio) or actual_ratio > ratio:
            return
        msg = self._formatMessage(
            msg,
            f"Expected '{str1}' to be at least {100*ratio:.4f}% similar to '{str2}', instead similarity is only {100*actual_ratio:.4f}%",
        )
        raise self.failureException(msg)

    def assertStringsAlmostEqualCosine(self,
                                       str1,
                                       str2,
                                       ratio: float = 0.8,
                                       msg=None):
        """Assert that two strings are similar enough; by default 80% in common using Cosine Similarity"""
        sim = Similarity(str1, str2)
        actual_ratio = sim.consine_distance()
        if is_equal(actual_ratio, ratio) or actual_ratio > ratio:
            return
        msg = self._formatMessage(
            msg,
            f"Expected '{str1}' to be at least {100*ratio:.4f}% similar to '{str2}', instead similarity is only {100*actual_ratio:.4f}%",
        )
        raise self.failureException(msg)

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
