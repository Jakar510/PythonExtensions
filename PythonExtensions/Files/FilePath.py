import base64
import hashlib
import os
import tempfile
from os.path import *
from pathlib import Path
from shutil import rmtree

from ..Json import *




__all__ = [
    'FilePath',
    ]

class FilePath(dict, BaseModel, os.PathLike):
    _hash: str
    _temporary: bool = False
    def __init__(self, obj: Union[str, Dict, Path, 'FilePath']):
        d = { }
        if isinstance(obj, dict):
            AssertKeys(obj, Keys.Path)
            d = obj

        elif isinstance(obj, str):
            d[Keys.Path] = abspath(obj)

        elif isinstance(obj, Path):
            d[Keys.Path] = obj.resolve()

        elif isinstance(obj, FilePath):
            d[Keys.Path] = obj.Value

        else: throw(obj, str, Path, FilePath, dict)

        dict.__init__(self, d)

    def __call__(self) -> str: return self.Value
    @property
    def Value(self) -> str: return self[Keys.Path]
    @property
    def IsTemporary(self) -> bool: return self._temporary

    @property
    def Exists(self) -> bool: return exists(self.Value)

    @property
    def IsFile(self) -> bool: return isfile(self.Value)
    @property
    def IsDirectory(self) -> bool: return isdir(self.Value)
    @property
    def IsLink(self) -> bool: return islink(self.Value)

    def rename(self, new: str): return os.rename(self.Value, join(self.BaseName, new))
    def Remove(self):
        if self.Exists:
            if self.IsFile: return os.remove(self)
            elif self.IsDirectory: return rmtree(self)

    def chmod(self, mode: int, dir_fd=None, follow_symlinks: bool = False) -> None:
        """
        Change the access permissions of a file.

          path
            FilePath to be modified.  May always be specified as a str, bytes, or a path-like object.
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
        return os.chmod(self.Value, mode, dir_fd=dir_fd, follow_symlinks=follow_symlinks)
    def Create(self, data: Union[str, bytes] = None, mode: int = 0o777, exist_ok: bool = True):
        os.makedirs(self.BaseName, mode, exist_ok)
        if self.Exists: return self
        if isinstance(data, str):
            with open(self, 'w') as f:
                f.write(data)

            return self

        if isinstance(data, bytes):
            with open(self, 'wb') as f:
                f.write(data)

        else:
            with open(self, 'wb'): pass

        return self

    # def Clear(self):
    #     for root, folders, files in os.walk(self):
    #         for f in files: os.remove(join(root, f))
    #
    #         for f in folders: os.remove(join(root, f))


    @property
    def BaseName(self) -> 'FilePath': return FilePath.FromString(basename(self.Value))
    @property
    def DirectoryName(self) -> 'FilePath': return FilePath.FromString(dirname(self.Value))

    @property
    def FileName(self) -> Optional[str]:
        if self.IsDirectory: return None
        return Path(self.Value).name


    @overload
    def Extension(self) -> Optional[str]: ...
    @overload
    def Extension(self, raw: Any) -> Optional[str]: ...
    @overload
    def Extension(self, replacements: Dict[str, str]) -> Optional[str]: ...
    @overload
    def Extension(self, replacements: Dict[str, str], lower: Any) -> Optional[str]: ...
    @overload
    def Extension(self, replacements: Dict[str, str], upper: Any) -> Optional[str]: ...

    def Extension(self, replacements: Dict[str, str] = { }, **kwargs) -> Optional[str]:
        name = self.FileName
        if not name: return None
        ext = name.split('.')[-1]
        if not kwargs or 'raw' in kwargs: return ext

        if kwargs.pop('lower', None):
            ext = ext.lower()

        if kwargs.pop('upper', None):
            ext = ext.upper()

        for key, value in replacements.items():
            ext = ext.replace(key, value)

        return ext


    @property
    def Size(self) -> int: return getsize(self.Value)
    def ToUri(self): return Path(self.Value).as_uri()

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



    def ToString(self) -> str:
        try:
            return f'<{self.__class__.__qualname__}() "{self.Value}">'
        except AttributeError:
            return f'<{self.__class__.__name__}() "{self.Value}">'
    def __repr__(self): return self.ToString()
    def __str__(self): return self.Value
    def __fspath__(self): return self.Value
    def __bytes__(self):
        """ Return the bytes representation of the path. This is only recommended to use under Unix. """
        return os.fsencode(self.Value)
    def __setitem__(self, key, value):
        if hasattr(self, '_hash'): del self._hash
        super(FilePath, self).__setitem__(key, value)
    def __del__(self):
        try:
            if self._temporary and self.Exists: return self.Remove()
        except PermissionError: pass

    def __eq__(self, other):
        if not isinstance(other, self.__class__): raise TypeError(type(other), self.__class__)
        return self.Value == other.Value
    def __ne__(self, other): return not self.__eq__(other)
    def __gt__(self, other):
        if not isinstance(other, self.__class__): raise TypeError(type(other), self.__class__)
        return self.Value > other.Value
    def __lt__(self, other):
        if not isinstance(other, self.__class__): raise TypeError(type(other), self.__class__)
        return self.Value < other.Value

    def __state__(self):
        d = { }
        for k in set(dir(self)).difference(dir(dict)):
            if k.startswith('_'): continue
            if k in ('Remove', 'GetHashID'): continue

            try:
                v = getattr(self, k)
                if isinstance(v, classmethod): continue
                if callable(v):
                    v = v()
            except (ValueError, TypeError, FileNotFoundError): pass
            else:
                d[k] = v

        return d





    @classmethod
    def FromString(cls, _path: Union[str, 'FilePath']) -> 'FilePath': return cls(_path)
    @classmethod
    def FromPath(cls, _path: Path) -> 'FilePath': return cls(str(_path.resolve()))

    @classmethod
    def Join(cls, *args: Union[str, 'FilePath']) -> 'FilePath': return cls(join(*args))

    @classmethod
    def ListDir(cls, path: Union[str, 'FilePath']) -> List['FilePath']:
        if not isinstance(path, FilePath):
            path = cls(path)

        if path.IsFile: return [cls.FromString(path)]

        if not path.IsDirectory: raise FileNotFoundError(f'path "{path}" is not a valid directory.')
        def _join(file): return cls.Join(path, file)
        return sorted(map(_join, os.listdir(path)))

    @classmethod
    def Temporary(cls, *args: str, root_dir: str = None):
        path = cls.Join(root_dir or tempfile.gettempdir(), *args)
        path._temporary = True
        return path.Create()

    @classmethod
    def Parse(cls, d) -> 'FilePath':
        if isinstance(d, dict):
            return cls(d)

        throw(d, dict)



    # @classmethod
    # @overload
    # def MakeDirectories(cls, path: str): ...
    # @classmethod
    # @overload
    # def MakeDirectories(cls, path: 'FilePath'): ...
    # @classmethod
    # @overload
    # def MakeDirectories(cls, path: Path): ...
    # @classmethod
    # @overload
    # def MakeDirectories(cls, *path: str): ...
    # @classmethod
    # @overload
    # def MakeDirectories(cls, *path: 'FilePath'): ...
    #
    #
    # @classmethod
    # def MakeDirectories(cls, *args):
    #     if len(args) == 1:
    #         args = args[0]
    #         if isinstance(args, str):
    #             path = cls.FromString(args)
    #
    #         elif isinstance(args, Path):
    #             path = cls.FromPath(args)
    #
    #         else:
    #             path = args
    #     else:
    #         path = cls.Join(*args)
    #
    #     os.makedirs(path)
    #     return path
