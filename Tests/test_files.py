from PythonExtensions.Files import *
from PythonExtensions.debug import *




__all__ = ['test_files']

def test_files():
    _file = FileIO.TemporaryFile('PythonExtensions', name='test.txt')
    _file.Write('test data')

    PrettyPrint(FilePath.ListDir('.'))
