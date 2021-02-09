import re
import sys
from itertools import count
from types import FunctionType, MethodType
from typing import Iterator, Union

from ..nameof import nameof




__all__ = [
    'CalculateOffset', 'RoundFloat',
    'IsMethod', 'IsFunction',
    'IsAttributePrivate',
    'get_size', 'sizeof',
    'AutoCounter', 'lazy_property',
    ]

def RoundFloat(Float: float, Precision: int) -> str:
    """ Rounds the Float to the given Precision and returns It as string. """
    return f"{Float:.{Precision}f}"

def CalculateOffset(starting: Union[int, float], *args: Union[int, float]) -> int:
    """
        Example: WrapLength = ScreenWidth * Widget.Parent.relwidth * Widget.relwidth * offset

    :param starting: starting value (such as width or height)
    :param args: a list of float or integers to be cumulatively multiplied together.
    :return:
    """
    for arg in args:
        if not isinstance(arg, (int, float)): arg = float(arg)
        starting *= arg
    return int(starting)



def IsMethod(o) -> bool:
    """
        Checks if passed object is a method

        https://stackoverflow.com/questions/37455426/advantages-of-using-methodtype-in-python
    :param o: object being checked
    :type o: any
    :return: weather it is a method
    :rtype: bool
    """
    return isinstance(o, MethodType)
def IsFunction(o) -> bool:
    """
        Checks if passed object is a function

        https://stackoverflow.com/questions/37455426/advantages-of-using-methodtype-in-python
    :param o: object being checked
    :type o: any
    :return: weather it is a method
    :rtype: bool
    """
    return isinstance(o, FunctionType)




private_or_special_function_searcher = re.compile(r"(^__\w+$)|(^_\w+$)|(^__\w+__$)")

def IsAttributePrivate(attr_name: str) -> bool: return private_or_special_function_searcher.search(attr_name) is not None



def get_size(obj, seen: set = set()):
    """ Recursively finds size of objects """
    size = sys.getsizeof(obj)
    if seen is None: seen = set()

    obj_id = id(obj)
    if obj_id in seen: return 0

    # Important mark as seen *before* entering recursion to gracefully handle self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])

    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)

    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])

    return size


def sizeof(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, dict): return size + sum(map(sizeof, obj.keys())) + sum(map(sizeof, obj.values()))
    if isinstance(obj, (list, tuple, set, frozenset)): return size + sum(map(sizeof, obj))
    return size



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
    def __repr__(self): return f'<{nameof(self)}, value: {self._value}>'




class lazy_property(object):
    """A @property that is only evaluated once."""
    def __init__(self, func: callable, name: str = None, doc: str = None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self._func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        value = self._func(obj)
        setattr(obj, self._func.__name__, value)
        return value
