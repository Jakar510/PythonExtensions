from itertools import count
from typing import Iterator




__all__ = ['AutoCounter']

class AutoCounter(object):
    _counter: Iterator[int]
    _next: callable
    def __init__(self, *, start: int = 0, step: int = 1):
        self._value = start
        self.reset(start=start, step=step)
    def __call__(self, *args, **kwargs) -> int:
        self._value = self._next()
        return self._value
    @property
    def value(self) -> int: return self._value
    def reset(self, *, start: int = 0, step: int = 1):
        self._counter = count(start=start, step=step)
        self._next = self._counter.__next__

    def __str__(self): return str(self._value)
    def __repr__(self): return f'<{self.__class__.__name__}, value: {self._value}>'
