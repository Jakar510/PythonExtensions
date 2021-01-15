import json

from Extensions.Images import ImageObject
from Extensions.Json import *
from Extensions.Logging import *

from Extensions.debug import *




def Test():
    pass
    # from TkinterExtensions.examples import run_all
    # run_all()

    # with open('test.txt', 'a+') as f: f.write(f.read())

    start = Point.Create(0, 0)
    end = Point.Create(150, 150)
    pic_pos = Point.Create(10, 10)
    img_size = Size.Create(200, 200)

    print(CropBox.BoxSize(start, end, pic_pos, img_size))

    t = (1, 2)
    print(json.dumps(img_size))

    with open('./BaseExtensions/ImageExtensions.py', 'w') as f:
        f.write('from enum import Enum\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('class ImageExtensions(str, Enum):\n')

        for item in ImageObject.Extensions():
            f.write(f"\t{item.replace('.', '')} = '{item}'\n")



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
    Test()
    TestLogging()
