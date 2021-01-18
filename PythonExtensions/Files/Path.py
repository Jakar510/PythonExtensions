import base64
import hashlib
import json
import os
import pickle
import tempfile
from os.path import *
from pathlib import Path as _Path
from typing import *
from typing import BinaryIO




__all__ = [
    'Path',
    'FileData'
    ]

class FileData(Protocol[AnyStr]):
    def load(self, f: BinaryIO) -> Any: ...
    def dump(self, data: AnyStr, f: BinaryIO) -> Any: ...



class Path(os.PathLike):
    def __init__(self, _path: str, temporary_file: bool = False):
        self._temporary_file = temporary_file
        self._path = _path

    @property
    def Exists(self) -> bool: return exists(self._path)

    @property
    def IsFile(self) -> bool: return isfile(self._path)
    @property
    def IsDirectory(self) -> bool: return isdir(self._path)
    @property
    def IsLink(self) -> bool: return islink(self._path)

    def rename(self, new: str): return os.rename(self._path, join(self.BaseName, new))
    def Remove(self):
        if self.Exists: return os.remove(self._path)

    def chmod(self, mode: int, dir_fd=None, follow_symlinks: bool = False) -> None:
        """
        Change the access permissions of a file.

          path
            Path to be modified.  May always be specified as a str, bytes, or a path-like object.
            On some platforms, path may also be specified as an open file descriptor.
            If this functionality is unavailable, using it raises an exception.
          mode
            Operating-system mode bitfield.
          dir_fd
            If not None, it should be a file descriptor open to a directory,
            and path should be relative; path will then be relative to that
            directory.
          follow_symlinks
            If False, and the last element of the path is a symbolic link,
            chmod will modify the symbolic link itself instead of the file
            the link points to.

        It is an error to use dir_fd or follow_symlinks when specifying path as
          an open file descriptor.
        dir_fd and follow_symlinks may not be implemented on your platform.
          If they are unavailable, using them will raise a NotImplementedError.
        """
        return os.chmod(self._path, mode, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

    @property
    def FileName(self) -> str: return splitext(self._path)[0]

    @overload
    def extension(self) -> str: ...
    @overload
    def extension(self, raw: Any) -> str: ...
    @overload
    def extension(self, **kwargs: str) -> str: ...
    @overload
    def extension(self, lower: Any, **kwargs: str) -> str: ...
    @overload
    def extension(self, upper: Any, **kwargs: str) -> str: ...

    def extension(self, **kwargs) -> str:
        ext = splitext(self._path)[1]
        if not kwargs or 'raw' in kwargs: return ext

        if kwargs.pop('lower', None):
            ext = ext.lower()

        if kwargs.pop('upper', None):
            ext = ext.upper()

        for key, value in kwargs.items():
            ext = ext.replace(key, value)

        return ext

    @property
    def BaseName(self) -> 'Path': return Path.FromString(basename(self._path))
    @property
    def DirectoryName(self) -> str: return dirname(self._path)

    @property
    def Size(self) -> int: return getsize(self._path)
    def ToUri(self): return _Path(self._path).as_uri()


    def GetHashID(self, BlockSize: int = 65536) -> str:
        """
        :param BlockSize: defaults to 64KB
        :return:
        """
        if self.IsDirectory: raise IsADirectoryError('Argument cannot be a directory.')

        _hasher = hashlib.sha1()
        with open(self, 'rb') as f:
            buf = f.read(BlockSize)
            while len(buf) > 0:
                _hasher.update(buf)
                buf = f.read(BlockSize)
        return base64.urlsafe_b64encode(_hasher.digest()).decode()



    def __del__(self):
        if self._temporary_file and self.Exists: return self.Remove()
    def __str__(self): return self._path
    def __repr__(self):
        try: return f'<{self.__class__.__qualname__} Object. Location: "{self._path}">'
        except AttributeError: return f'<{self.__class__.__name__} Object. Location: "{self._path}">'
    def __bytes__(self):
        """ Return the bytes representation of the path. This is only recommended to use under Unix. """
        return os.fsencode(self._path)
    def __fspath__(self): return self._path

    def __eq__(self, other):
        if not isinstance(other, Path): return NotImplementedError()
        return self._path == other._path
    def __ne__(self, other):
        if not isinstance(other, Path): return NotImplementedError()
        return self._path != other._path

    def __hash__(self):
        try:
            return self._hash
        except AttributeError:
            self._hash = hash(self._path)
            return self._hash

    @property
    def Value(self): return self._path

    @classmethod
    def FromString(cls, _path: Union[str, 'Path']): return cls(abspath(_path))

    @classmethod
    def FromPathLibPath(cls, _path: _Path): return cls(abspath(_path.resolve()))

    @classmethod
    def Join(cls, *args: str): return cls(join(*args))

    @classmethod
    def MakeDirectories(cls, path: Union[str, 'Path'], mode: int = 0o777, exist_ok: bool = True):
        os.makedirs(path, mode, exist_ok)
        return cls(path)

    @classmethod
    def ListDir(cls, path: Union[str, 'Path']) -> List['Path']:
        if isfile(path): return [cls.FromString(path)]

        d = basename(path)
        def _join(file): return cls.FromString(join(d, file))
        return list(map(_join, os.listdir(path)))

