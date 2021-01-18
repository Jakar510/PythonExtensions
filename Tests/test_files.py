from PythonExtensions.Files import *
from PythonExtensions.debug import *




__all__ = ['test_files']

def test_files():
    _file = File.TemporaryFile('PythonExtensions', name='test.txt')
    _file.Write('test data')

    PrettyPrint(Path.ListDir('.'))
