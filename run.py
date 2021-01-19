from Tests import RUN_TESTS

from PythonExtensions.Files import *



if __name__ == '__main__':
    # RUN_TESTS()

    d = Path.MakeDirectories(Path.Join('.', 'temp', 'py'))
    d = Path.Join(d, 't.txt')
    print(d)
    print(d.FileName)
    print(d.extension())

