import random
import string
import threading
import time
import unittest
from os.path import abspath

from PythonExtensions.Files import *
from PythonExtensions.Images import ImageObject
from PythonExtensions.Json import *
from PythonExtensions.Logging import *
from PythonExtensions.Names import nameof
from PythonExtensions.Threads import *
from PythonExtensions.debug import *
from PythonExtensions.tk import *




__all__ = [
    'FileIO_TestCase',
    'FilePath_TestCase',
    'Debug_TestCase',
    'Logging_TestCase',
    'TkApp_TestCase',
    ]

class FilePath_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return cls()

    @classmethod
    def tearDownClass(cls):
        return cls()


    def setUp(self) -> None:
        pass
    def tearDown(self):
        pass


    def test_FilePaths(self):
        temp = FilePath.Join('.', 'logs')
        self.assertEqual(temp.FullPath, abspath('./logs'))


    def test_Paths(self):
        d = FilePath.Join('.', 'temp')
        d()

        self.assertTrue(d.IsDirectory)
        self.assertFalse(d.IsFile)

        self.assertIsNone(d.Extension())
        self.assertIsNone(d.FileName)

        file = FilePath.Join(d, 't.txt')
        with open(file, 'w') as f: f.write(str(d))
        self.assertIsNotNone(file.FileName)
        self.assertIsNotNone(file.Extension())

        file.Remove()
        d.Remove()


# noinspection PyMethodMayBeStatic
class FileIO_TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_Image(self):
        root = tkRoot.Create(800, 480, fullscreen=False)
        frame = Frame(root).PlaceFull()
        label = Canvas(frame).PlaceFull()
        root.update()
        root.update_idletasks()

        paths = FilePath.ListDir(r'D:\WorkSpace\SmartPhotoFrame\client\src\.images')
        path = random.choice(paths)
        with open(path, 'rb') as f:
            with ImageObject.open(f) as img:
                print('init: ', img.size)
                print('label: ', label.size)
                img = ImageObject(img, label.Width, label.Height)
                box = CropBox(0, 0, label.Width, label.Height)
                img.CropZoom(box, size=(img.Width, img.Height))

                x = int((label.Width - img.Raw.Width) / 2)
                y = int((label.Height - img.Raw.Height) / 2)
                print(dict(x=x, y=y))
                items = label.CreateImage(img.Raw, x, y)
                print(items)

        root.after(2000, root.destroy)
        root.mainloop()

    def test_files(self):
        _file = FileIO.TemporaryFile('PythonExtensions', _name='test.txt')
        _file.Write('test data')

        PrettyPrint(FilePath.ListDir('.'))

    def test_Boxes(self):
        screen = Size(3820, 2160)
        window = Size(1920, 1080)

        for w in (2560,):  # 1024, 1366,  1920, 3820
            for h in (1600,):  # 768, 864, 1080, 2160
                for x in range(-1500, 500, 50):
                    for y in range(-750, 500, 50):
                        start = PlacePosition(x, y)
                        img_size = Size(w, h)

                        box = CropBox.FromPointSize(start, window)
                        box.Update(start, img=img_size, view=window)

                        if not box.IsAllVisible(start, img_size):
                            (start.ToTuple(), img_size.ToTuple(), box)


class Debug_TestCase(unittest.TestCase):
    class test(object):
        @Debug()
        def pp_run(self, *args, **kwargs):
            return args, kwargs

        @Debug()
        def run(self, *args, **kwargs):
            return args, kwargs

        @DebugTkinterEvent()
        def tk_run(self, _event: tk.Event):
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



    @classmethod
    def setUpClass(cls):
        return cls()

    @classmethod
    def tearDownClass(cls):
        return cls()


    def setUp(self) -> None:
        self.t = self.test()

    def tearDown(self):
        pass

    def _t1(self):
        print('_t1')
        self.t.run()
        self.t.pp_run()
        self.t.timed(1)
        self.t.timed_sig(1)

        self.t.stack(1, 2, 3, test=True, print=False)
        self.t.stack_sig(1, 2, 3, test=True, print=True)
    def _t2(self):
        evt = tk.Event()
        evt.widget = None
        evt.x = None
        evt.y = None
        self.t.tk_run(evt)

        self.t.stack(*string.ascii_lowercase)
        self.t.stack_sig(*string.ascii_uppercase)

        self.t.chain_root()

    def test_Debug(self):
        global pp
        _pp = Printer.Default()
        self.assertFalse(_pp is pp)
        pp = Printer.Set(_pp)
        self.assertTrue(_pp is pp)

        self._threads = []

        self._threads.append(threading.Thread(target=self._t1, daemon=True))
        self._threads.append(threading.Thread(target=self._t2, daemon=True))

        for _t in self._threads:
            _t.start()
            _t.join()


class Logging_TestCase(unittest.TestCase):
    class Test(object): pass



    class Other(object): pass



    def setUp(self):
        self.temp = FilePath.Temporary('logs', root_dir='.')
        self.lm = LoggingManager.FromTypes(self.Test, self.Other, app_name=nameof(self), root_path=self.temp.FullPath)

    def tearDown(self):
        del self.lm

    def test_Logging(self):
        PrettyPrint(self.lm.paths.Test)
        PrettyPrint(self.lm.paths.Test_errors)

        PrettyPrint(self.lm.paths.Other)
        PrettyPrint(self.lm.paths.Other_errors)

        PrettyPrint('self.lm.paths.logs', self.lm.paths.logs)

        self.t = self.lm.CreateLogger(self.Test(), debug=True)
        self.o = self.lm.CreateLogger(self.Other(), debug=True)

    def test_CreateLogger(self):
        with self.assertRaises(ValueError):
            self.lm.CreateLogger(self.Other, debug=True)

        PrettyPrint(FilePath.ListDir(self.temp.FullPath))

        PrettyPrint(state=self.temp.__state__())


class TkApp_TestCase(unittest.TestCase):
    class Root(tkRoot): pass



    class App(BaseApp): pass



    class Main(BaseWindow): pass



    class Test(object): pass



    class Other(object): pass



    def setUp(self):
        self.temp = FilePath.Temporary('logs', root_dir='.')
        self.lm = LoggingManager.FromTypes(self.__class__, self.Test, self.Other, app_name=nameof(self), root_path=self.temp.FullPath)

    def tearDown(self):
        del self.lm
        del self.temp
        del self.home
        del self.app

    def test_TkApp(self):
        temp = FilePath.Join('.', 'logs')

        self.app = self.App(self.Test, self.Other, app_name='app', root_path=temp, Screen_Width=800, Screen_Height=480)
        self.home = self.Main(self.app.root, self.app).PlaceFull()

        self.app.root.after(2000, self.app.Close)
        self.app.start_gui()


class TkAppAsync_TestCase(unittest.TestCase):
    class Root(tkRoot): pass



    class App(BaseApp): pass



    class Main(BaseWindow): pass



    class Test(object): pass



    class Other(object): pass



    def setUp(self):
        self.temp = FilePath.Temporary('logs', root_dir='.')
        self.lm = LoggingManager.FromTypes(self.__class__, self.Test, self.Other, app_name=nameof(self), root_path=self.temp.FullPath)

    def tearDown(self):
        del self.lm
        del self.temp
        del self.home
        del self.app

    def test_TkApp(self):
        temp = FilePath.Join('.', 'logs')

        self.app = self.App(self.Test, self.Other, app_name='app', root_path=temp, Screen_Width=800, Screen_Height=480)
        self.home = self.Main(self.app.root, self.app).PlaceFull()

        self.app.root.after(2000, self.app.Close)
        self.app.start_gui_Async()
