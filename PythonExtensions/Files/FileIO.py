import json
import os
import pickle
from os.path import *

from .FilePath import *
from ..Json import *
from ..Models import URL




__all__ = [
    'FileIO',
    'ReadWriteData'
    ]

class ReadWriteData(Protocol[AnyStr]):
    def load(self, f: BinaryIO) -> Any: ...
    def dump(self, data: AnyStr, f: BinaryIO) -> Any: ...

class FileIO(object):
    def __init__(self, path: Union[str, FilePath]):
        if not isinstance(path, FilePath):
            path = FilePath(path)

        self._path = path

    @property
    def path(self) -> FilePath: return self._path

    def Remove(self): return self._path.Remove()
    def __del__(self): return self._path.__del__()
    def __str__(self): return str(self._path)
    def __repr__(self):
        try: return f'<{self.__class__.__qualname__} Object. Location: "{self._path}">'
        except AttributeError: return f'<{self.__class__.__name__} Object. Location: "{self._path}">'


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
    def TemporaryFile(cls, *sub_folders: str, name: str, root_dir: str = None):
        path = FilePath.Temporary(*sub_folders, name, root_dir=root_dir)
        path.Create()
        return cls(path)

    @classmethod
    def Create(cls, _path: Union[str, 'FilePath'], content: Union[str, bytes] = None, *,
               buffering=None, encoding: str = None, errors=None, newline: str = '\n', closefd=True):
        os.makedirs(basename(_path), exist_ok=True)
        path = cls(abspath(_path))
        path.Write(content, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd)

        return path

    @staticmethod
    def CopyFile(_inPath: Union[str, 'FilePath'], _outPath: Union[str, 'FilePath'], open_as_binary: bool = False):
        with open(_outPath, 'wb' if open_as_binary else 'w') as out:
            with open(_inPath, 'rb' if open_as_binary else 'r') as _in:
                out.write(_in.read())
