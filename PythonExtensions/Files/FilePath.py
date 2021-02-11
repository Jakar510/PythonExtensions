import base64
import hashlib
import json
import os
import pickle
import tempfile
from os import PathLike, chmod, fsencode, listdir, makedirs, remove, rename
from os.path import *
from pathlib import Path
from shutil import rmtree

from ..Json import *
from ..Names import nameof




__all__ = [
    'FilePath',
    'FileIO',
    'ReadWriteData'
    ]


class ReadWriteData(Protocol[AnyStr]):
    def load(self, f: BinaryIO) -> Any: ...
    def dump(self, data: AnyStr, f: BinaryIO) -> Any: ...


class FileIO(PathLike):
    def __init__(self, _path: Union[str, 'FilePath']):
        if not isinstance(_path, FilePath):
            _path = FilePath(_path)

        self._path = _path


    @property
    def path(self) -> 'FilePath': return self._path

    def Remove(self): return self._path.Remove()
    def __del__(self): return self._path.__del__()
    def __repr__(self): return f'<{nameof(self)} Object. Location: "{self._path}">'
    def __str__(self): return str(self._path)
    def __fspath__(self): return self._path.__fspath__()
    def __bytes__(self):
        """ Return the bytes representation of the path. This is only recommended to use under Unix. """
        return bytes(self._path)


    def GetFileData(self, file: ReadWriteData, *, Default=None, Check: callable = None, RemoveOnError: bool = False):
        try:
            with open(self._path, 'rb') as f:
                dat = file.load(f)
                if callable(Check): Check(dat)
                return dat
        except FileNotFoundError: return Default
        except (pickle.PickleError, pickle.PicklingError, json.JSONDecodeError):
            if RemoveOnError: self._path.Remove()
            return Default
    def SetFileData(self, data: Any, file: ReadWriteData, *, Check: callable = None):
        with open(self._path, 'wb') as f:
            if callable(Check): data = Check(data)
            return file.dump(data, f)


    def SaveJson(self, data: Union[List, Dict], **kwargs):
        with open(self._path, 'w') as f:
            return json.dump(data, f, **kwargs)
    def ReadJson(self, **kwargs) -> Union[List, Dict]:
        with open(self._path, 'r') as f:
            return json.load(f, **kwargs)


    def SavePickle(self, data: Any, **kwargs):
        with open(self._path, 'wb') as f:
            return pickle.dump(data, f, **kwargs)
    def ReadPickle(self, **kwargs) -> Any:
        with open(self._path, 'rb') as f:
            return pickle.load(f, **kwargs)


    def Write(self, content: Union[str, bytes], *, newline: str = '\n', **kwargs) -> int:
        if isinstance(content, str):
            with open(self._path, 'w', newline=newline, **kwargs) as f:
                return f.write(content)

        elif isinstance(content, bytes):
            with open(self._path, 'wb', newline=newline, **kwargs) as f:
                return f.write(content)

        else: raise TypeError(type(content), (bytes, str))
    def Read(self, open_as_binary: bool = False):
        with open(self._path, 'rb' if open_as_binary else 'r') as f:
            return f.read()


    @classmethod
    def TemporaryFile(cls, *sub_folders: str, _name: str, root_dir: str = None): return FilePath.Temporary(*sub_folders, _name, root_dir=root_dir)

    @classmethod
    def Create(cls, _path: Union[str, 'FilePath'], content: Union[str, bytes] = None, *,
               buffering=None, encoding: str = None, errors=None, newline: str = '\n', closefd=True):
        os.makedirs(basename(_path), exist_ok=True)
        _path = cls(_path)
        _path.Write(content, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd)

        return _path

    @staticmethod
    def CopyFile(_inPath: Union[str, 'FilePath'], _outPath: Union[str, 'FilePath'], open_as_binary: bool = False):
        with open(_outPath, 'wb' if open_as_binary else 'w') as out:
            with open(_inPath, 'rb' if open_as_binary else 'r') as _in:
                out.write(_in.read())


class FilePath(dict, BaseModel, PathLike):
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

    def __hash__(self) -> int: return hash(self.Value)
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

    def Rename(self, new: str): return rename(self.Value, join(self.BaseName, new))
    def Remove(self):
        if self.Exists:
            if self.IsFile: return remove(self)
            elif self.IsDirectory: return rmtree(self)

    def Chmod(self, mode: int, dir_fd=None, follow_symlinks: bool = False) -> None:
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
        return chmod(self.Value, mode, dir_fd=dir_fd, follow_symlinks=follow_symlinks)
    def Create(self, data: Union[str, bytes] = None, mode: int = 0o777, exist_ok: bool = True) -> FileIO:
        makedirs(self.BaseName, mode, exist_ok)
        file = FileIO(self)
        if self.Exists or not data: return file
        file.Write(data)
        return file

        # if isinstance(data, str):
        #     with open(self, 'w') as f:
        #         f.write(data)
        #
        #     return self
        #
        # if isinstance(data, bytes):
        #     with open(self, 'wb') as f:
        #         f.write(data)
        #
        # else:
        #     with open(self, 'ab'): pass
        #
        # return self



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
        _name = self.FileName
        if not _name: return None
        ext = _name.split('.')[-1]
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



    def ToString(self) -> str: return f'<{nameof(self)}() "{self.Value}">'
    def __repr__(self): return self.ToString()
    def __str__(self): return self.Value
    def __fspath__(self): return self.Value
    def __bytes__(self):
        """ Return the bytes representation of the path. This is only recommended to use under Unix. """
        return fsencode(self.Value)
    def __setitem__(self, key, value):
        if hasattr(self, '_hash'): del self._hash
        super(FilePath, self).__setitem__(key, value)
    def __del__(self):
        try:
            if self._temporary and self.Exists: return self.Remove()
        except PermissionError: pass

    def __eq__(self, other):
        if not isinstance(other, (str, self.__class__)):
            raise TypeError(type(other), (str, self.__class__))

        if isinstance(other, str):
            return self.Value == other

        return self.Value == other.Value
    def __ne__(self, other): return not self.__eq__(other)
    def __gt__(self, other):
        if not isinstance(other, (str, self.__class__)):
            raise TypeError(type(other), (str, self.__class__))

        if isinstance(other, str):
            return self.Value > other

        return self.Value > other.Value
    def __lt__(self, other):
        if not isinstance(other, (str, self.__class__)):
            raise TypeError(type(other), (str, self.__class__))

        if isinstance(other, str):
            return self.Value < other

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
    def CurrentFile(cls, file=__file__): return cls(file)

    @classmethod
    def FromString(cls, _path: Union[str, 'FilePath']) -> 'FilePath': return cls(_path)
    @classmethod
    def FromPath(cls, _path: Path) -> 'FilePath': return cls(str(_path.resolve()))

    @classmethod
    def Join(cls, *args: Union[str, 'FilePath']) -> 'FilePath': return cls(join(*args))

    @classmethod
    def ListDir(cls, _path: Union[str, 'FilePath']) -> List['FilePath']:
        if not isinstance(_path, FilePath):
            _path = cls(_path)

        if _path.IsFile: return [cls.FromString(_path)]

        if not _path.IsDirectory: raise FileNotFoundError(f'path "{_path}" is not a valid directory.')
        def _join(file): return cls.Join(_path, file)
        return sorted(map(_join, listdir(_path)))

    @classmethod
    def Temporary(cls, *args: str, root_dir: str = None) -> FileIO:
        _path = cls.Join(root_dir or tempfile.gettempdir(), *args)
        _path._temporary = True
        return _path.Create()

    @classmethod
    def Parse(cls, d) -> 'FilePath':
        if isinstance(d, dict):
            return cls(d)

        throw(d, dict)
