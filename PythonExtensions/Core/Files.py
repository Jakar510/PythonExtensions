import base64
import hashlib
import json
import os
import pickle
import tempfile
from multiprocessing.pool import ThreadPool
from os import PathLike, chmod, fsencode, listdir, makedirs, remove, rename
from os.path import *
from pathlib import Path
from shutil import copy2, rmtree
from typing import *
from typing import BinaryIO

from aiofiles import open as async_open
from attr import attrib, attrs, validators
from cryptography.fernet import Fernet

from ..Core.Json import *
from ..Core.Names import nameof




__all__ = [
    'FilePath',
    'FileIO',
    'ReadWriteData',
    'Encryptor',
    'MultiThreadedCopier'
    ]

class ReadWriteData(Protocol[AnyStr]):
    def load(self, f: BinaryIO) -> Any: ...
    def dump(self, data: AnyStr, f: BinaryIO) -> Any: ...


@attrs(slots=True, hash=True, order=True, eq=True, auto_attribs=True, init=False)
class FilePath(PathLike):
    FullPath: str = attrib(validator=validators.instance_of((dict, Path, str, PathLike)))
    IsTemporary: bool = attrib(validator=validators.instance_of(bool), init=False)
    Hash: Optional[str] = attrib(default=None, validator=validators.instance_of(str), init=False)

    def __init__(self, _path: Union[str, Dict[str, Any], Path, 'FilePath'], temporary: bool = False):
        self.FullPath = self.convert(_path)
        self.IsTemporary = temporary


    @staticmethod
    def convert(_path: Union[str, Dict[str, Any], Path, 'FilePath']) -> str:
        if isinstance(_path, dict):
            options = ('path', 'Path', 'fullPath', 'fullpath', 'FullPath')
            for option in options:
                if option in _path:
                    return FilePath.convert(_path['FullPath'])

            raise KeyError(f'Not one of {options} are found in provided dict')

        elif isinstance(_path, str):
            return abspath(_path)

        elif isinstance(_path, Path):
            return _path.resolve().__fspath__()

        elif isinstance(_path, FilePath):
            return _path.FullPath

        elif hasattr(_path, '__fspath__'):
            return abspath(_path.__fspath__())

        else:
            throw(_path, str, Path, FilePath, dict)


    @property
    def __class_name__(self) -> str:
        return nameof(self)


    @property
    def Exists(self) -> bool:
        return exists(self.FullPath)

    @property
    def IsFile(self) -> bool:
        return isfile(self.FullPath)
    @property
    def IsDirectory(self) -> bool:
        return isdir(self.FullPath)
    @property
    def IsLink(self) -> bool:
        return islink(self.FullPath)

    def Rename(self, new: str):
        return rename(self.FullPath, join(self.BaseName, new))
    def Remove(self):
        if self.Exists:
            if self.IsFile:
                return remove(self)
            elif self.IsDirectory:
                return rmtree(self)


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
        return chmod(self.FullPath, mode, dir_fd=dir_fd, follow_symlinks=follow_symlinks)



    @property
    def _locked(self):
        return isfile(self._lockFile)
    @property
    def _lockFile(self):
        return f'{self.FullPath}.lock'

    def __enter__(self):
        while self._locked:
            pass

        with open(self._lockFile, 'w') as f:
            f.write(self.FileName)

        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clearLcok()
    def _clearLcok(self):
        if self._locked:
            remove(self._lockFile)


    def __call__(self, mode: int = 0o777, exist_ok: bool = True) -> Optional['FileIO']:
        """
        Creates the base directories then opens the file for reading / writing via FileIO

        :param mode:
        :param exist_ok:
        :return: FileIO
        """
        makedirs(self.BaseName, mode, exist_ok)

        return None if self.IsDirectory else FileIO(self)



    @property
    def BaseName(self) -> 'FilePath':
        return FilePath(basename(self.FullPath))
    @property
    def DirectoryName(self) -> 'FilePath':
        return FilePath(dirname(self.FullPath))

    @property
    def FileName(self) -> Optional[str]:
        if self.IsDirectory: return None
        return Path(self.FullPath).name


    @overload
    def Extension(self) -> Optional[str]:
        ...
    @overload
    def Extension(self, raw: Any) -> Optional[str]:
        ...
    @overload
    def Extension(self, replacements: Dict[str, str]) -> Optional[str]:
        ...
    @overload
    def Extension(self, replacements: Dict[str, str], lower: Any) -> Optional[str]:
        ...
    @overload
    def Extension(self, replacements: Dict[str, str], upper: Any) -> Optional[str]:
        ...

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
    def Size(self) -> int:
        return getsize(self.FullPath)
    def ToUri(self):
        return Path(self.FullPath).as_uri()

    def GetHashID(self, BlockSize: int = 65536) -> str:
        """
        :param BlockSize: defaults to 64KB
        :return:
        """
        if self.IsDirectory: raise IsADirectoryError('Argument cannot be a directory.')

        if self.Hash is None:
            _hasher = hashlib.sha1()
            with open(self, 'rb') as f:
                buf = f.read(BlockSize)
                while len(buf) > 0:
                    _hasher.update(buf)
                    buf = f.read(BlockSize)
            self.Hash = base64.urlsafe_b64encode(_hasher.digest()).decode()

        return self.Hash



    def ToString(self) -> str:
        return f'<{nameof(self)}() "{self.FullPath}">'
    def __str__(self):
        return self.FullPath
    def __fspath__(self):
        return self.FullPath
    def __bytes__(self):
        """ Return the bytes representation of the path. This is only recommended to use under Unix. """
        return fsencode(self.FullPath)
    def __del__(self):
        self._clearLcok()
        try:
            if self.IsTemporary and self.Exists: return self.Remove()
        except PermissionError:
            pass

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
            except (ValueError, TypeError, FileNotFoundError):
                pass
            else:
                d[k] = v

        return d



    @classmethod
    def CurrentFile(cls, file=__file__):
        return cls(file)

    @classmethod
    def Join(cls, *args: Union[str, 'FilePath']) -> 'FilePath':
        return cls(join(*args))

    @classmethod
    def ListDir(cls, _path: Union[str, 'FilePath']) -> Sequence['FilePath']:
        if not isinstance(_path, FilePath): _path = cls(_path)

        if _path.IsFile: return [cls(_path)]

        if not _path.IsDirectory: raise FileNotFoundError(f'path "{_path}" is not a valid directory.')

        def _join(file):
            return cls.Join(_path, file)

        return sorted(map(_join, listdir(_path)), key=lambda x: x.FullPath)

    @classmethod
    def Temporary(cls, *args: str, root_dir: str = None) -> 'FileIO':
        _path = cls.Join(root_dir or tempfile.gettempdir(), *args)
        _path._temporary = True
        return _path()

    @classmethod
    def Parse(cls, d) -> 'FilePath':
        if isinstance(d, dict):
            AssertKeys(d, 'FullPath')
            return cls(d['FullPath'])

        throw(d, dict)



_TFileData = TypeVar('_TFileData', bound='FileIO')
@attrs(slots=True, hash=True, order=True, eq=True, auto_attribs=True, frozen=True, collect_by_mro=True)
class FileIO(PathLike, Generic[_TFileData]):
    Path: FilePath = attrib(validator=validators.instance_of(FilePath))

    def Remove(self):
        return self.Path.Remove()
    def __del__(self):
        return self.Path.__del__()
    def __fspath__(self):
        return self.Path.__fspath__()
    def __bytes__(self):
        """ Return the bytes representation of the path. This is only recommended to use under Unix. """
        return bytes(self.Path)


    def GetFileData(self, file: ReadWriteData, *, Default: _TFileData = None, Check: callable = None, RemoveOnError: bool = False) -> _TFileData:
        try:
            with open(self, 'rb') as f:
                dat = file.load(f)
                if callable(Check): Check(dat)
                return dat
        except FileNotFoundError:
            return Default
        except (pickle.PickleError, pickle.PicklingError, json.JSONDecodeError):
            if RemoveOnError: self.Path.Remove()
            return Default
    def SetFileData(self, data: _TFileData, file: ReadWriteData, *, Check: callable = None):
        with open(self, 'wb') as f:
            if callable(Check): data = Check(data)
            return file.dump(data, f)


    def SaveJson(self, data: _TFileData, **kwargs):
        with open(self, 'w') as f:
            return json.dump(data, f, **kwargs)
    def ReadJson(self, **kwargs) -> _TFileData:
        with open(self, 'r') as f:
            return json.load(f, **kwargs)


    def SavePickle(self, data: Any, **kwargs):
        with open(self, 'wb') as f:
            return pickle.dump(data, f, **kwargs)
    def ReadPickle(self, **kwargs) -> Any:
        with open(self, 'rb') as f:
            return pickle.load(f, **kwargs)




    def Write(self, content: Union[str, bytes], **kwargs) -> int:
        if 'newline' not in kwargs: kwargs['newline'] = '\n'

        if isinstance(content, str):
            with open(self, 'w', **kwargs) as f:
                return f.write(content)

        elif isinstance(content, bytes):
            with open(self, 'wb', **kwargs) as f:
                return f.write(content)

        else:
            raise TypeError(type(content), (bytes, str))

    def Read(self) -> str:
        with open(self, 'r') as f:
            return f.read()
    def ReadBytes(self) -> bytes:
        with open(self, 'rb') as f:
            return f.read()




    async def WriteAsync(self, content: Union[str, bytes], **kwargs) -> int:
        if 'newline' not in kwargs: kwargs['newline'] = '\n'

        if isinstance(content, str):
            async with async_open(self, 'w', **kwargs) as f:
                return await f.write(content)

        elif isinstance(content, bytes):
            async with async_open(self, 'wb', **kwargs) as f:
                return await f.write(content)

        else:
            raise TypeError(type(content), (bytes, str))

    async def ReadAsync(self) -> str:
        async with async_open(self, 'r') as f:
            return await f.read()

    async def ReadBytesAsync(self) -> bytes:
        async with async_open(self, 'rb') as f:
            return await f.read()


    async def CopyToAsync(self, _outPath: FilePath):
        async with async_open(_outPath, 'wb') as out:
            async with async_open(self, 'rb') as _in:
                await out.write(await _in.read())



    @classmethod
    def TemporaryFile(cls, *sub_folders: str, _name: str, root_dir: str = None):
        return FilePath.Temporary(*sub_folders, _name, root_dir=root_dir)

    @classmethod
    def Create(cls, _path: Union[str, 'FilePath'], content: Union[str, bytes] = None, *,
               buffering=None, encoding: str = None, errors=None, newline: str = '\n', close_fd=True):
        os.makedirs(basename(_path), exist_ok=True)
        _path = cls(_path)
        _path.Write(content, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=close_fd)

        return Path

    @classmethod
    async def CreateAsync(cls, _path: Union[str, 'FilePath'], content: Union[str, bytes] = None, *,
                          buffering=None, encoding: str = None, errors=None, newline: str = '\n', close_fd=True, loop=None, executor=None):
        os.makedirs(basename(_path), exist_ok=True)
        _path = cls(_path)
        await _path.WriteAsync(content, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=close_fd, loop=loop, executor=executor)

        return Path



# key = Fernet.generate_key()
class Encryptor(object):
    __slots__ = ['_path', '_encoding', '_private_key', '_encrypter']
    # _KEY_FILE_ = paths.PASS_KEY_FILE_NAME
    def __init__(self, path: Union[str, Path, 'FilePath'], *, private_key: bytes, encoding: str = "utf-8"):
        self._path = FilePath.convert(path)
        self._encoding = encoding
        self._private_key = private_key
        self._encrypter = Fernet(self._private_key)


    @property
    def _locked(self):
        return isfile(self._lockFile)
    @property
    def _lockFile(self):
        return f'{self._path}.lock'

    def __enter__(self):
        while self._locked:
            pass

        with open(self._lockFile, 'w') as f:
            f.write(self._path)

        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clearLcok()
    def _clearLcok(self):
        if self._locked:
            remove(self._lockFile)


    def encode(self, s: str) -> bytes:
        return s.encode(self._encoding)
    def decode(self, s: bytes) -> str:
        return s.decode(self._encoding)


    @staticmethod
    def _from_json(s: Union[str, bytes, bytearray], **kwargs) -> Dict:
        try:
            return json.loads(s, **kwargs)
        except Exception:
            print('_____from__json_____', type(s), s, sep='\n\n', end='\n\n\n')
            raise
    @staticmethod
    def _to_json(s: Dict, **kwargs) -> str:
        return json.dumps(s, **kwargs)


    @staticmethod
    def _from_pickle(s: bytes) -> Dict:
        return pickle.loads(s)
    @staticmethod
    def _to_pickle(s: Dict) -> bytes:
        return pickle.dumps(s, protocol=pickle.HIGHEST_PROTOCOL)


    def _ReadFile(self) -> bytes:
        with open(self._path, 'rb') as f:
            return f.read()
    def _WriteFile(self, value: bytes):
        with open(self._path, 'wb') as f:
            return f.write(value)


    def DecryptFile(self) -> bytes:
        return self.Decode(self._ReadFile())
    def EncryptFile(self, value: bytes):
        return self._WriteFile(self.Encrypt(value))


    def ReadJson(self, **kwargs) -> Dict:
        return self._from_json(self._ReadFile(), **kwargs)
    def WriteJson(self, value: Dict, **kwargs):
        return self._WriteFile(self._to_json(value, **kwargs).encode())


    def ReadPickle(self) -> Dict:
        return self._from_pickle(self.DecryptFile())
    def WritePickle(self, value: Dict):
        return self.EncryptFile(self._to_pickle(value))



    def Encrypt(self, value: bytes) -> bytes:
        return self._encrypter.encrypt(value)
    def Decode(self, value: bytes = None) -> bytes:
        return self._encrypter.decrypt(value)



class MultiThreadedCopier(object):
    """
    Based on https://stackoverflow.com/a/64813422

src_dir = /path/to/src/dir
dest_dir = /path/to/dest/dir

with MultiThreadedCopier(max_threads=16) as copier:
    shutil.copytree(src_dir, dest_dir, copy_function=copier.copy)
    """
    __slots__ = ['pool', '_max_threads']
    def __init__(self, max_threads: int = os.cpu_count()): self._max_threads = max_threads
    def __enter__(self):
        self.pool = ThreadPool(self._max_threads)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()
        del self.pool

    def copy(self, source: Union[str, FilePath], dest: Union[str, FilePath]): return self.pool.apply_async(copy2, args=(source, dest))
