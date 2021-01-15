import functools
import time
from tkinter import Event

from .console import *
from BaseExtensions.Helpers import RoundFloat




__all__ = ['Debug', 'CheckTime', 'CheckTimeWithSignature', 'DebugTkinterEvent', 'SimpleDebug', 'StackTrace', 'StackTraceWithSignature']


# def ClassMethodDebug(cls: str or type, tag: str = DEFAULT_TAG):
#     """
#         Print the function signature and return value
#
#     :param cls: class string or type to describe the method's parent or caller.
#     :param tag: a unique string to identify the output in the console window.
#     :return:
#     """
#     if isinstance(cls, type):
#         cls = cls.__name__
#
#     def debug_inner(func: callable = None):
#         """
#             Print the function signature and return value
#
#         :param func: callable function to be debugged.
#         :return:
#         """
#         name = f"{cls}.{func.__name__}"
#
#         @functools.wraps(func)
#         def wrapper_debug(*args, **kwargs):
#             if debug:
#                 Print(tag.format(name))
#                 if args or kwargs:
#                     try: args_repr = [repr(a) for a in args]  # 1
#                     except: args_repr = [str(a) for a in args]  # 1
#
#                     kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
#
#                     signature = ", ".join(args_repr + kwargs_repr)  # 3
#
#                     Print(f"{name}(\n      {signature}\n   )")
#             result = func(*args, **kwargs)
#             if debug: Print(f"{name}  returned  {result!r}\n")  # 4
#
#             return result
#         return wrapper_debug
#     return debug_inner


def SimpleDebug(func: callable):
    """
        Print the function signature and return value




    """
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        result = func(*args, **kwargs)
        if pp.can_print: return result
        name = GetFunctionName(func)
        start = f"--------- CALLED: {name}\n"
        _end = f"--------- ENDED: {name}\n"
        PRINT(start, _end)
        return result
    return wrapper_debug
def Debug(*, tag: str = pp.DEFAULT_TAG):
    """
        Print the function signature and return value

    :param tag: a unique string to identify the output in the console window.
    """

    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            result = func(*args, **kwargs)
            if pp.can_print: return result
            result, _tag, name, signature, pp_result = pp.get_func_details(func, tag, result, args, kwargs)
            Print(_tag, signature, f"{name}  returned  {pp_result}\n")

            return result
        return wrapper_debug
    return wrapper




def CheckTime(*, Precision: int = 5, tag: str = pp.TITLE_TAG):
    """




    :param Precision:
    :type Precision:
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def timed(*args, **kwargs):
            if pp.can_print: return func(*args, **kwargs)
            start_time = time.time()
            result = func(*args, **kwargs)
            _time = RoundFloat(time.time() - start_time, Precision=Precision)
            result, _tag, name, signature, pp_result =pp. get_func_details(func, tag, result, args, kwargs)
            Print(_tag, f'{name}  took:  {_time}')
            return result

        return timed
    return wrapper
def CheckTimeWithSignature(*, Precision: int = 5, tag: str = pp.TITLE_TAG):
    """




    :param Precision:
    :type Precision:
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def timed(*args, **kwargs):
            if pp.can_print: return func(*args, **kwargs)
            start_time = time.time()
            result = func(*args, **kwargs)
            _time = RoundFloat(time.time() - start_time, Precision=Precision)
            result, _tag, name, signature, pp_result = pp.get_func_details(func, tag, result, args, kwargs)
            _start = f'{name}  took:  {_time}'
            _end = f'{name} returned {pp_result}'
            Print(_start, signature, _end)
            return result

        return timed
    return wrapper



def DebugTkinterEvent(*, tag: str = pp.TITLE_TAG):
    """
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapper_debug(self, event: Event, *args, **kwargs):
            result = func(self, event, *args, **kwargs)
            if pp.can_print: return result
            name = GetFunctionName(func)
            _tag = tag.format(f'{name}')
            start = f'{name}.{event.__class__}'
            data = event.__dict__
            _end = f"{name}  returned  {pp.getPPrintStr(result)}"
            Print(_tag, start, data, _end)

            return result

        return wrapper_debug
    return wrapper




def StackTrace(*, INDENT=4 * ' ', tag: str = pp.TITLE_TAG):
    """
        Get all but last line returned by traceback.format_stack() which is the line below.




    :param INDENT:
    :type INDENT:
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            if pp.can_print: return result
            result, _tag, name, signature, pp_result = pp.get_func_details(func, tag, result, args, kwargs)
            callstack = CallStack(INDENT)
            call = f'{name}() called:'
            _end = f"{name}  returned  {pp.getPPrintStr(result)}"
            Print(_tag, call, callstack, _end)
            return result

        return wrapped
    return wrapper
def StackTraceWithSignature(*, INDENT=4 * ' ', tag: str = pp.TITLE_TAG):
    """
        Get all but last line returned by traceback.format_stack() which is the line below.




    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :param INDENT:
    :type INDENT:
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            if pp.can_print: return result
            result, _tag, name, signature, pp_result = pp.get_func_details(func, tag, result, args, kwargs)
            callstack = CallStack(INDENT)
            call = f'{name}() called: '
            _end = f"{name}  returned  {pp_result}"
            Print(_tag, call, signature, callstack, _end)
            return result

        return wrapped
    return wrapper
