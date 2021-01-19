import base64
import hashlib
import os
from os.path import *
from pathlib import Path as _Path
from shutil import rmtree
from typing import *
from typing import BinaryIO

from ..Json import AssertKeys, BaseDictModel, Keys, throw




__all__ = [
    'Path',
    'FileData'
    ]

class FileData(Protocol[AnyStr]):
    def load(self, f: BinaryIO) -> Any: ...
    def dump(self, data: AnyStr, f: BinaryIO) -> Any: ...



class Path(BaseDictModel[str, Union[str, bool]], os.PathLike):
    _hash: str
    @property
    def Value(self) -> str: return self._path
    @property
    def _path(self) -> str: return self[Keys.Path]
    @property
    def IsTemporary(self) -> bool: return Keys.Temporary in self

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
        if self.Exists:
            if self.IsFile: return os.remove(self._path)
            elif self.IsDirectory: return rmtree(self)

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
    def extension(self, replacements: Dict[str, str]) -> str: ...
    @overload
    def extension(self, replacements: Dict[str, str], lower: Any) -> str: ...
    @overload
    def extension(self, replacements: Dict[str, str], upper: Any) -> str: ...

    def extension(self, replacements: Dict[str, str] = { }, **kwargs) -> str:
        ext = splitext(self._path)[1]
        if not kwargs or 'raw' in kwargs: return ext

        if kwargs.pop('lower', None):
            ext = ext.lower()

        if kwargs.pop('upper', None):
            ext = ext.upper()

        for key, value in replacements.items():
            ext = ext.replace(key, value)

        return ext

    @property
    def BaseName(self) -> 'Path': return Path.FromString(basename(self._path))
    @property
    def DirectoryName(self) -> 'Path': return Path.FromString(dirname(self._path))

    @property
    def Size(self) -> int: return getsize(self._path)
    def ToUri(self): return _Path(self._path).as_uri()

    def GetHashID(self, BlockSize: int = 65536) -> str:
        """
        :param BlockSize: defaults to 64KB
        :return:
        """
        if self.IsDirectory: raise IsADirectoryError('Argument cannot be a directory.')

        try:
            return self._hash
        except AttributeError:
            _hasher = hashlib.sha1()
            with open(self, 'rb') as f:
                buf = f.read(BlockSize)
                while len(buf) > 0:
                    _hasher.update(buf)
                    buf = f.read(BlockSize)
            self._hash = base64.urlsafe_b64encode(_hasher.digest()).decode()
            return self._hash

    def __del__(self):
        if self.IsTemporary and self.Exists: return self.Remove()
    def __str__(self): return self._path
    def __fspath__(self): return self._path
    def __bytes__(self):
        """ Return the bytes representation of the path. This is only recommended to use under Unix. """
        return os.fsencode(self._path)
    def __setitem__(self, key, value):
        if hasattr(self, '_hash'): del self._hash
        super(Path, self).__setitem__(key, value)

    def __eq__(self, other):
        if not isinstance(other, Path): raise TypeError(type(other), Path)
        return self._path == other._path
    def __ne__(self, other):
        if not isinstance(other, Path): raise TypeError(type(other), Path)
        return self._path != other._path
    def __gt__(self, other):
        if not isinstance(other, Path): raise TypeError(type(other), Path)
        return self._path > other._path
    def __lt__(self, other):
        if not isinstance(other, Path): raise TypeError(type(other), Path)
        return self._path < other._path

    @classmethod
    def FromString(cls, _path: Union[str, 'Path']) -> 'Path': return cls.Init(_path)

    @classmethod
    def FromPathLibPath(cls, _path: _Path) -> 'Path': return cls.Init(str(_path.resolve()))

    @classmethod
    def Join(cls, *args: Union[str, 'Path'], temporary_file: bool = False) -> 'Path': return cls.Init(join(*args), temporary_file=temporary_file)

    @classmethod
    def MakeDirectories(cls, path: Union[str, 'Path'], mode: int = 0o777, exist_ok: bool = True) -> 'Path':
        os.makedirs(path, mode, exist_ok)
        return cls.Init(path)

    @classmethod
    def ListDir(cls, path: Union[str, 'Path']) -> List['Path']:
        if not isinstance(path, Path):
            path = Path.Init(path)

        if path.IsFile: return [cls.FromString(path)]

        if not path.IsDirectory: raise FileNotFoundError(f'path "{path}" is not a valid directory.')
        def _join(file): return cls.Join(path, file)
        return sorted(map(_join, os.listdir(path)))

    @classmethod
    def Init(cls, path: str, *, temporary_file: bool = False) -> 'Path':
        if temporary_file: return cls({ Keys.Path: abspath(path), Keys.Temporary: temporary_file })
        return cls({ Keys.Path: abspath(path) })

    @classmethod
    def Parse(cls, d) -> 'Path':
        if isinstance(d, dict):
            AssertKeys(d, Keys.Path)
            return cls(d)

        throw(d, dict)
