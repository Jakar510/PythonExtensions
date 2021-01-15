import functools
from typing import *

from BaseExtensions.AutoCounter import AutoCounter

from .console import *




__all__ = ['chain', 'sub']

_counter = AutoCounter()



def chain(start_tag: str = pp.TITLE_TAG, end_tag: str = pp.END_TAG, start: int = 1):
    """
        Print the function signature and return value

    :param start:
    :type start:
    :param end_tag: a unique string to identify the ENDING of the chain in the console window.
    :param start_tag: a unique string to identify the START of the chain in the console window.
    :return:
    """
    _counter.reset(start=start)
    def wrapped(func: callable):
        """
        :param func: callable function to be debugged.
        :return:
        """
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            name = GetFunctionName(func)
            tag = start_tag.format(name)
            signature = pp.getPPrintStr({ 'kwargs': kwargs, 'args': args, })
            _start = f'{name}(\n      {signature}\n   )'

            Print(pp.END_TAG, tag, _start)
            result = func(*args, **kwargs)
            _end = f'{name} returned: {pp.getPPrintStr(result)}\n'
            Print(_end, end_tag)

            return result
        return wrapper_debug
    return wrapped


def _print_chain_signature(func: callable, tag: str, level: Union[int, AutoCounter], signature: bool, result, args, kwargs):
    assert ('{0}' in tag)
    if signature and (args or kwargs):
        name = GetFunctionName(func)
        _tag = tag.format(f'{level} --> {name}')
        signature = pp.getPPrintStr({ 'args': args, 'kwargs': kwargs })
        Print(_tag, f'{name}(\n      {signature}\n   )', name, f'returned: \n{pp.getPPrintStr(result)}')
def sub(level: int = None, *, tag: str = '-------------- level: {0}', signature: bool = False):
    """
        Print the function signature [Optional] and return value.

    :param level: optional positive non-zero intenger
    :type level: int
    :param signature: for sub-level method chains, prints it's signature. defaults to False.
    # :param level: the call stack level. f() -> g() -> h() -> etc.
    :param tag: a unique string to identify the output in the console window. must have one '{0}' for str.format() support.
    :return:
    """

    def wrapped(func: callable):
        """
        :param func: callable function to be debugged.
        :return:
        """
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            result = func(*args, **kwargs)
            _print_chain_signature(func, tag, level or _counter(), signature, result, args, kwargs)
            return result
        return wrapper_debug
    return wrapped
