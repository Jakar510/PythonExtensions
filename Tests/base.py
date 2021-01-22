from PythonExtensions.Json import *
from PythonExtensions.Logging import *

from PythonExtensions.debug import *




def Test_base():
    start = Point.Create(0, 0)
    end = Point.Create(150, 150)
    pic_pos = Point.Create(10, 10)
    img_size = Size.Create(200, 200)

    print(CropBox.Box(start, end, pic_pos, img_size))



def TestLogging():
    class Test(object): pass



    class Other(object): pass



    m = LoggingManager.FromTypes(Test, Other, app_name='app', root_path='.')

    PrettyPrint(m.paths.Test)
    PrettyPrint(m.paths.Test_errors)

    PrettyPrint(m.paths.Other)
    PrettyPrint(m.paths.Other_errors)

    PrettyPrint('m.paths.logs', m.paths.logs)

    Print(m.CreateLogger(Test(), debug=True))
    Print(m.CreateLogger(Other(), debug=True))

    try: m.CreateLogger(Other, debug=True)
    except Exception as e: print_exception(e)



if __name__ == '__main__':
    Test_base()
    TestLogging()
