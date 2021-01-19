from Tests import RUN_TESTS

from PythonExtensions.Files import *



if __name__ == '__main__':
    d = Path.MakeDirectories(Path.Join('.', 'temp'))
    print(d)
    print(d.FileName)
    print(d.extension())
    file = Path.Join(d, 't.txt')
    with open(file, 'w') as f: f.write(str(d))
    print(file)
    print(file.FileName)
    print(file.extension())

    file.Remove()
    d.Remove()

    RUN_TESTS()


