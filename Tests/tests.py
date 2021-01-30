import json
import os
import random
import string
import sys
import threading
import time

from PythonExtensions.Files import *
from PythonExtensions.Images import ImageObject
from PythonExtensions.Json import *
from PythonExtensions.Logging import *
from PythonExtensions.Threads import *
from PythonExtensions.debug import *
from PythonExtensions.tk import *
import unittest



__all__ = [
    'Tests'
    ]

class Tests(unittest.TestCase):
    def test_Paths(self):
        d = FilePath.Join('.', 'temp')
        d.Create()
        print(d)
        print(d.FileName)
        print(d.Extension())
        file = FilePath.Join(d, 't.txt')
        with open(file, 'w') as f: f.write(str(d))
        print(file)
        print(file.FileName)
        print(file.Extension())

        file.Remove()
        d.Remove()

    def test_Image(self):
        root = tkRoot.Create(800, 480, fullscreen=False)
        frame = Frame(root).PlaceFull()
        label = Canvas(frame).PlaceFull()
        root.update()
        root.update_idletasks()

        # init = (1335, 1080)
        # RUN_TESTS()
        paths = FilePath.ListDir(r'D:\WorkSpace\SmartPhotoFrame\client\src\.images')
        path = random.choice(paths)
        with open(path, 'rb') as f:
            with ImageObject.open(f) as img:
                print('init: ', img.size)
                print('label: ', label.size)
                img = ImageObject(img, label.width, label.height)
                box = CropBox.Create(0, 0, label.width, label.height)
                img.CropZoom(box, size=(img.width, img.height))
                # img.Resize(box=box, check_metadata=False)
                # img.Resize(size=(2960 * 1.2, 1440 * 1.2), box=box, check_metadata=False)
                # img.Resize(check_metadata=False)

                x = int((label.width - img.Raw.width) / 2)
                y = int((label.height - img.Raw.height) / 2)
                print(dict(x=x, y=y))
                items = label.CreateImage(img.Raw, x, y)
                print(items)
        root.mainloop()

    def test_files(self):
        _file = FileIO.TemporaryFile('PythonExtensions', name='test.txt')
        _file.Write('test data')

        PrettyPrint(FilePath.ListDir('.'))

    def test_Boxes(self):
        # screen = Size.Create(1920, 1080)
        # screen = Size.Create(1366, 768)
        screen = Size.Create(3820, 2160)

        # img_size = Size.Create(1920, 1080)
        # start = Point.Create(0, 0)

        window = Size.Create(1920, 1080)

        for w in (2560,):  # 1024, 1366,  1920, 3820
            for h in (1600,):  # 768, 864, 1080, 2160
                for x in range(-1500, 500, 50):
                    for y in range(-750, 500, 50):
                        start = PlacePosition.Create(x, y)
                        img_size = Size.Create(w, h)

                        box = CropBox.FromPointSize(start, window)
                        box.Update(start, img=img_size, view=window)
                        # if box.IsAllVisible(start, img_size):
                        #     print('_______UPDATE______', w, h, window)

                        # box = CropBox.BoxSize(start, window, start, img_size)
                        if not box.IsAllVisible(start, img_size):
                            print('_______BOX______', start.ToTuple(), img_size.ToTuple(), box)
                            print()

                        # result = box.Scale(screen)
                        # print('__Scale__', result <= screen)

        # for x in range(-100, 100, 25):
        #     for y in range(-100, 100, 25):
        #         point = Point.Create(x, y)
        #
        #         print()
        #         box = CropBox.FromPointSize(start, window)
        #         box.Update(point, img=img_size, view=window)
        #         print('_______UPDATE______', x, y, box.IsAllVisible(point, img_size))
        #
        #
        #         box = CropBox.BoxSize(start, window, point, img_size)
        #         print('_______BOX______', x, y, box.IsAllVisible(point, img_size))
        #
        #         result = box.Scale(screen).ToTuple()
        #         print('__Scale__', result, result > screen)
        #         print()

    def test_Debug(self):
        _pp = Printer.Default()
        print('_pp is pp', _pp is pp)
        Printer.Set(_pp)
        print('_pp is pp', _pp is pp)



        class test(object):
            @Debug()
            def pp_run(self, *args, **kwargs):
                return args, kwargs

            @Debug()
            def run(self, *args, **kwargs):
                return args, kwargs

            @DebugTkinterEvent()
            def tk_run(self, event: tk.Event):
                return None

            @CheckTime()
            def timed(self, delay: int, *args, **kwargs):
                Wait(delay)
                return args, kwargs

            @CheckTimeWithSignature()
            def timed_sig(self, delay: int, *args, **kwargs):
                time.sleep(delay)
                return args, kwargs

            @StackTrace()
            def stack(self, *args, **kwargs):
                return args, kwargs

            @StackTrace()
            def stack_sig(self, *args, **kwargs):
                return args, kwargs


            @chain()
            def chain_root(self, *args, **kwargs):
                return self.sub1(*args, **kwargs)

            @sub()
            def sub1(self, *args, **kwargs):
                return self.sub2(*args, **kwargs)

            @sub()
            def sub2(self, *args, **kwargs):
                return 'chain.sub.end', args, kwargs



        def _json():
            print('_json')
            path = os.path.abspath(sys.argv[1])

            with open(path, 'r') as f:
                d = json.load(f)

            PRINT('__json__', d)

        _threads = []
        # _threads.append(threading.Thread(target=_json, daemon=True))
        t = test()



        def _t1():
            print('_t1')
            t.run()
            t.pp_run()
            t.timed(1)
            t.timed_sig(1)

            t.stack(1, 2, 3, test=True, print=False)
            t.stack_sig(1, 2, 3, test=True, print=True)

        _threads.append(threading.Thread(target=_t1, daemon=True))

        def _t2():
            print('_t2')
            evt = tk.Event()
            evt.widget = None
            evt.x = None
            evt.y = None
            t.tk_run(evt)

            t.stack(*string.ascii_lowercase)
            t.stack_sig(*string.ascii_uppercase)

            t.chain_root()
        _threads.append(threading.Thread(target=_t2, daemon=True))

        for _t in _threads:
            _t.start()
            _t.join()

        print('__fin__')

    def test_Logging(self):
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

    def test_TkApp(self):
        class Root(tkRoot): pass



        class App(BaseApp): pass



        class Main(BaseWindow): pass



        class Test(object): pass



        class Other(object): pass



        temp = FilePath.Join('.', 'logs')
        print(repr(temp))
        app = App(Test, Other, app_name='app', root_path=temp, Screen_Width=800, Screen_Height=480)
        home = Main(app.root, app).PlaceFull()

        app.start_gui()

    @staticmethod
    def Run():
        unittest.main()
