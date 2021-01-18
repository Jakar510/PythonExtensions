import json
import os
import pickle
import tempfile
from os.path import *
from typing import *

from .Path import *




__all__ = [
    'File'
    ]


class File(object):
    def __init__(self, path: Path, *, temporary: bool = False):
        self._path = path
        self._temporary = temporary

    def Remove(self): return self._path.Remove()
    def __del__(self):
        if self._temporary: self.Remove()
    def __str__(self): return str(self._path)
    def __repr__(self):
        try: return f'<{self.__class__.__qualname__} Object. Location: "{self._path}">'
        except AttributeError: return f'<{self.__class__.__name__} Object. Location: "{self._path}">'


    def GetFileData(self, file: FileData, *, Default=None, Check: callable = None, RemoveOnError: bool = False):
        try:
            with open(self._path, 'rb') as f:
                dat = file.load(f)
                if callable(Check): Check(dat)
                return dat
        except FileNotFoundError: return Default
        except (pickle.PickleError, pickle.PicklingError, json.JSONDecodeError):
            if RemoveOnError: self._path.Remove()
            return Default
    def SetFileData(self, data: Any, file: FileData, *, Check: callable = None):
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


    def Write(self, content: Union[str, bytes] = None, *, newline: str = '\n', **kwargs) -> int:
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
    def TemporaryFile(cls, fileName: str, *sub_folders: str, root_dir: str = None):
        if not root_dir: root_dir = tempfile.gettempdir()
        path = Path.Join(root_dir, *sub_folders, fileName)
        os.makedirs(basename(path), exist_ok=True)
        return cls(path, temporary=True)

    @classmethod
    def Create(cls, _path: Union[str, 'Path'], content: Union[str, bytes] = None, *, buffering=None, encoding: str = None, errors=None, newline: str = '\n', closefd=True):
        os.makedirs(basename(_path), exist_ok=True)
        path = cls(os.path.abspath(_path))
        path.Write(content, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd)

        return path

    @staticmethod
    def CopyFile(_inPath: Union[str, 'Path'], _outPath: Union[str, 'Path'], open_as_binary: bool = False):
        with open(_outPath, 'wb' if open_as_binary else 'w') as out:
            with open(_inPath, 'rb' if open_as_binary else 'r') as _in:
                out.write(_in.read())



if __name__ == '__main__':
    _file = File.TemporaryFile('test.txt', 'BaseExtensions')
    print(_file)
    _file.Write('test data')
