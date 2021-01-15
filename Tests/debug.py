import json
import os
import string
import sys
import threading
import time
import tkinter as tk

from PythonDebugTools import *




def Test():
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
            time.sleep(delay)
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

if __name__ == '__main__':
    Test()
