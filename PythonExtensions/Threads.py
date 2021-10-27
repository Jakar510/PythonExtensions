import threading
import time
from abc import ABC
from asyncio import sleep
from typing import Union

from .Names import nameof




__all__ = ['AutoStartThread', 'AutoStartTargetedThread', 'Wait', 'WaitAsync']

class AutoStartThread(threading.Thread, ABC):
    __slots__ = []
    def __init__(self, *args, Name: str = None, AutoStart: bool = True, Daemon: bool = True, **kwargs):
        super().__init__(name=Name or nameof(self), args=args, kwargs=kwargs, daemon=Daemon)
        if AutoStart: self.start()
    def run(self): raise NotImplementedError()



class AutoStartTargetedThread(threading.Thread):
    __slots__ = []
    def __init__(self, target: callable, *args, Name: str = None, AutoStart: bool = True, Daemon: bool = True, **kwargs):
        assert (callable(target))
        if not Name: Name = nameof(target)

        super().__init__(name=Name, target=target, args=args, kwargs=kwargs, daemon=Daemon)
        if AutoStart: self.start()



def Wait(delay: Union[int, float]): time.sleep(delay)
async def WaitAsync(delay: Union[int, float], result=None, *, loop=None): await sleep(delay, result, loop=loop)
