import threading
import time
from abc import ABC
from typing import Union




__all__ = ['AutoStartThread', 'AutoStartTargetedThread', 'Wait']

class AutoStartThread(threading.Thread, ABC):
    def __init__(self, *args, Name: str = None, AutoStart: bool = True, Daemon: bool = True, **kwargs):
        if not Name:
            try: Name = self.__class__.__qualname__
            except AttributeError: Name = self.__class__.__name__

        super().__init__(name=Name, args=args, kwargs=kwargs, daemon=Daemon)
        if AutoStart: self.start()
    def run(self): raise NotImplementedError()

class AutoStartTargetedThread(threading.Thread):
    def __init__(self, target: callable, *args, Name: str = None, AutoStart: bool = True, Daemon: bool = True, **kwargs):
        assert (callable(target))
        if not Name:
            try: Name = target.__qualname__
            except AttributeError: Name = target.__name__

        super().__init__(name=Name, target=target, args=args, kwargs=kwargs, daemon=Daemon)
        if AutoStart: self.start()


def Wait(delay: Union[int, float]): time.sleep(delay)
