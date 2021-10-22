# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
import asyncio
import base64
import tkinter as tk
from abc import ABC
from asyncio import BaseEventLoop, iscoroutine
from enum import Enum
from io import BytesIO
from os.path import isfile
from tkinter import Event as tkEvent, ttk
from types import FunctionType, MethodType
from typing import *
from typing import BinaryIO

from PIL.Image import Image, open as _img_open
from PIL.ImageTk import PhotoImage
from aiofiles import open as async_file_open
from aiofiles.threadpool.binary import AsyncBufferedReader
from aiohttp import ClientResponse, ClientSession
from requests import get
from yarl import URL

from PythonExtensions import ArgumentError
from ..Enumerations import *
from ..Events import Bindings
from ...Files import FilePath
from ...Names import nameof
from ...debug import pp




__all__ = [
    'BaseTkinterWidget', 'BaseTextTkinterWidget',
    'CommandMixin', 'ImageMixin',
    'CurrentValue', 'CallWrapper',
    'tk', 'ttk', 'tkEvent', 'URL',
    'img_open', 'tkPhotoImage'
    ]

class BindingCollection(dict, Dict[Bindings, Set[str]]):
    def __getitem__(self, item: Bindings):
        try:
            return super(BindingCollection, self).__getitem__(item)
        except KeyError:
            self[item] = set()
            return super(BindingCollection, self).__getitem__(item)
    def Clear(self):
        for _set in self.values(): _set.clear()
        self.clear()
    __del__ = Clear


class BaseTkinterWidget(tk.Widget, ABC):
    # noinspection PyMissingConstructor
    def __init__(self, Color: Optional[Dict[str, str]], loop: Optional[asyncio.BaseEventLoop]):
        if Color: self.configure(**Color)
        self._loop: Final[Optional[asyncio.BaseEventLoop]] = loop

    __bindings__: BindingCollection = BindingCollection()
    _state_: ViewState = ViewState.Hidden
    _pi: Dict = { }
    _manager_: Layout = None
    _wrap: int = None
    _cb: str or None = None
    @property
    def pi(self) -> dict: return self._pi.copy()

    @property
    def IsVisible(self) -> bool: return self._state_ != ViewState.Hidden

    @property
    def CurrentViewState(self) -> ViewState: return self._state_

    def ToString(self, IncludeState: bool = None) -> str:
        start = self.__repr__().replace('>', '').replace('<', '').replace('object', 'Tkinter Widget')
        if IncludeState is None: return f'<{start}. State: {pp.getPPrintStr(self.Details)}>'
        if IncludeState: return f'<{start}. State: {pp.getPPrintStr(self.FullDetails)}>'

        return f'<{start}>'
    @property
    def Details(self) -> dict: return dict(IsVisible=self.IsVisible)
    @property
    def FullDetails(self) -> dict:
        d = self.Details
        d.update({
            'Type':               type(self),
            'repr':               repr(self),
            'str':                str(self),
            'ViewState':          self.CurrentViewState,
            'LayoutManger':       self._manager_,
            'children':           self.children.copy(),
            'PI (position info)': self.pi,
            'dir':                dir(self),
            '__dict__':           self.__dict__.copy(),
            'winfo':              {
                'name':               self.winfo_name(),
                'manager':            self.winfo_manager(),
                'id':                 self.winfo_id(),
                'parent':             self.winfo_parent(),
                'ismapped':           self.winfo_ismapped(),
                'pathname(winfo_id)': self.winfo_pathname(self.winfo_id()),
                'children':           self.winfo_children(),
                },
            })
        return d



    @property
    def size(self) -> Tuple[int, int]: return self.width, self.height
    @property
    def width(self) -> int: return self.winfo_width()
    @property
    def height(self) -> int: return self.winfo_height()

    @property
    def x(self) -> int: return self.winfo_rootx()
    @property
    def y(self) -> int: return self.winfo_rooty()


    @overload
    def show(self) -> bool: ...
    @overload
    def show(self, TakeFocus: bool) -> bool: ...
    @overload
    def show(self, TakeFocus: bool, State: ViewState) -> bool: ...

    def show(self, **kwargs) -> bool:
        """
        Shows the current widget or _root_frame, based on the current geometry manager.
        Can be overridden to add additional functionality if needed.
        """
        if self._manager_ is None: return False

        state = kwargs.get('State', ViewState.Normal)
        assert (isinstance(state, ViewState))

        if 'TakeFocus' in kwargs: self.focus_set()

        if self._manager_ == Layout.pack:
            self.pack(self._pi)
            return self._show(state)

        elif self._manager_ == Layout.grid:
            self.grid(self._pi)
            return self._show(state)

        elif self._manager_ == Layout.place:
            self.place(self._pi)
            return self._show(state)

        return False
    def _show(self, state: ViewState) -> bool:
        assert (isinstance(state, ViewState))
        self._SetState(state)
        self._cb = self.after(10, self.OnAppearing)
        return True

    @overload
    def hide(self) -> bool: ...
    @overload
    def hide(self, parent: tk.Widget) -> bool: ...

    def hide(self, parent: tk.Widget = None) -> bool:
        """
        Hides the current widget or _root_frame, based on the current geometry manager.
        Can be overridden to add additional functionality if needed.
        """
        if self._manager_ is None: return False

        if parent: parent.focus_set()

        self.OnDisappearing()
        if self._manager_ == Layout.pack:
            self.pack_forget()
            return self._hide()

        elif self._manager_ == Layout.grid:
            self.grid_forget()
            return self._hide()

        elif self._manager_ == Layout.place:
            self.place_forget()
            return self._hide()

        return False
    def _hide(self) -> bool:
        self._SetState(state=ViewState.Hidden)
        return True

    @staticmethod
    def convert_kwargs(kwargs: dict, lower: bool = True) -> dict:
        d = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                if lower: d[k] = v
                else: d[str(k).lower()] = v

        return d

    def SetColors(self, text: str, background: str):
        if background: self.configure(background=background)
        if text: self.configure(foreground=text)
        return self
    def SetActiveColors(self, text: str, background: str):
        if background: self.configure(activebackground=background)
        if text: self.configure(activeforeground=text)
        return self
    def SetHighlightColors(self, text: str, background: str):
        if background:  self.configure(highlightcolor=text)
        if text: self.configure(highlightbackground=background)
        return self
    def SetDisabledColor(self, color: str):
        if color: self.configure(disabledforeground=color)
        return self

    def UnbindIDs(self, ids: Iterable[str] = None):
        for item in ids: self.unbind(item or self.__bindings__)

    def Bind(self, sequence: Bindings = None, func: callable = None, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        _id = self.bind(sequence, func, add)
        self.__bindings__[sequence].add(_id)
        return _id
    def BindAll(self, sequence: Bindings = None, func: callable = None, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        _id = self.bind_all(sequence, func, add)
        self.__bindings__[sequence].add(_id)
        return _id

    def ResetBindings(self):
        for seq, _set in self.__bindings__.items():
            for item in _set:
                self.unbind(seq, item)
    def ClearBindings(self, sequence: Bindings):
        for item in self.__bindings__[sequence]:
            self.unbind(sequence, item)
    def UnBind(self, sequence: Bindings, func_id: str):
        self.__bindings__[sequence].discard(func_id)
        self.unbind(sequence, func_id)
    def UnBindAll(self, sequence: Bindings = None):
        if isinstance(sequence, Enum): sequence = sequence.value
        self.__bindings__[sequence].clear()
        self.unbind_all(sequence)


    def BindClass(self, className, sequence: Bindings = None, func: callable = None, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        _id = self.bind_class(className, sequence, func, add)
        self.__bindings__[sequence].add(_id)
        return _id
    def UnBindClass(self, className, sequence: Bindings = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        self.__bindings__[sequence].clear()
        return self.unbind_class(className, sequence)



    def Pack(self, cnf: dict = { }, **kwargs):
        """Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to
                                  given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        self.pack(cnf, **kwargs)
        self._pi = self.pack_info()
        self._manager_ = Layout.pack
        return self
    def PackFull(self):
        """ Default placement in _root_frame occupying the full screen and/or space available in master. """
        return self.Pack(expand=True, fill=Fill.both, side=Side.top)
    def PackOptions(self, *, side: Union[str, Side], fill: Union[str, Fill], expand: bool, padx: int = 0, pady: int = 0):
        return self.Pack(side=side, expand=expand, fill=fill, padx=padx, pady=pady)
    def PackHorizontal(self, side: Union[str, Side] = Side.top): return self.PackOptions(expand=True, fill=Fill.x, side=side)
    def PackVertical(self, side: Union[str, Side] = Side.left): return self.PackOptions(expand=True, fill=Fill.y, side=side)


    def Place(self, cnf={ }, **kwargs):
        """Place a widget in the master widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        _x=amount - locate anchor of this widget at position _x of master
        _y=amount - locate anchor of this widget at position _y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        width=amount - width of this widget in pixel
        height=amount - height of this widget in pixel
        relwidth=amount - width of this widget between 0.0 and 1.0
                          relative to width of master (1.0 is the same width
                          as the master)
        relheight=amount - height of this widget between 0.0 and 1.0
                           relative to height of master (1.0 is the same
                           height as the master)
        bordermode="inside" or "outside" - whether to take border width of
                                           master widget into account
        """
        self.place(cnf, **kwargs)
        self._pi = self.place_info()
        self._manager_ = Layout.place
        return self
    def PlaceAbsolute(self, x: float, y: float, width: float, height: float):
        return self.Place(x=x, y=y, width=width, height=height)
    def PlaceRelative(self, relx: float, rely: float, relwidth: float, relheight: float):
        return self.Place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    def PlaceFull(self):
        """ Default placement in _root_frame occupying the full screen and/or space available in master. """
        return self.PlaceRelative(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)


    def Grid(self, row: int, column: int, sticky: str or AnchorAndSticky = tk.NSEW, rowspan: int = 1, columnspan: int = 1, padx: int = 0, pady: int = 0, **kwargs):
        """Position a widget in the master widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in _x direction
        ipady=amount - add internal padding in _y direction
        padx=amount - add padding in _x direction
        pady=amount - add padding in _y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                      widget stick to the cell boundary
        """
        self.grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, **kwargs)
        self._pi = self.grid_info()
        self._manager_ = Layout.grid
        return self
    # noinspection PyMethodOverriding
    def Grid_Anchor(self, anchor: str or AnchorAndSticky):
        """The anchor value controls how to place the grid within the
        master when no row/column has any weight.

        The default anchor is nw."""
        self.grid_anchor(anchor=anchor)
        return self
    def Grid_RowConfigure(self, index: int, weight: int, **kwargs):
        """Configure row INDEX of a grid.

        Valid resources are minsize (minimum size of the row),
        weight (how much does additional space propagate to this row)
        and pad (how much space to let additionally)."""
        self.grid_rowconfigure(index, weight=weight, **kwargs)
        return self
    def Grid_ColumnConfigure(self, index: int, weight: int, **kwargs):
        """Configure column INDEX of a grid.

        Valid resources are minsize (minimum size of the column),
        weight (how much does additional space propagate to this column)
        and pad (how much space to let additionally)."""
        self.grid_columnconfigure(index, weight=weight, **kwargs)
        return self


    def SetActive(self, takeFocus: bool = True):
        """ Set the widget to Active Status """
        if takeFocus: self.focus_set()
        return self._SetState(state=ViewState.Active)

    def Disable(self):
        """ Disable the widget """
        return self._SetState(state=ViewState.Disabled)
    def Enable(self, state: ViewState = ViewState.Normal):
        """ Enable the widget, and optinally change its state from normal. """
        return self._SetState(state=state)

    def _SetState(self, state: ViewState):
        assert (isinstance(state, ViewState))
        try: self.configure(state=state.value)
        except tk.TclError: pass

        self._state_ = state
        return self

    def Cancel_OnAppearing(self):
        if self._cb is None: return
        self.after_cancel(self._cb)
        self._cb = None
    def OnAppearing(self):
        """ this is called just after widget appears. override to implement desired effects """
        pass
    def OnDisappearing(self):
        """ this is called just before widget disappears. override to implement desired effects """
        pass

    @property
    def __class_name__(self) -> str: return nameof(self)

class BaseTextTkinterWidget(BaseTkinterWidget):
    _txt: tk.StringVar
    # noinspection PyMissingConstructor
    def __init__(self, text: str, Override_var: Optional[tk.StringVar], Color: Optional[Dict[str, str]], configure: bool = True, loop: Optional[asyncio.BaseEventLoop] = None):
        if Override_var is not None: self._txt = Override_var
        else: self._txt = tk.StringVar(master=self, value=text)

        if configure: self.configure(textvariable=self._txt)
        BaseTkinterWidget.__init__(self, Color, loop)
    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str): self._txt.set(value)

    @property
    def wrap(self) -> int: return self._wrap
    @wrap.setter
    def wrap(self, value: int):
        if not isinstance(value, int): value = int(value)
        self._wrap = value
        self.configure(wraplength=self._wrap)

    def Append(self, v: str):
        t = self.txt
        t += v
        self.txt = t

# ------------------------------------------------------------------------------------------

class CallWrapper(tk.CallWrapper):
    """ Internal class. Stores function to call when some user defined Tcl function is called e.g. after an event occurred. """

    _widget: Union[BaseTextTkinterWidget, BaseTkinterWidget] = None
    def __init__(self, func: Callable, widget: BaseTkinterWidget = None):
        """Store FUNC, SUBST and WIDGET as members."""
        self._func: Final[Callable] = func
        self._widget: Optional[BaseTkinterWidget] = widget

    def __call__(self, *args, **kwargs):
        """Apply first function SUBST to arguments, than FUNC."""
        try:
            return self._func(*args, **kwargs)
        except SystemExit: raise
        except Exception:
            if hasattr(self._widget, '_report_exception'):
                # noinspection PyProtectedMember
                return self._widget._report_exception()

            raise

    def __repr__(self) -> str: return f'{super().__repr__().replace(">", "")} [ {dict(func=self._func, widget=self._widget)} ]>'
    def __str__(self) -> str: return repr(self)

    def SetWidget(self, w: BaseTkinterWidget):
        """ Internal Method """
        assert (isinstance(w, BaseTkinterWidget))
        self._widget = w
        return self

    @classmethod
    def Create(cls, func: Callable, z: Union[int, float, str, Enum] = None, widget: BaseTkinterWidget = None, **kwargs):
        if z is not None and kwargs and func:
            return cls(lambda x=kwargs: func(z, **x), widget=widget)

        elif kwargs and func:
            return cls(lambda x=kwargs: func(**x), widget=widget)

        elif z is not None and func:
            return cls(lambda x=z: func(x), widget=widget)

        elif func:
            return cls(func, widget=widget)

        return None

class AsyncCallWrapper(tk.CallWrapper):
    """ Internal class. Stores function to call when some user defined Tcl function is called e.g. after an event occurred. """

    _widget: Union[BaseTextTkinterWidget, BaseTkinterWidget] = None
    # noinspection PyMissingConstructor
    def __init__(self, func: Coroutine, loop: BaseEventLoop, widget: Union[BaseTextTkinterWidget, BaseTkinterWidget]):
        """Store FUNC, SUBST and WIDGET as members."""
        # noinspection PyFinal
        self._func: Final[Coroutine] = func
        self._loop = loop
        self._widget = widget


    def __call__(self, *args, **kwargs): self._loop.create_task(self._func, name=self._func.__name__)

    def __repr__(self) -> str: return f'{super().__repr__().replace(">", "")} [ {dict(func=self._func, widget=self._widget)} ]>'
    def __str__(self) -> str: return repr(self)

    @classmethod
    def Create(cls, func: Union[Awaitable, Coroutine, Generator, Callable[[...], Coroutine]],
               loop: BaseEventLoop,
               widget: Union['CommandMixin', BaseTkinterWidget],
               z: Union[int, float, str, Enum] = None,
               **kwargs):
        if not func: return None

        async def wrapper() -> Any:
            try:
                if iscoroutine(func):
                    return await func

                if callable(func):
                    if z is not None and kwargs:
                        return func(z, **kwargs)

                    elif kwargs:
                        return func(**kwargs)

                    elif z is not None:
                        return func(z)

                    return await func(z, **kwargs)

                return await func

            except SystemExit: raise
            except Exception:
                if hasattr(widget, '_report_exception'):
                    # noinspection PyProtectedMember
                    return widget._report_exception()

                raise


        return cls(wrapper(), loop, widget)

class CurrentValue(CallWrapper):
    """
        Stores function to call when some user defined Tcl function is called e.g. after an event occurred.
        Passes the current value of the widget to the funciton.

        example:
            widget.SetCommand(CurrentValue(passed_function))
    """
    def __init__(self, func: callable, *args, widget: BaseTkinterWidget = None, **kwargs):
        """ Store FUNC, SUBST and WIDGET as members. """
        self._args = args
        self._kwargs = kwargs
        super(CurrentValue, self).__init__(func, widget)

    def __call__(self, *args, **kwargs): return self._func(self._widget.txt, *(self._args or args), **(self._kwargs or kwargs))
    def SetWidget(self, w):
        """
            Internal Method

        :param w: widget being assigned to this wrapper
        :type w: BaseTextTkinterWidget, CommandMixin
        :return: CurrentValue
        :rtype: CurrentValue
        """
        assert (isinstance(w, BaseTextTkinterWidget) and isinstance(w, CommandMixin))
        self._widget = w
        return self


# ------------------------------------------------------------------------------------------


class CommandMixin:
    _cmd: Optional[Union[CurrentValue, AsyncCallWrapper, CallWrapper]]
    configure: callable
    command_cb: str
    _loop: Optional[BaseEventLoop]
    def __call__(self, *args, **kwargs):
        """ Execute the Command """
        if callable(self._cmd): self._cmd(*args, **kwargs)

    def SetCommand(self, func: Union[Callable, FunctionType, MethodType, CurrentValue], z: Union[int, float, str, Enum] = None, add: bool = False, **kwargs):
        """
        :param func: function or method being called.
        :type func: Union[callable, FunctionType, MethodType, CurrentValue]
        :param z: arg passed to the fucntion.
        :type z: Union[int, float, str, Enum]
        :param add: if True, replaces the current function.
        :type add: bool
        :param kwargs: keyword args passed to the function.
        :type kwargs: Any
        :return: returns self to enable chaining.
        """
        if not callable(func): raise ValueError(f'func is not callable. got {type(func)}')

        if isinstance(func, CurrentValue): self._cmd = func.SetWidget(self)
        else: self._cmd = CallWrapper.Create(func, z, **kwargs)

        return self._setCommand(add)

    def SetCommandAsync(self, func: Union[Awaitable, Callable[[...], Coroutine], Coroutine],
                        z: Union[int, float, str, Enum] = None,
                        add: bool = False,
                        **kwargs):
        """
        :param func: function or method being called.
        :type func: Union[callable, FunctionType, MethodType, CurrentValue]
        :param z: arg passed to the function.
        :type z: Union[int, float, str, Enum]
        :param add: if True, replaces the current function.
        :type add: bool
        :param kwargs: keyword args passed to the function.
        :type kwargs: Any
        :return: returns self to enable chaining.
        """

        if isinstance(func, CurrentValue): raise ArgumentError(f'func cannot be a CurrentValue instance. Use "SetCommand" instead.')

        self._cmd = AsyncCallWrapper.Create(func, self._loop, self, z, **kwargs)

        return self._setCommand(add)

    def _setCommand(self, add: bool):
        self.configure(command=self._cmd)
        return self



class tkPhotoImage(PhotoImage):
    @property
    def width(self) -> int:
        """
        Get the width of the img.

        :return: The width, in pixels.
        """
        return super().width()

    @property
    def height(self) -> int:
        """
        Get the height of the img.

        :return: The height, in pixels.
        """
        return super().height()



def img_open(fp: BinaryIO, *formats: str, mode="r") -> Image:
    """
    Opens and identifies the given image file.

    This is a lazy operation; this function identifies the file, but
    the file remains open and the actual image data is not read from
    the file until you try to process the data (or call the
    :py:meth:`~PIL.Image.Image.load` method).  See
    :py:func:`~PIL.Image.new`. See :ref:`file-handling`.

    :param fp: A filename (string), pathlib.Path object or a file object.
       The file object must implement ``file.read``,
       ``file.seek``, and ``file.tell`` methods,
       and be opened in binary mode.
    :param mode: The mode.  If given, this argument must be "r".
    :param formats: A list or tuple of formats to attempt to load the file in.
       This can be used to restrict the set of formats checked.
       Pass ``None`` to try all supported formats. You can print the set of
       available formats by running ``python3 -m PIL`` or using
       the :py:func:`PIL.features.pilinfo` function.
    :returns: An :py:class:`~PIL.Image.Image` object.
    :exception FileNotFoundError: If the file cannot be found.
    :exception PIL.UnidentifiedImageError: If the image cannot be opened and
       identified.
    :exception ValueError: If the ``mode`` is not "r", or if a ``StringIO``
       instance is used for ``fp``.
    :exception TypeError: If ``formats`` is not ``None``, a list or a tuple.
    """
    return _img_open(fp, mode, formats or None)



class ImageMixin:
    width: int
    height: int
    configure: callable
    update_idletasks: callable
    update: callable
    _IMG: tkPhotoImage = None

    @overload
    def SetImage(self, img: tkPhotoImage): ...

    @overload
    def SetImage(self, url: URL, *formats: str, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs): ...
    @overload
    def SetImage(self, url: URL, *formats: str, widthMax: int, heightMax: int, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs): ...

    @overload
    def SetImage(self, path: Union[str, bytes, FilePath, Enum], *formats: str): ...
    @overload
    def SetImage(self, path: Union[str, bytes, FilePath, Enum], *formats: str, widthMax: int, heightMax: int): ...

    @overload
    def SetImage(self, base64data: Union[str, bytes, Enum], *formats: str): ...
    @overload
    def SetImage(self, base64data: Union[str, bytes, Enum], *formats: str, widthMax: int, heightMax: int): ...


    def SetImage(self, data: Union[str, bytes, Enum, FilePath, URL, tkPhotoImage],
                 *formats: str,
                 widthMax: int = None,
                 heightMax: int = None, **kwargs):
        if data is None: return self._setImage(None)

        if isinstance(data, Enum): data = data.value

        if isinstance(data, tkPhotoImage):
            return self._setImage(data)

        if isinstance(data, URL) or isinstance(data, str) and data.lower().strip().startswith('http'):
            reply = get(data, **kwargs)
            with BytesIO(reply.content) as buf:
                return self._setImage(ImageMixin.open(self, buf, widthMax, heightMax, *formats))

        if isfile(data):
            with open(data, 'rb') as f:
                return self._setImage(ImageMixin.open(self, f, widthMax, heightMax, *formats))

        return self.SetImageFromBytes(base64.b64decode(data), *formats, width=widthMax, height=heightMax)






    @overload
    async def SetImageAsync(self, img: tkPhotoImage): ...

    @overload
    async def SetImageAsync(self, url: URL, *formats: str, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs): ...
    @overload
    async def SetImageAsync(self, url: URL, *formats: str, widthMax: int, heightMax: int, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs): ...

    @overload
    async def SetImageAsync(self, path: Union[str, bytes, FilePath, Enum], *formats: str): ...
    @overload
    async def SetImageAsync(self, path: Union[str, bytes, FilePath, Enum], *formats: str, widthMax: int, heightMax: int): ...

    @overload
    async def SetImageAsync(self, base64data: Union[str, bytes, Enum], *formats: str): ...
    @overload
    async def SetImageAsync(self, base64data: Union[str, bytes, Enum], *formats: str, widthMax: int, heightMax: int): ...


    async def SetImageAsync(self, data: Union[str, bytes, Enum, FilePath, URL, tkPhotoImage],
                            *formats: str,
                            widthMax: int = None,
                            heightMax: int = None,
                            **kwargs) -> 'ImageMixin':
        if data is None: return self._setImage(None)

        if isinstance(data, Enum): data = data.value

        if isinstance(data, tkPhotoImage):
            return self._setImage(data)

        if isinstance(data, URL) or isinstance(data, str) and data.lower().strip().startswith('http'):
            async with ClientSession() as session:
                content: ClientResponse = await session.get(data, **kwargs)
                with BytesIO(await content.read()) as buf:
                    return self._setImage(ImageMixin.open(self, buf, widthMax, heightMax, *formats))

        if isfile(data):
            async with async_file_open(data, 'rb') as f:
                return self._setImage(ImageMixin.open(self, f, widthMax, heightMax, *formats))

        return self.SetImageFromBytes(base64.b64decode(data), *formats, width=widthMax, height=heightMax)

    def SetImageFromBytes(self, data: bytes, *formats: str, width: int = None, height: int = None) -> 'ImageMixin':
        assert (isinstance(data, bytes))

        with BytesIO(data) as buf:
            return self._setImage(ImageMixin.open(self, buf, width, height, *formats))


    @staticmethod
    def open(self: Union[BaseTkinterWidget, 'ImageMixin'], f: Union[BinaryIO, AsyncBufferedReader],
             widthMax: Optional[int], heightMax: Optional[int], *formats: str) -> tkPhotoImage:
        if widthMax is None: widthMax = self.width
        if heightMax is None: heightMax = self.height

        if widthMax <= 0: raise ValueError(f'widthMax must be positive. Value: {widthMax}')
        if heightMax <= 0: raise ValueError(f'heightMax must be positive. Value: {heightMax}')

        with img_open(f, *formats) as img:
            img = img.resize(ImageMixin.CalculateNewSize(img, widthMax, heightMax))
            return tkPhotoImage(img, master=self)

    def _setImage(self, img: Optional[tkPhotoImage]) -> 'ImageMixin':
        self.update_idletasks()
        self._IMG = img
        self.configure(img=self._IMG)
        return self


    @staticmethod
    def Maximum_ScalingFactor(*options: float) -> float: return max(options)
    @staticmethod
    def Minimum_ScalingFactor(*options: float) -> float: return min(options)

    @staticmethod
    def Factors(img: Image, widthMax: int, heightMax: int) -> Tuple[float, float]: return widthMax / img.width, heightMax / img.height
    @staticmethod
    def CalculateNewSize(img: Image, widthMax: int, heightMax: int) -> Tuple[int, int]:
        options = ImageMixin.Factors(img, widthMax, heightMax)
        scalingFactor = ImageMixin.Minimum_ScalingFactor(*options)
        return ImageMixin.Scale(img, scalingFactor)
    @staticmethod
    def Scale(img: Image, factor: float) -> Tuple[int, int]: return int(img.width * (factor or 1)), int(img.height * (factor or 1))
