from PythonExtensions.Files import *
from PythonExtensions.Logging import *

from PythonExtensions.debug import *
from PythonExtensions.Threads import *




def TestLogging():
    class Test(object): pass

    class Other(object): pass


    temp = FilePath.Temporary('logs', root_dir='.')
    m = LoggingManager.FromTypes(Test, Other, app_name='app', root_path=temp)

    PrettyPrint(m.paths.Test)
    PrettyPrint(m.paths.Test_errors)

    PrettyPrint(m.paths.Other)
    PrettyPrint(m.paths.Other_errors)

    PrettyPrint('m.paths.logs', m.paths.logs)

    t = m.CreateLogger(Test(), debug=True)
    o = m.CreateLogger(Other(), debug=True)

    try: m.CreateLogger(Other, debug=True)
    except Exception as e:
        Print('-------------THIS IS EXPECTED-------------')
        o.exception(e)

    PrettyPrint('__ListDir__', FilePath.ListDir(temp))

    print('__state__')
    PrettyPrint(state=temp.__state__())

    print('Waiting....')
    Wait(3)
    del m
    print('__Exit__')


if __name__ == '__main__':
    TestLogging()
