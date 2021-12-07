import functools
import re
import sys
import time
import tkinter as tk
import traceback
from abc import ABC
from pprint import PrettyPrinter
from threading import Lock
from tkinter import Event
from types import TracebackType
from typing import *

from ..Core.Misc import AutoCounter, RoundFloat
from ..Core.Names import nameof




__all__ = [
    'chain',
    'sub',
    # 'getPPrintStr',  'check', 'get_func_details', 'print_signature'
    'PRINT',
    'Print',
    'print_exception',
    'print_stack_trace',
    'PrettyPrint',
    'Printer',
    'pp',
    'CallStack',
    'GetFunctionName',
    'GetFuncModule',
    'IsAttributePrivate',
    'ObjectToDict',
    'DebugWidget',
    'DebugWidgetRecursively',
    'Debug',
    'CheckTime',
    'CheckTimeWithSignature',
    'DebugTkinterEvent',
    'SimpleDebug',
    'StackTrace',
    'StackTraceWithSignature'
    ]

class NoStringWrappingPrettyPrinter(PrettyPrinter, ABC):
    """
        https://stackoverflow.com/questions/31485402/can-i-make-pprint-in-python3-not-split-strings-like-in-python2
        https://stackoverflow.com/a/31485450/9530917
    """

    @classmethod
    def Create(cls):
        return cls(indent=4, sort_dicts=False)

    # noinspection PyProtectedMember, PyUnresolvedReferences
    def _format(self, o, *args):
        if isinstance(o, (str, bytes, bytearray)):
            width = self._width
            self._width = sys.maxsize
            try:
                return super()._format(o, *args)
            finally:
                self._width = width

        elif isinstance(o, CallStack):
            print('__CallStack__', o, *args)
            # super()._format(o.Lines, *args)
            return super()._format(str(o), *args)

        else:
            return super()._format(o, *args)

class CallStack(object):
    _lines: Iterable[str] = None
    def __init__(self, indent: str = 4 * ' ', *, once: bool = True):
        self._indent = indent
        self._once = once
        self.Update()

    def Update(self):
        if self._once and self._lines is not None: raise RuntimeError()

        self._lines = [self._indent + line.strip() for line in traceback.format_stack()][:-1]

    @property
    def Lines(self) -> Iterable[str]:
        if self._lines is None: self.Update()
        return self._lines
    def __str__(self) -> str:
        return '\n'.join(self.Lines)
    # def __repr__(self) -> str: return '\n'.join(self.Lines)



class Printer(object):
    DEFAULT_TAG = '\n______________________________________________________________\n"{0}"'
    TITLE_TAG = "\n ---------------- {0} ---------------- \n"
    END_TAG = '\n ============================================================= \n'

    _lock = Lock()
    _active: bool = False
    def __init__(self, _pp: PrettyPrinter = None, *, use_double_quotes: bool, end: str, file=None):
        """
        :param end: string to append to end of passed args
        :type end: str
        :param file: file to write to
        :type file: file
        :param _pp: any PrettyPrinter implementation. provide your own to customize the output.
        :type _pp: PrettyPrinter
        :param use_double_quotes: use double quotes (") instead of the default single quotes (')
        :type use_double_quotes: bool
        """
        self._file = file
        self._end = end
        self._use_double_quotes = use_double_quotes
        self._pp = _pp or NoStringWrappingPrettyPrinter.Create()

    @property
    def can_print(self) -> bool:
        return __debug__

    def __enter__(self):
        self._active = True
        self._lock.__enter__()
        return self
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> Optional[bool]:
        self._active = False
        return self._lock.__exit__(exc_type, exc_val, exc_tb)


    def print(self, *args):
        if self.can_print:
            if self._active:
                return print(*args, sep='\n', end=self._end, file=self._file)

            with self:
                return print(*args, sep='\n', end=self._end, file=self._file)

    @overload
    def PrettyPrint(self, *args):
        ...
    @overload
    def PrettyPrint(self, title: str, *args):
        ...
    @overload
    def PrettyPrint(self, **kwargs):
        ...
    @overload
    def PrettyPrint(self, title: str, **kwargs):
        ...

    @staticmethod
    def _PrettyPrint(obj, *args, **kwargs):
        assert (isinstance(obj, Printer))
        if kwargs:
            if args and isinstance(args[0], str):
                title = args[0]
                obj.print(title)
                obj._pp.pprint(kwargs)

            else:
                obj._pp.pprint(kwargs)

        elif args:
            if isinstance(args[0], str):
                title = args[0]
                args = args[1:]
                obj.print(title)
                obj._pp.pprint(args)

            else:
                obj._pp.pprint(args)
    def PrettyPrint(self, *args, **kwargs):
        if self.can_print:
            if self._active:
                self._PrettyPrint(self, *args, **kwargs)

            else:
                with self as p:
                    self._PrettyPrint(p, *args, **kwargs)



    def getPPrintStr(self, o: any) -> str:
        """
        :param o: object to be serialized
        :type o: any
        :return: formatted string of the passed object
        :rtype: str
        """
        s = self._pp.pformat(o)
        if self._use_double_quotes: s = s.replace("'", '"')
        return s


    def print_exception(self, e: Exception, limit=None, file=None, _chain=True):
        """Print exception up to 'limit' stack trace entries from 'tb' to 'file'.

        This differs from print_tb() in the following ways: (1) if
        traceback is not None, it prints a header "Traceback (most recent
        call last):"; (2) it prints the exception type and value after the
        stack trace; (3) if type is SyntaxError and value has the
        appropriate format, it prints the line where the syntax error
        occurred with a caret on the next line indicating the approximate
        position of the error.
        """
        if self.can_print:
            if self._active:
                return traceback.print_exception(type(e), e, e.__traceback__, limit, file, _chain)

            with self._lock:
                return traceback.print_exception(type(e), e, e.__traceback__, limit, file, _chain)

    def print_stack_trace(self, f=None, limit=None, file=None):
        """Print a stack trace from its invocation point.

        The optional 'f' argument can be used to specify an alternate
        stack frame at which to start. The optional 'limit' and 'file'
        arguments have the same meaning as for print_exception().
        """
        if self.can_print:
            if self._active:
                traceback.print_stack(f, limit, file)
                return print()

            with self._lock:
                traceback.print_stack(f, limit, file)
                return print()


    def get_func_details(self, func: callable, tag: str, result: Any, args, kwargs) -> Tuple[Any, str, str, str, str]:
        """
        :param result: result of the passed function or method
        :type result: Any
        :param func: function or method being called
        :type func: callable
        :param tag: line to print before function/method details
        :type tag: str
        :param args: args passed to function/method
        :param kwargs: keyword args passed to function/method
        :return: result, tag, name, signature, pp_result
        :rtype: Tuple[Any, str, str, str, str]
        """
        assert ('{0}' in tag)

        name = GetFunctionName(func)
        tag = tag.format(name)
        signature = self.getPPrintStr({ 'args': args, 'kwargs': kwargs })
        pp_result = self.getPPrintStr(result)

        return result, tag, name, signature, pp_result

    def print_signature(self, func: callable, tag: str, *args, **kwargs):
        if self.can_print:
            assert ('{0}' in tag)

            result = func(*args, **kwargs)
            result, _tag, name, signature, pp_result = self.get_func_details(func, tag, result, args, kwargs)
            self.print(tag, f'{name}(\n      {signature}\n   )', name, f'returned: \n{self.getPPrintStr(result)}')

            return result

    @classmethod
    def Default(cls):
        return cls(use_double_quotes=True, end='\n\n')

    @staticmethod
    def Set(_pp):
        """
        :param _pp: Printer class instance to be used for all printing.
        :type _pp: Printer
        """
        if not isinstance(_pp, Printer): raise TypeError(type(_pp), (Printer,))
        global pp
        pp = _pp
        return pp



pp: Printer = Printer.Default()

# ------------------------------------------------------------------------------------------


_private_or_special_function_searcher = re.compile(r"(^__\w+$)|(^_\w+$)|(^__\w+__$)")
def IsAttributePrivate(attr_name: str) -> bool:
    return _private_or_special_function_searcher.search(attr_name) is not None


def ObjectToDict(Object: any, Skip: list or tuple = (), *, ShowAll: bool = False, IncludeCallable: bool = False) -> dict:
    """
        Returns a dictionary of the public attributes of the given object provided;
        Filter out private or special functions (_private, __SuperPrivate, __special__).

    :param IncludeCallable: doesn't include functions by default.
    :param ShowAll: remove all filters and show entire object.
    :param Skip:  list of names to skip. i.e. certain method names when IncludeCallable is True.
    :param Object: the thing being inspected.
    :return:
    """
    temp = { }
    for key in dir(Object):
        if key in Skip: continue
        if ShowAll or IsAttributePrivate(key):
            temp[key] = getattr(Object, key)
            if IncludeCallable and callable(temp[key]):
                del temp[key]
    return temp


# ------------------------------------------------------------------------------------------


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
def sub(level: int = _counter(), *, tag: str = '-------------- level: {0}', signature: bool = False):
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
            _print_chain_signature(func, tag, level, signature, result, args, kwargs)
            return result
        return wrapper_debug
    return wrapped


# ------------------------------------------------------------------------------------------


def GetFuncModule(func: callable) -> str: return func.__module__
def GetFunctionName(func: callable) -> str:
    if hasattr(func, '__qualname__') and hasattr(func, '__module__'):
        return f"{func.__module__}.{func.__qualname__}"
    elif hasattr(func, '__qualname__'):
        return func.__qualname__
    else:
        return func.__name__



def PRINT(title: str, *args, tag: str = pp.TITLE_TAG, **kwargs):
    """
    :param tag: identifer to seprate calls
    :type tag: str
    :param title: message to start the Print, to make it easier to find it.
    :type title: str
    """
    with pp as p:
        p.print(tag.format(title))
        return p.PrettyPrint(dict(args=args, kwargs=kwargs))



def Print(*args):
    with pp as p:
        return p.print(*args)


def print_exception(e: Exception, limit=None, file=None, _chain=True):
    with pp as p:
        return p.print_exception(e, limit, file, _chain)


def print_stack_trace(f=None, limit=None, file=None):
    with pp as p:
        return p.print_stack_trace(f, limit, file)



@overload
def PrettyPrint(*args): ...
@overload
def PrettyPrint(title: str, *args): ...
@overload
def PrettyPrint(**kwargs): ...
@overload
def PrettyPrint(title: str, **kwargs): ...

def PrettyPrint(*args, **kwargs):
    with pp as p:
        return p.PrettyPrint(*args, **kwargs)


# ------------------------------------------------------------------------------------------


def _rootLevelDataRecursive(w) -> Dict[str, Any]:
    return _WidgetDataRecursive(w)
def _WidgetDataRecursive(w) -> Dict[str, Any]:
    from ..tk.Base import BaseTkinterWidget

    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    return {
        'Type':                     w.__class__,
        'str(w)':                   str(w),
        'repr(w)':                  repr(w),
        'PI (position info)':       w.pi,
        # 'master.children':            w.master.children,
        'children':                 w.children,
        'winfo_id':                 w.winfo_id(),
        'winfo_name':               w.winfo_name(),
        'winfo_parent':             w.winfo_parent(),
        'winfo_manager':            w.winfo_manager(),
        'winfo_ismapped':           w.winfo_ismapped(),
        'winfo_pathname(winfo_id)': w.winfo_pathname(w.winfo_id()),
        'winfo_children':           _childData(w.winfo_children()),
        }


def _childData(obj: Union[List, Dict]):
    if isinstance(obj, dict):
        r = { }
        for key, w in obj:
            print('type(w)', type(w))
            print('type(key)', type(key))
            r[key] = _WidgetDataRecursive(w)
        return r

    if isinstance(obj, list):
        r = []
        for w in obj:
            print('type(w)', type(w))
            r.append((w.winfo_id(), _WidgetDataRecursive(w)))
        return dict(r)

    return obj
def DebugWidgetRecursively(w, *, Message: str):
    from ..tk.Base import BaseTkinterWidget

    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    print(f'---------------- {Message} < {nameof(w)} > ----------------')
    pp.PrettyPrint(_rootLevelDataRecursive(w))
    print()
    print()


def _rootLevelData(w, root: Union[tk.Tk, tk.Toplevel]) -> Dict[str, Any]:
    return {
        'root.children': root.children,
        # f'Widget: {w.__class__.__name__}':        _WidgetData(w)
        'Widget':        _WidgetData(w)
        }
def _WidgetData(w) -> Dict[str, Any]:
    from ..tk.Base import BaseTkinterWidget

    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    return {
        'Type':                     w.__class__,
        'str(w)':                   str(w),
        'repr(w)':                  repr(w),
        'PI (position info)':       w.pi,
        'master.children':          w.root.children,
        'children':                 w.children,
        'winfo_id':                 w.winfo_id(),
        'winfo_name':               w.winfo_name(),
        'winfo_parent':             w.winfo_parent(),
        'winfo_manager':            w.winfo_manager(),
        'winfo_ismapped':           w.winfo_ismapped(),
        'winfo_pathname(winfo_id)': w.winfo_pathname(w.winfo_id()),
        'winfo_children':           w.winfo_children(),
        }
def DebugWidget(w, *, root: Union[tk.Tk, tk.Toplevel], Message: str):
    from ..tk.Base import BaseTkinterWidget

    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))

    print(f'---------------- {Message} < {w.__class__.__name__} > ----------------')
    pp.PrettyPrint(_rootLevelData(w, root))
    print()
    print()


# ------------------------------------------------------------------------------------------


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
            result, _tag, name, signature, pp_result = pp.get_func_details(func, tag, result, args, kwargs)
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
