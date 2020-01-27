# -*- coding: utf-8 -*-

import base64
import hashlib
import io
import os
import tempfile
import random

READ_LIMIT_BYTES = 1 << 30  # Do not attempt to read more than 1GB of data


class RandomStrings:
    _letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _digits = "0123456789"

    def __init__(self, seed=None, urandom=False, include_digits=True):
        if urandom and seed:
            raise ValueError("Cannot combine seed value with /dev/urandom")
        if urandom:
            self._r = random.SystemRandom()
        elif seed:
            self._r = random.Random(seed)
        else:
            self._r = random.Random()

        if not include_digits:
            self.chars = self.__class__._letters
        else:
            self.chars = self.__class__._letters + self.__class__._digits

    def string(self, length=10):
        return "".join([
            self.chars[self._r.choice(range(0, self.chars.__len__()))]
            for i in range(0, length)
        ])

    def iter_string(self, length=10, count=100):
        c = count
        while c:
            yield "".join([
                self.chars[self._r.choice(range(0, self.chars.__len__()))]
                for i in range(0, length)
            ])
            c -= 1


class ChecksumStringIO:

    def __init__(self, stream: io.StringIO):
        self._stream = stream

    @property
    def sha1(self):
        offset = self._stream.tell()
        if offset:
            self._stream.seek(0)  # rewind if necessary
        digest = hashlib.sha1(
            self._stream.read(READ_LIMIT_BYTES).encode("utf-8")).hexdigest()

        self._stream.seek(offset)  # reset to original offset
        return digest

    @property
    def sha256(self):
        offset = self._stream.tell()
        if offset:
            self._stream.seek(0)  # rewind if necessary
        digest = hashlib.sha256(
            self._stream.read(READ_LIMIT_BYTES).encode("utf-8")).hexdigest()
        self._stream.seek(offset)  # reset to original offset
        return digest

    @property
    def md5(self):
        offset = self._stream.tell()
        if offset:
            self._stream.seek(0)  # rewind if necessary
        digest = hashlib.md5(
            self._stream.read(READ_LIMIT_BYTES).encode("utf-8")).hexdigest()
        self._stream.seek(offset)  # reset to original offset
        return digest


class ChecksumBytesIO:

    def __init__(self, stream: io.BytesIO):
        self._stream = stream

    @property
    def sha1(self):
        digest = hashlib.sha1(self._stream.read(READ_LIMIT_BYTES)).hexdigest()
        self._stream.seek(0)  # reset to beginning for next operation
        return digest

    @property
    def sha256(self):
        digest = hashlib.sha256(self._stream.read(READ_LIMIT_BYTES)).hexdigest()
        self._stream.seek(0)  # reset to beginning for next operation
        return digest

    @property
    def md5(self):
        digest = hashlib.md5(self._stream.read(READ_LIMIT_BYTES)).hexdigest()
        self._stream.seek(0)  # reset to beginning for next operation
        return digest


class ChecksumStream:

    def __init__(self, stream: io.IOBase):
        self._stream = stream

    def __del__(self):
        if not self._stream.closed:
            self._stream.close()

    @property
    def sha1(self):
        """
        Generate SHA1 checksum for stream

        Returns:
            string: Hexadecimal checksum value
        """
        if self._stream.tell():
            self._stream.seek(0)
        if isinstance(self._stream, io.TextIOBase):
            digest = hashlib.sha1(
                self._stream.read(READ_LIMIT_BYTES).encode(
                    "utf-8")).hexdigest()
        else:
            digest = hashlib.sha1(
                self._stream.read(READ_LIMIT_BYTES)).hexdigest()
        self._stream.seek(0)  # reset to beginning for next operation
        return digest

    @property
    def sha256(self):
        """
        Generate SHA256 checksum for stream

        Returns:
            string: Hexadecimal checksum value
        """
        if self._stream.tell():
            self._stream.seek(0)
        if isinstance(self._stream, io.TextIOBase):
            digest = hashlib.sha256(
                self._stream.read(READ_LIMIT_BYTES).encode(
                    "utf-8")).hexdigest()
        else:
            digest = hashlib.sha256(
                self._stream.read(READ_LIMIT_BYTES)).hexdigest()
        self._stream.seek(0)  # reset to beginning for next operation
        return digest

    @property
    def md5(self):
        """
        Generate MD5 checksum for stream

        Returns:
            string: Hexadecimal checksum value
        """
        if self._stream.tell():
            self._stream.seek(0)
        if isinstance(self._stream, io.TextIOBase):
            digest = hashlib.md5(
                self._stream.read(READ_LIMIT_BYTES).encode(
                    "utf-8")).hexdigest()
        else:
            digest = hashlib.md5(
                self._stream.read(READ_LIMIT_BYTES)).hexdigest()
        self._stream.seek(0)  # reset to beginning for next operation
        return digest

    @property
    def base64_enc(self):
        """
        Generate base64 encoded bytes for stream
        
        Returns:
            bytes: Encoded contents as bytestring
        """
        offset = self._stream.tell()
        encoded: bytes = None
        if isinstance(self._stream, io.TextIOBase):
            encoded = base64.b64encode(
                bytes(self._stream.read().encode("utf-8")))
        else:
            encoded = base64.b64encode(bytes(self._stream.read()))
        self._stream.seek(offset)
        return encoded

    @property
    def base64_dec(self):
        """
        Decode base64 encoded bytes from stream
        
        Returns:
            bytes: Decode contents as bytestring
        """
        offset = self._stream.tell()
        self._stream.seek(0)
        decoded: bytes = None
        if isinstance(self._stream, io.TextIOBase):
            decoded = base64.b64decode(self._stream.read().encode("utf-8"))
        else:
            decoded = base64.b64decode(self._stream.read())
        self._stream.seek(offset)
        return decoded


class ChecksumFile(ChecksumStream):

    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File '{path}' does not exist")
        self._stream = open(path, "rb")
        super(ChecksumFile, self).__init__(self._stream)

    def __del__(self):
        if not self._stream.closed:
            self._stream.close()


class TemporaryFile:
    """Temporary file with automatic deletion."""

    def __init__(
        self,
        initial_content: bytes = None,
        virtual=False,
        suffix=None,
        prefix=None,
        dir=None,
        delete=True,
    ):
        if virtual:
            self._f = tempfile.TemporaryFile(suffix=suffix,
                                             prefix=prefix,
                                             dir=dir)
        else:
            self._f = tempfile.NamedTemporaryFile(suffix=suffix,
                                                  prefix=prefix,
                                                  dir=dir,
                                                  delete=delete)
        if initial_content:
            self._f.write(initial_content)
            self._f.seek(0)  # Seek to starting offset
        self._csum = ChecksumStream(self._f)

    def __del__(self):
        self._f.close()

    def read(self, size=-1):
        return self._f.read(size)

    def write(self, b):
        return self._f.write(b)

    @property
    def abspath(self):
        return self._f.name

    @property
    def fp(self):
        return self._f

    @property
    def sha1(self):
        """
        SHA1 checksum of file content.
        
        Returns:
            str: Hexadecimal checksum string.
        """
        return self._csum.sha1

    @property
    def sha256(self):
        """
        SHA256 checksum of file content.
        
        Returns:
            str: Hexadecimal checksum string.
        """
        return self._csum.sha256

    @property
    def md5(self):
        """
        MD5 checksum of file content.
        
        Returns:
            str: Hexadecimal checksum string.
        """
        return self._csum.md5

    @property
    def content(self):
        offset = self._f.tell()
        self._f.seek(0)
        content = self._f.read(READ_LIMIT_BYTES).decode("utf-8")
        self._f.seek(offset)
        return content
