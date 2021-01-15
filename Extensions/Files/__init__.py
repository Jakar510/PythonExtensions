import base64
import hashlib
import json
import os
import pickle
import tempfile
from os.path import *
from pathlib import Path as _Path
from typing import *




__all__ = [
        'Path'
        ]

class FileData(Protocol[bytes]):
    def load(self, f: BinaryIO) -> Any: ...
    def dump(self, data: bytes, f: BinaryIO) -> Any: ...

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
    def Remove(self): return os.remove(self._path)

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


    def GetFileData(self, file: FileData, *, Default=None, Check: callable = None, RemoveOnError: bool = False):
        try:
            with open(self, 'rb') as f:
                dat = file.load(f)
                if callable(Check): Check(dat)
                return dat
        except FileNotFoundError: return Default
        except (pickle.PickleError, pickle.PicklingError, json.JSONDecodeError):
            if RemoveOnError: self.Remove()
            return Default
    def SetFileData(self, data: Any, file: FileData, *, Check: callable = None):
            with open(self, 'wb') as f:
                if callable(Check): data = Check(data)
                file.dump(data, f)


    def SaveJson(self, data: Union[List, Dict], **kwargs):
        with open(self, 'w') as f:
            return json.dump(data, f, **kwargs)
    def ReadJson(self, **kwargs) -> Union[List, Dict]:
        with open(self, 'r') as f:
            return json.load(f, **kwargs)


    def SavePickle(self, data: Any, **kwargs):
        with open(self, 'wb') as f:
            return pickle.dump(data, f, **kwargs)
    def ReadPickle(self, **kwargs) -> Any:
        with open(self, 'rb') as f:
            return pickle.load(f, **kwargs)


    def Write(self, content: Union[str, bytes] = None, *, buffering=None, encoding: str = None, errors=None, newline: str = '\n', closefd=True):
        if isinstance(content, str):
            with open(self, 'w', buffering, encoding, errors, newline, closefd) as f:
                f.write(content)

        elif isinstance(content, bytes):
            with open(self, 'wb', buffering, encoding, errors, newline, closefd) as f:
                f.write(content)
    def Read(self, open_as_binary: bool = False):
        with open(self, 'rb' if open_as_binary else 'r') as f:
            f.read()

    @classmethod
    def CreateTemporaryFile(cls, fileName: str, *sub_folders: str, root_dir: str = None):
        if not root_dir: root_dir = tempfile.gettempdir()
        os.makedirs(root_dir, exist_ok=True)
        return cls.Join(root_dir, *sub_folders, fileName)

    @classmethod
    def Create(cls, _path: Union[str, 'Path'], content: Union[str, bytes] = None, *, buffering=None, encoding: str = None, errors=None, newline: str = '\n', closefd=True):
        os.makedirs(basename(_path), exist_ok=True)
        path = cls(os.path.abspath(_path))
        path.Write(content, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd)

        return path

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
        if isfile(path): return [cls.Create(path)]

        d = basename(path)
        def _join(file): return cls.FromString(join(d, file))
        return list(map(_join, os.listdir(path)))





    @staticmethod
    def CopyFile(_inPath: Union[str, 'Path'], _outPath: Union[str, 'Path'], open_as_binary: bool = False):
        with open(_outPath, 'wb' if open_as_binary else 'w') as out:
            with open(_inPath, 'rb' if open_as_binary else 'r') as _in:
                out.write(_in.read())



# _TFile = TypeVar("_TFile", BytesIO, StringIO, FileIO, TextIOWrapper)
# class FileMode(str, Enum):
#     """
#     ========= ===============================================================
#     Character Meaning
#     --------- ---------------------------------------------------------------
#     'r'       open for reading (default)
#     'w'       open for writing, truncating the file first
#     'x'       create a new file and open it for writing
#     'a'       open for writing, appending to the end of the file if it exists
#     'b'       binary mode
#     't'       text mode (default)
#     '+'       open a disk file for updating (reading and writing)
#     ========= ===============================================================
#     """
#     Text = 't'
#
#     Read = 'r'
#     Write = 'w'
#     Create = 'x'
#     Append = 'a'
#
#     ReadBytes = 'rb'
#     WriteBytes = 'wb'
#     CreateBytes = 'xb'
#     AppendBytes = 'ab'
#
#     ReadWrite = 'w+'
#     ReadWriteBytes = 'wb+'
#
#     @staticmethod
#     def IsBinary(o):
#         if isinstance(o, FileMode):
#             return o == FileMode.ReadBytes or o == FileMode.WriteBytes or o == FileMode.ReadWriteBytes or o == FileMode.AppendBytes or o == FileMode.CreateBytes
#
#         return False
#     @staticmethod
#     def IsText(o):
#         if isinstance(o, FileMode):
#             return o == FileMode.Text
#
#         return False
#     @staticmethod
#     def IsString(o):
#         if isinstance(o, FileMode):
#             return o == FileMode.Read or o == FileMode.Write or o == FileMode.ReadWrite or o == FileMode.Create or o == FileMode.Append
#
#         return False
#
#
#
# class BaseFile(Generic[_TFile]):
#     _fp: Optional[_TFile]
#     _mode: FileMode
#     def __init__(self, mode: FileMode): self._mode = mode
#
#     def __enter__(self, **kwargs): return self.Open()
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self._fp:
#             self._fp.__exit__(exc_type, exc_val, exc_tb)
#             self._fp = None
#
#     def Open(self, **kwargs):
#         self._fp.__enter__()
#         return self._fp
#
#     # def close(self) -> None: self._fp.close()
#     # def fileno(self) -> int: return self._fp.fileno()
#     # def flush(self) -> None: self._fp.flush()
#     # def isatty(self) -> bool: return self._fp.isatty()
#     # def tell(self) -> int: return self._fp.tell()
#     # def truncate(self, size: Optional[int] = -1) -> int: return self._fp.truncate(size)
#     # def seek(self, offset: int, whence: int = 0) -> int: return self._fp.seek(offset, whence)
#     # def seekable(self) -> bool: return self._fp.seekable()
#     #
#     # def read(self, n: int = -1) -> AnyStr: return self._fp.read(n)
#     # def readable(self) -> bool: return self._fp.readable()
#     # def readline(self, limit: int = -1) -> AnyStr: return self._fp.readline(limit)
#     # def readlines(self, hint: int = -1) -> list[AnyStr]: return self._fp.readlines(hint)
#     #
#     # def writable(self) -> bool: return self._fp.writable()
#     # def write(self, s: AnyStr) -> int: return self._fp.write(s)
#     # def writelines(self, lines: Iterable[AnyStr]) -> None: return self._fp.writelines(lines)
#     #
#     # def __next__(self) -> AnyStr: return self._fp.__next__()
#     # def __iter__(self) -> Iterator[AnyStr]: return self._fp.__iter__()
#
#
# class LocalFile(BaseFile):
#     _path: Path
#     def __init__(self, path: Path, mode: FileMode):
#         super().__init__(mode)
#         self._path = path
#
#     def Open(self, **kwargs):
#         self._fp = open(self._path.Value, self._mode.value, **kwargs)
#         return super().Open()
#
#
# class VirtualFile(BaseFile[_TFile]):
#     def Open(self, *args, **kwargs):
#         if FileMode.IsBinary(self._mode):
#             self._fp = BytesIO(*args, **kwargs)
#
#         if FileMode.IsString(self._mode):
#             self._fp = StringIO(*args, **kwargs)
#
#         if FileMode.IsText(self._mode):
#             self._fp = TextIOWrapper(*args, **kwargs)
#
#         return super().Open()
