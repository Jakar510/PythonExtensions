# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
import base64
import tkinter as tk
from _tkinter import DONT_WAIT
from abc import ABC
from asyncio import AbstractEventLoop, get_event_loop, iscoroutine, iscoroutinefunction, run_coroutine_threadsafe
from enum import Enum
from io import BytesIO
from logging import Logger
from multiprocessing import Queue
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

from .Enumerations import *
from .Enumerations import Orientation
from .Events import Bindings, TkinterEvent, tkEvent
from .Style import *
from ..Core import *
from ..Debug import pp




__all__ = [
    'BaseTkinterWidget',
    'BaseTextTkinterWidget',
    'CommandMixin',
    'ImageMixin',
    'CurrentValue',
    'CallWrapper',
    'tk',
    'ttk',
    'tkEvent',
    'URL',
    'img_open',
    'async_file_open',
    'tkPhotoImage',
    'BaseApp',
    'BaseAsyncApp',
    'BaseSyncApp',
    'BaseWindow',
    'BaseLabelWindow',
    'Updater',
    'AsyncUpdater',
    'Frame',
    'LabelFrame',
    'FrameThemed',
    'LabelFrameThemed',
    'convert_kwargs',
    'tkRoot',
    'tkTopLevel',
    ]


class _rootMixin:
    style: Style
    Screen_Width: int = None
    Screen_Height: int = None

    winfo_screenwidth: callable
    winfo_screenheight: callable
    geometry: callable
    config: callable
    bind: callable
    unbind_all: callable
    bind_all: callable
    title: callable

    winfo_x: callable
    winfo_y: callable
    winfo_height: callable
    winfo_width: callable

    update: callable
    update_idletasks: callable
    tk_focusNext: callable
    tk_focusPrev: callable
    attributes: callable
    resizable: callable
    def SetDimensions(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0):
        self.Screen_Width = Screen_Width or int(self.winfo_screenwidth())
        self.Screen_Height = Screen_Height or int(self.winfo_screenheight())
        return self.geometry(self.Dimensions(x, y))
    def Dimensions(self, x: int = 0, y: int = 0) -> str:
        return f"{self.Screen_Width}x{self.Screen_Height}+{x}+{y}"

    def HideCursor(self):
        self.config(cursor="none")
        return self

    def SetFullScreen(self, fullscreen: bool = False):
        self.attributes('-fullscreen', fullscreen)
        return self
    def SetTitle(self, title: str):
        self.title(title)
        return self
    def SetResizable(self, resizable: bool):
        self.resizable(width=resizable, height=resizable)
        return self

    def Update(self):
        self.update()
        self.update_idletasks()

    def Bind(self, sequence: Union[str, Enum] = None, func: callable = None, add: bool = None):
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind(sequence, func, add)

    def MultiUnbindAll(self, *args: Union[str, Enum]):
        for arg in args: self.UnbindAll(arg)
    def UnbindAll(self, sequence: Union[str, Enum] = None):
        """Unbind for all widgets for event SEQUENCE all functions."""
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.unbind_all(sequence)

    def BindAll(self, sequence: Union[str, Enum] = None, func: callable = None, add: bool = None):
        """Bind to all widgets at an event SEQUENCE a call to function FUNC.
        An additional boolean parameter ADD specifies whether FUNC will
        be called additionally to the other bound function or whether
        it will replace the previous function. See bind for the return value."""
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind_all(sequence, func, add)

    @property
    def width(self) -> int:
        return self.winfo_width()
    @property
    def height(self) -> int:
        return self.winfo_height()

    @property
    def x(self) -> int:
        return self.winfo_x()
    @property
    def y(self) -> int:
        return self.winfo_y()


    @property
    def Orientation(self) -> Orientation:
        return Orientation.Landscape if self.Screen_Width > self.Screen_Height else Orientation.Portrait

    def SetTransparency(self, v: float):
        assert (0.0 <= v <= 1.0)
        return self.attributes('-alpha', v)

    def FocusNext(self):
        self.tk_focusNext().focus_set()
    def FocusPrevious(self):
        self.tk_focusPrev().focus_set()


class tkRoot(tk.Tk, _rootMixin):
    __slots__ = ['style']
    def __init__(self, width: Optional[int] = None, height: Optional[int] = None, fullscreen: Optional[bool] = None, x: int = 0, y: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.SetDimensions(width, height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)
        self.style = Style(master=self)

    def _options(self, cnf, kwargs=None) -> Dict:
        # noinspection PyUnresolvedReferences,PyProtectedMember
        return super()._options(cnf, convert_kwargs(kwargs))


    def Create_Event(self, tag: Union[str, Bindings], *, num: int = '??', height: int = '??', width: int = '??', key_code: int = '??', state: int = '??',
                     x: int = '??', y: int = '??', char: str = '??', keysym: Union[str, Bindings] = '??', keysym_num: int = '??', delta: int = '??',
                     event_type: tk.EventType, widget: tk.Widget, current_time=time()):
        """
            example:
                <TkinterEvent Object. Configuration:
                {   'char': 'a',
                    'delta': 0,
                    'Height': '??',
                    'keycode': 65,
                    'keysym': 'a',
                    'keysym_num': 97,
                    'num': '??',
                    'state': 8,
                    'time': 329453312,
                    'type': <EventType.KeyPress: '2'>,
                    'widget': <spf.Workers.Views.Carousel.CarouselView object .!carouselview>,
                    'Width': '??',
                    'x': 936,
                    'x_root': 1045,
                    'y': 670,
                    'y_root': 808} >

            class Event:
                '''Container for the properties of an event.

                Instances of this type are generated if one of the following events occurs:

                KeyPress, KeyRelease - for keyboard events
                ButtonPress, ButtonRelease, Motion, Enter, Leave, MouseWheel - for mouse events
                Visibility, Unmap, Map, Expose, FocusIn, FocusOut, Circulate,
                Colormap, Gravity, Reparent, Property, Destroy, Activate,
                Deactivate - for window events.

                If a callback function for one of these events is registered
                using bind, bind_all, bind_class, or tag_bind, the callback is
                called with an Event as first argument. It will have the
                following attributes (in braces are the event types for which
                the attribute is valid):

                    serial - serial number of event
                num - mouse button pressed (ButtonPress, ButtonRelease)
                focus - whether the window has the focus (Enter, Leave)
                Height - Height of the exposed window (Configure, Expose)
                Width - Width of the exposed window (Configure, Expose)
                keycode - keycode of the pressed key (KeyPress, KeyRelease)
                state - state of the event as a number (ButtonPress, ButtonRelease,
                                        Enter, KeyPress, KeyRelease,
                                        Leave, Motion)
                state - state as a string (Visibility)
                time - when the event occurred
                x - x-position of the mouse
                y - y-position of the mouse
                x_root - x-position of the mouse on the screen
                         (ButtonPress, ButtonRelease, KeyPress, KeyRelease, Motion)
                y_root - y-position of the mouse on the screen
                         (ButtonPress, ButtonRelease, KeyPress, KeyRelease, Motion)
                char - pressed character (KeyPress, KeyRelease)
                send_event - see X/Windows documentation
                keysym - keysym of the event as a string (KeyPress, KeyRelease)
                keysym_num - keysym of the event as a number (KeyPress, KeyRelease)
                type - type of the event as a number
                widget - widget in which the event occurred
                delta - delta of wheel movement (MouseWheel)
                '''

        :param tag:
        :param num: mouse button pressed (ButtonPress, ButtonRelease)
        :param key_code: keycode of the pressed key (KeyPress, KeyRelease)
        :param state: state of the event as a number (ButtonPress, ButtonRelease,
                                        Enter, KeyPress, KeyRelease,
                                        Leave, Motion)
        :param current_time:
        :param height: Height of the exposed window (Configure, Expose)
        :param width: Width of the exposed window (Configure, Expose)
        :param x: x-position of the mouse
        :param y: y-position of the mouse
        :param char: pressed character (KeyPress, KeyRelease)
        :param keysym: keysym of the event as a string (KeyPress, KeyRelease)
        :param keysym_num: keysym of the event as a number (KeyPress, KeyRelease)
        :param event_type: type of the event as a number
        :param widget: widget in which the event occurred
        :param delta: delta of wheel movement (MouseWheel)
        :return:
        """
        if isinstance(tag, Bindings): tag = tag.value
        if isinstance(keysym, Bindings): keysym = keysym.value

        # noinspection PyArgumentList
        self.event_generate(sequence=tag, num=num, width=width, height=height, keycode=key_code, state=state, time=current_time, x=x, y=y, char=char, keysym=keysym,
                            keysym_num=keysym_num, type=event_type, widget=widget, x_root=self.winfo_rootx(), y_root=self.winfo_rooty(), delta=delta)

    def do_one_event(self):
        return self.tk.dooneevent(DONT_WAIT)


class tkTopLevel(tk.Toplevel, _rootMixin):
    __slots__ = ['style']
    def __init__(self, master: tkRoot, *, width: int = None, height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(master, **kwargs)
        self.SetDimensions(width, height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.style = master.style

    def _options(self, cnf, kwargs=None) -> Dict:
        # noinspection PyUnresolvedReferences,PyProtectedMember
        return super()._options(cnf, convert_kwargs(kwargs))


# ------------------------------------------------------------------------------------------


def convert_kwargs(kwargs: Dict[str, Any], lower: bool = True) -> Optional[Dict[str, Any]]:
    if kwargs is None: return None

    Assert(kwargs, dict)

    d = { }
    for k, v in kwargs.items():
        if isinstance(v, Enum): v = v.value
        if lower:
            d[str(k).lower()] = v
        else:
            d[k] = v

    return d


# ------------------------------------------------------------------------------------------


class tkPhotoImage(PhotoImage):
    __slots__ = []
    @property
    def width(self) -> int:
        """
        Get the Width of the img.

        :return: The Width, in pixels.
        """
        return super().width()

    @property
    def height(self) -> int:
        """
        Get the Height of the img.

        :return: The Height, in pixels.
        """
        return super().height()

    @property
    def size(self) -> Tuple[int, int]: return self.width, self.height


# ------------------------------------------------------------------------------------------


class BindingCollection(dict, Dict[Bindings, Set[str]]):
    __slots__ = []
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
    __bindings__: BindingCollection
    _state_: ViewState
    _pi: Optional[Dict]
    _manager_: Optional[Layout]
    _wrap: Optional[int]
    _cb: Union[str, None]
    _loop: Optional[AbstractEventLoop]

    # noinspection PyMissingConstructor
    def __init__(self, Color: Optional[Dict[str, str]], loop: Optional[AbstractEventLoop]):
        if Color: self.configure(**Color)
        self._loop = loop
        self._state_ = ViewState.Hidden
        self.__bindings__ = BindingCollection()
        self._pi = None
        self._manager_ = None
        self._wrap = None
        self._cb = None



    @property
    def pi(self) -> Dict:
        return self._pi.copy()

    @property
    def IsVisible(self) -> bool:
        return self._state_ != ViewState.Hidden

    @property
    def CurrentViewState(self) -> ViewState:
        return self._state_

    def ToString(self, IncludeState: bool = None) -> str:

        start = repr(self).replace('>', '').replace('<', '').replace('object', 'Tkinter Widget')
        if IncludeState is None:
            return f'<{start}. State: {pp.getPPrintStr(self.Details)}>'

        if IncludeState:
            return f'<{start}. State: {pp.getPPrintStr(self.FullDetails)}>'

        return f'<{start}>'
    @property
    def Details(self) -> Dict[str, Any]:
        return dict(IsVisible=self.IsVisible)
    @property
    def FullDetails(self) -> Dict[str, Any]:
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


    def Dimensions(self) -> Tuple[int, int, int, int]:
        """
        :return: x, y, width, height
        """
        s = self.winfo_geometry()
        wh, x, y = s.split('+')
        w, h = wh.split('x')
        return int(x), int(y), int(w), int(h)


    def Left(self) -> int:
        d = self.Dimensions()
        return d[0]
    def Right(self) -> int:
        d = self.Dimensions()
        return d[0] + d[2]
    def Top(self) -> int:
        d = self.Dimensions()
        return d[1]
    def Bottom(self) -> int:
        d = self.Dimensions()
        return d[1] + d[3]



    @property
    def size(self) -> Tuple[int, int]:
        return self.Width, self.Height
    @property
    def Width(self) -> int:
        return self.winfo_width()
    @property
    def Height(self) -> int:
        return self.winfo_height()

    @property
    def x(self) -> int:
        return self.winfo_rootx()
    @property
    def y(self) -> int:
        return self.winfo_rooty()


    @overload
    def show(self, _event: Optional[tkEvent] = None) -> bool:
        ...
    @overload
    def show(self, _event: Optional[tkEvent] = None, *, TakeFocus: bool) -> bool:
        ...
    @overload
    def show(self, _event: Optional[tkEvent] = None, *, TakeFocus: bool, State: ViewState) -> bool:
        ...

    def show(self, _event: Optional[tkEvent] = None, **kwargs) -> bool:
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
    def hide(self, _event: Optional[tkEvent] = None) -> bool:
        ...
    @overload
    def hide(self, _event: Optional[tkEvent] = None, *, new_focus: tk.Widget) -> bool:
        ...

    def hide(self, _event: Optional[tkEvent] = None, *, new_focus: tk.Widget = None) -> bool:
        """
        Hides the current widget or _root_frame, based on the current geometry manager.
        Can be overridden to add additional functionality if needed.
        """
        if self._manager_ is None: return False

        if new_focus: new_focus.focus_set()

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


    # noinspection PyArgumentList
    def SetColors(self, text: str, background: str):
        if background: self.configure(background=background)
        if text: self.configure(foreground=text)
        return self
    # noinspection PyArgumentList
    def SetActiveColors(self, text: str, background: str):
        if background: self.configure(activebackground=background)
        if text: self.configure(activeforeground=text)
        return self
    # noinspection PyArgumentList
    def SetHighlightColors(self, text: str, background: str):
        if background:  self.configure(highlightcolor=text)
        if text: self.configure(highlightbackground=background)
        return self
    # noinspection PyArgumentList
    def SetDisabledColor(self, color: str):
        if color: self.configure(disabledforeground=color)
        return self

    def UnbindIDs(self, ids: Iterable[str] = None):
        for item in ids: self.unbind(item)

    def Bind(self, sequence: Bindings, func: callable, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        _id = self.bind(sequence, func, add)
        self.__bindings__[sequence].add(_id)
        return _id
    def BindAll(self, sequence: Bindings, func: callable, add: bool = None) -> str:
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

    def unbind(self, sequence: Union[Bindings, str], funcid: str = None) -> None:
        _seq = sequence.value if isinstance(sequence, Bindings) else sequence
        return super(BaseTkinterWidget, self).unbind(_seq)


    def BindClass(self, className, sequence: Bindings, func: callable, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        _id = self.bind_class(className, sequence, func, add)
        self.__bindings__[sequence].add(_id)
        return _id
    def UnBindClass(self, className, sequence: Bindings) -> None:
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
    def PackHorizontal(self, side: Union[str, Side] = Side.top):
        return self.PackOptions(expand=True, fill=Fill.x, side=side)
    def PackVertical(self, side: Union[str, Side] = Side.left):
        return self.PackOptions(expand=True, fill=Fill.y, side=side)


    def Place(self, cnf={ }, **kwargs):
        """Place a widget in the master widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        _x=amount - locate anchor of this widget at position _x of master
        _y=amount - locate anchor of this widget at position _y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to Width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to Height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        Width=amount - Width of this widget in pixel
        Height=amount - Height of this widget in pixel
        relwidth=amount - Width of this widget between 0.0 and 1.0
                          relative to Width of master (1.0 is the same Width
                          as the master)
        relheight=amount - Height of this widget between 0.0 and 1.0
                           relative to Height of master (1.0 is the same
                           Height as the master)
        bordermode="inside" or "outside" - whether to take border Width of
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

    # noinspection PyArgumentList
    def _SetState(self, state: ViewState):
        assert (isinstance(state, ViewState))
        try:
            self.configure(state=state.value)
        except tk.TclError:
            pass

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
    def __class_name__(self) -> str:
        return nameof(self)

    def __updateSize__(self):
        self.update()
        size = self.size
        while any(i <= 1 for i in size):
            self.update_idletasks()
            size = self.size


class BaseTextTkinterWidget(BaseTkinterWidget):
    _txt: tk.StringVar
    def __init__(self, text: str, Override_var: Optional[tk.StringVar], Color: Optional[Dict[str, str]], loop: Optional[AbstractEventLoop], configure: bool = True):
        if Override_var is not None:
            self._txt = Override_var
        else:
            self._txt = tk.StringVar(master=self, value=text)

        if configure:
            # noinspection PyArgumentList
            self.configure(textvariable=self._txt)
        BaseTkinterWidget.__init__(self, Color, loop)


    @property
    def txt(self) -> str:
        return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)

    @property
    def wrap(self) -> int:
        return self._wrap
    @wrap.setter
    def wrap(self, value: int):
        if not isinstance(value, int): value = int(value)
        self._wrap = value
        # noinspection PyArgumentList
        self.configure(wraplength=self._wrap)

    def Append(self, v: str):
        t = self.txt
        t += v
        self.txt = t


# ------------------------------------------------------------------------------------------


SyncCallable = Callable[[Optional[tkEvent], Tuple, Dict[str, Any]], Any]
SimpleSyncCallable = Callable[[Optional[tkEvent]], Any]
# class CallWrapper(object):
#     """ Internal class. Stores function to call when some user defined Tcl function is called e.g. after an event occurred. """
#     __slots__ = ['_func',
#                  '_widget',
#                  '_args',
#                  '_kwargs',
#                  ]
#     _widget: Union[BaseTextTkinterWidget, BaseTkinterWidget, 'CommandMixin']
#     _func: Final[SyncCallable]
#     def __init__(self, func: SyncCallable, widget: Union[BaseTextTkinterWidget, BaseTkinterWidget, 'CommandMixin'], *args, **kwargs):
#         assert (isinstance(widget, BaseTkinterWidget) and isinstance(widget, CommandMixin))
#         self._func = func
#         self._widget = widget
#         self._args = args
#         self._kwargs = kwargs
#
#     def __call__(self, event: Optional[tkEvent] = None):
#         try:
#             return self._func(event, *self._args, **self._kwargs)
#         except KeyboardInterrupt:
#             return
#
#         except SystemExit:
#             raise
#
#         except Exception as e:
#             # noinspection PyProtectedMember
#             root = self._widget._root()
#             root.report_callback_exception(typeof(e), e, e.__traceback__)
#
#
#     def __repr__(self) -> str:
#         return f'{super().__repr__().replace(">", "")} [ {dict(func=self._func, widget=self._widget)} ]>'
#     def __str__(self) -> str:
#         return repr(self)
#
#     def SetWidget(self, w: BaseTkinterWidget):
#         """ Internal Method """
#         assert (isinstance(w, BaseTkinterWidget))
#         self._widget = w
#         return self


AsyncCallable = Callable[[Optional[tkEvent], Tuple, Dict[str, Any]], Coroutine]
SimpleAsyncCallable = Callable[[Optional[tkEvent]], Coroutine]
class CallWrapper(object):
    """ Internal class. Stores function to call when some user defined Tcl function is called e.g. after an event occurred. """
    __slots__ = ['_func',
                 '_widget',
                 '_loop',
                 '_args',
                 '_kwargs',
                 ]

    _widget: Union[BaseTextTkinterWidget, BaseTkinterWidget, None]
    _func: Final[Union[SimpleSyncCallable, SyncCallable, AsyncCallable, SimpleAsyncCallable]]
    _loop: Final[Optional[AbstractEventLoop]]
    _args: Final[Tuple]
    _kwargs: Final[Dict[str, Any]]
    def __init__(self, func: Union[SimpleSyncCallable, SyncCallable, AsyncCallable, SimpleAsyncCallable],
                 loop: Optional[AbstractEventLoop],
                 widget: Union[BaseTextTkinterWidget, BaseTkinterWidget, 'CommandMixin'],
                 args,
                 kwargs):
        assert (isinstance(widget, BaseTkinterWidget) and isinstance(widget, CommandMixin))
        self._func = func
        self._loop = loop
        self._widget = widget
        self._args = args
        self._kwargs = kwargs


    def __call__(self, _event: Optional[tkEvent] = None):
        try:
            try:
                result = self._func(_event, self._args, self._kwargs)
            except TypeError:
                result = self._func(_event)

            if iscoroutine(result) or iscoroutinefunction(result):
                if self._loop is None: raise ValueError('_loop is None')
                return run_coroutine_threadsafe(result, self._loop)

            return result

        except KeyboardInterrupt:
            return

        except SystemExit:
            raise

        except Exception as e:
            if hasattr(self._widget, '_root'):
                # noinspection PyProtectedMember
                root = self._widget._root()
                root.report_callback_exception(typeof(e), e, e.__traceback__)
                return

            raise AttributeError('_root')

    def __repr__(self) -> str:
        return f'{super().__repr__().replace(">", "")} [ {dict(func=self._func, widget=self._widget)} ]>'
    def __str__(self) -> str:
        return repr(self)


CurrentValueCallable = Callable[[Optional[tkEvent], str, Tuple, Dict[str, Any]], Any]
CurrentValueAsyncCallable = Callable[[Optional[tkEvent], str, Tuple, Dict[str, Any]], Coroutine]
class CurrentValue(object):
    __doc__ = """
        Stores function to call when some user defined Tcl function is called e.g. after an event occurred.
        Passes the current value of the widget to the function.

        example:
            widget.SetCommand(CurrentValue(passed_function))
    """
    __slots__ = ['_func', '_widget', '_args', '_kwargs', '_loop']
    _widget: Union[BaseTextTkinterWidget, BaseTkinterWidget, None]
    _args: Final[Union[List[Any], Tuple[Any]]]
    _kwargs: Final[Dict[str, Any]]
    _loop: Optional[AbstractEventLoop]
    _func: Final[Union[CurrentValueCallable, CurrentValueAsyncCallable]]
    def __init__(self, func: Union[CurrentValueCallable, CurrentValueAsyncCallable], *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._widget = None
        self._func = func
        self._loop = None
    def _SetWidget(self, w: 'CommandMixin'):
        """
            Internal Method

        :param w: widget being assigned to this wrapper
        :return: CurrentValue
        :rtype: CurrentValue
        """
        assert (isinstance(w, BaseTextTkinterWidget) and isinstance(w, CommandMixin))
        self._widget = w
        # noinspection PyProtectedMember
        self._loop = w._current_loop()
        return self

    def __call__(self, event: Optional[tkEvent] = None):
        try:
            result = self._func(event, self._widget.txt, *self._args, **self._kwargs)
            if iscoroutine(result) or iscoroutinefunction(result):
                return run_coroutine_threadsafe(result, self._loop)

            return result
        except SystemExit:
            raise
        except Exception as e:
            if hasattr(self._widget, '_root'):
                # noinspection PyProtectedMember
                root = self._widget._root()
                root.report_callback_exception(typeof(e), e, e.__traceback__)
                return

            raise AttributeError('_root')


class CommandMixin:
    _cmd: Optional[Union[CurrentValue, CallWrapper]]
    configure: callable
    command_cb: str

    def __call__(self, *args, **kwargs):
        """ Execute the Command """
        if callable(self._cmd): self._cmd(*args, **kwargs)

    def SetCommand(self,
                   func: Union[SimpleSyncCallable, SyncCallable, AsyncCallable, SimpleAsyncCallable, CurrentValue],
                   # func: Union[Callable, FunctionType, MethodType, CurrentValue, Awaitable, Coroutine, Generator],
                   *args,
                   add: bool = False,
                   **kwargs):
        """
        :param func: function or method being called.
        :type func: Union[callable, FunctionType, MethodType, CurrentValue, Awaitable, Coroutine, Generator]
        :param args: args passed to the fucntion.
        :param add: if True, replaces the current function.
        :type add: bool
        :param kwargs: keyword args passed to the function.
        :type kwargs: Any
        :return: returns self to enable chaining.
        """
        assert (isinstance(self, BaseTkinterWidget) and isinstance(self, CommandMixin))

        if not callable(func):
            raise ValueError(f'func is not callable. got {typeof(func)}')

        if isinstance(func, CurrentValue):
            # noinspection PyProtectedMember
            self._cmd = func._SetWidget(self)
        else:
            self._cmd = CallWrapper(func, self._current_loop(), self, args, kwargs)

        return self._setCommand(add)


    def _setCommand(self, add: bool):
        self.configure(command=self._cmd)
        return self


    def _current_loop(self) -> Optional[AbstractEventLoop]:
        assert (isinstance(self, BaseTkinterWidget) and isinstance(self, CommandMixin))

        if self._loop is not None:
            return self._loop

        master = self.master
        while master is not None:
            if isinstance(master, BaseAsyncApp):
                self._loop = master.loop
                return self._loop

            elif isinstance(master, (BaseApp, BaseSyncApp)):
                return None

            elif isinstance(master, tk.Widget):
                master = master.master

            elif isinstance(master, tkTopLevel):
                master = master.master

            else:
                break

        raise TypeError(typeof(master), (BaseAsyncApp, BaseSyncApp, BaseApp))


# ------------------------------------------------------------------------------------------


def img_open(fp: BinaryIO, *formats: str, mode: Literal['r'] = 'r') -> Image:
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


# async def img_open_async(fp: AsyncBufferedReader, *formats: str, mode="r") -> Image:
#     if mode != "r":
#         raise ValueError(f"bad mode {repr(mode)}")
#
#     if formats is None:
#         formats = ID
#     elif not isinstance(formats, (list, tuple)):
#         raise TypeError("formats must be a list or tuple")
#
#     exclusive_fp = False
#     try:
#         await fp.seek(0)
#     except (AttributeError, UnsupportedOperation):
#         fp = BytesIO(await fp.read())
#         exclusive_fp = True
#
#     prefix = await fp.read(16)
#
#     preinit()
#
#     accept_warnings: List[Union[str, bytes]] = []
#
#     async def _open_core(_fp: AsyncBufferedReader, _prefix: bytes, _formats: Iterable[str]) -> Optional[Image]:
#         for fmt in _formats:
#             fmt = fmt.upper()
#             if fmt not in OPEN:
#                 init()
#
#             try:
#                 factory: Callable[[AsyncBufferedReader, Optional[str]], Image]
#                 accept: Callable[[bytes], Union[str, bytes, None]]
#
#                 factory, accept = OPEN[fmt]
#
#                 result = not accept or accept(_prefix)
#                 if type(result) in [str, bytes]:
#                     accept_warnings.append(result)
#
#                 elif result:
#                     await _fp.seek(0)
#                     _im: Image = factory(_fp, None)
#                     _decompression_bomb_check(_im.size)
#                     return _im
#
#             except (SyntaxError, IndexError, TypeError, struct.error):
#                 # Leave disabled by default, spams the logs with image
#                 # opening failures that are entirely expected.
#                 # logger.debug("", exc_info=True)
#                 continue
#             except BaseException:
#                 if exclusive_fp:
#                     await _fp.close()
#
#                 raise
#
#         return None
#
#     im = await _open_core(fp, prefix, formats)
#
#     if im is None:
#         if init():
#             im = await _open_core(fp, prefix, formats)
#
#     if im:
#         im._exclusive_fp = exclusive_fp
#         return im
#
#     if exclusive_fp:
#         await fp.close()
#
#     for message in accept_warnings:
#         warnings.warn(message)
#
#     raise UnidentifiedImageError()


class ImageMixin:
    Width: int
    Height: int
    configure: callable
    update_idletasks: callable
    update: callable
    _IMG: Optional[tkPhotoImage]
    def __init__(self):
        self._IMG = None


    @overload
    def SetImage(self, img: tkPhotoImage):
        ...

    @overload
    def SetImage(self, url: URL, *formats: str, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs):
        ...
    @overload
    def SetImage(self, url: URL, *formats: str, widthMax: int, heightMax: int, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs):
        ...

    @overload
    def SetImage(self, path: Union[str, bytes, FilePath, Enum], *formats: str):
        ...
    @overload
    def SetImage(self, path: Union[str, bytes, FilePath, Enum], *formats: str, widthMax: int, heightMax: int):
        ...

    @overload
    def SetImage(self, base64data: Union[str, bytes, Enum], *formats: str):
        ...
    @overload
    def SetImage(self, base64data: Union[str, bytes, Enum], *formats: str, widthMax: int, heightMax: int):
        ...


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
    async def SetImageAsync(self, img: tkPhotoImage):
        ...

    @overload
    async def SetImageAsync(self, url: URL, *formats: str, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs):
        ...
    @overload
    async def SetImageAsync(self, url: URL, *formats: str, widthMax: int, heightMax: int, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs):
        ...

    @overload
    async def SetImageAsync(self, path: Union[str, bytes, FilePath, Enum], *formats: str):
        ...
    @overload
    async def SetImageAsync(self, path: Union[str, bytes, FilePath, Enum], *formats: str, widthMax: int, heightMax: int):
        ...

    @overload
    async def SetImageAsync(self, base64data: Union[str, bytes, Enum], *formats: str):
        ...
    @overload
    async def SetImageAsync(self, base64data: Union[str, bytes, Enum], *formats: str, widthMax: int, heightMax: int):
        ...


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
            f: AsyncBufferedReader
            async with async_file_open(data, 'rb') as f:
                raw = await f.read()

            return self.SetImageFromBytes(raw, *formats, width=widthMax, height=heightMax)

        return self.SetImageFromBytes(base64.b64decode(data), *formats, width=widthMax, height=heightMax)



    def SetImageFromBytes(self, data: bytes, *formats: str, width: int = None, height: int = None) -> 'ImageMixin':
        assert (isinstance(data, bytes))

        with BytesIO(data) as buf:
            return self._setImage(self.open(self, buf, width, height, *formats))


    @staticmethod
    def open(self: Union[BaseTkinterWidget, 'ImageMixin'], f: BinaryIO,
             widthMax: Optional[int], heightMax: Optional[int], *formats: str) -> tkPhotoImage:
        self.__updateSize__()

        if widthMax is None: widthMax = self.Width
        if heightMax is None: heightMax = self.Height

        if widthMax is None or widthMax <= 0: raise ValueError(f'widthMax must be positive. Value: {widthMax}')
        if heightMax is None or heightMax <= 0: raise ValueError(f'heightMax must be positive. Value: {heightMax}')

        with img_open(f, *formats) as img:
            img = img.resize(ImageMixin.CalculateNewSize(img, widthMax, heightMax))
            return tkPhotoImage(img, master=self)

    def _setImage(self, img: Optional[tkPhotoImage]) -> 'ImageMixin':
        self.update_idletasks()
        self._IMG = img
        self.configure(image=self._IMG)
        return self


    @staticmethod
    def Maximum_ScalingFactor(*options: float) -> float:
        return max(options)
    @staticmethod
    def Minimum_ScalingFactor(*options: float) -> float:
        return min(options)

    @staticmethod
    def Factors(img: Image, widthMax: int, heightMax: int) -> Tuple[float, float]:
        return widthMax / img.width, heightMax / img.height
    @staticmethod
    def CalculateNewSize(img: Image, widthMax: int, heightMax: int) -> Tuple[int, int]:
        options = ImageMixin.Factors(img, widthMax, heightMax)
        scalingFactor = ImageMixin.Minimum_ScalingFactor(*options)
        return ImageMixin.Scale(img, scalingFactor)
    @staticmethod
    def Scale(img: Image, factor: float) -> Tuple[int, int]:
        return int(img.width * (factor or 1)), int(img.height * (factor or 1))



# ------------------------------------------------------------------------------------------


class Updater(AutoStartThread, ABC):
    __slots__ = ['_app',
                 '_queue',
                 ]
    _app: 'BaseApp'
    _queue: Queue
    def __init__(self, app: 'BaseApp', queue: Queue):
        self._app = app
        self._queue = queue
        AutoStartThread.__init__(self)

    def stop(self): raise NotImplementedError()



class AsyncUpdater(AutoStartThread):
    __slots__ = ['_loop']
    _loop: Optional[AbstractEventLoop]
    def __init__(self, loop: AbstractEventLoop):
        self._loop = loop
        AutoStartThread.__init__(self)

    def run(self):
        self._loop.run_forever()

    def stop(self):
        self._loop.stop()

    @property
    def loop(self) -> AbstractEventLoop: return self._loop



_TUpdater = TypeVar('_TUpdater', Updater, AsyncUpdater)
class BaseApp(tkRoot, Generic[_TUpdater], ABC):
    """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
    __slots__ = ['logger',
                 '_logging_manager',
                 '_updater',
                 'NAME'
                 ]
    logger: Logger
    _logging_manager: LoggingManager
    _updater: _TUpdater
    NAME: Final[str]
    def __init__(self, updater: _TUpdater, app_name: str, *types: Type,
                 width: Optional[int] = None, height: Optional[int] = None, fullscreen: Optional[bool] = None, x: int = 0, y: int = 0, **kwargs):
        root_path = kwargs.pop('root_path', '.')
        tkRoot.__init__(self, width, height, fullscreen, x, y, **kwargs)

        self._logging_manager = LoggingManager.FromTypes(self.__class__, *types, app_name=app_name, root_path=FilePath.convert(root_path))
        self.logger = self.CreateLogger(self)
        self._updater = updater
        self.NAME = app_name
        self.SetTitle(app_name)

        self.protocol('WM_DELETE_WINDOW', self.Close)

        self.Bind(Bindings.ButtonPress, self._OnPress)
        self.Bind(Bindings.Key, self._OnKeyPress)
        self._setup()

    @property
    def DEBUG(self) -> bool:
        return __debug__

    def CreateLogger(self, source, *, debug: bool = __debug__) -> Logger:
        return self._logging_manager.CreateLogger(source, debug=debug)

    def GetLogger(self, source: Union[Type, Any]) -> Logger:
        return self.logger.getChild(typeof(source).__name__)


    def Close(self):
        """ Override to add functionality. Closes updater loop then closes application. """
        self._updater.stop()
        self.tk.quit()
    def start_gui(self, *_args, **_kwargs): raise NotImplementedError()

    def _setup(self):
        """Called on class creation. use this to create any required attributes, views, threads, processes, etc for the app to run."""
        raise NotImplementedError()


    def _OnPress(self, event: tkEvent) -> Optional[bool]:
        return self.Handle_Press(TkinterEvent(event))
    def Handle_Press(self, event: TkinterEvent) -> Optional[bool]:
        raise NotImplementedError()



    def _OnKeyPress(self, event: tkEvent) -> Optional[bool]:
        return self.Handle_KeyPress(TkinterEvent(event))
    def Handle_KeyPress(self, event: TkinterEvent) -> Optional[bool]:
        raise NotImplementedError()



class BaseAsyncApp(BaseApp[AsyncUpdater], ABC):
    """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
    __slots__ = ['_updater']
    def __init__(self, app_name: str,
                 *types: Type,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 x: int = 0,
                 y: int = 0,
                 fullscreen: Optional[bool] = None,
                 loop: Type[AbstractEventLoop] = None,
                 root_path: Union[str, FilePath] = '.',
                 updater: Type[AsyncUpdater] = None,
                 **kwargs):
        if fullscreen is None: fullscreen = not self.DEBUG
        _updater = (updater or AsyncUpdater)(loop or get_event_loop())

        BaseApp.__init__(self, _updater, app_name, *types, root_path=root_path, width=width, height=height, fullscreen=fullscreen, x=x, y=y, **kwargs)

    @property
    def loop(self) -> AbstractEventLoop:
        return self._updater.loop


    def start_gui(self, *_args, **_kwargs):
        try:
            self.tk.mainloop()
        except KeyboardInterrupt:
            self._updater.stop()
            return


class BaseSyncApp(BaseApp[Updater], ABC):
    """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
    __slots__ = ['queue']
    queue: Queue
    def __init__(self, app_name: str,
                 *types: Type,
                 x: int = 0,
                 y: int = 0,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 fullscreen: Optional[bool] = None,
                 root_path: Union[str, FilePath] = '.',
                 updater: Type[Updater] = None,
                 queue: Queue = Queue(),
                 **kwargs):
        if fullscreen is None: fullscreen = not self.DEBUG
        self.queue = queue
        _updater = (updater or Updater)(self, queue)
        BaseApp.__init__(self, _updater, app_name, *types, root_path=root_path, width=width, height=height, fullscreen=fullscreen, x=x, y=y, **kwargs)


    def start_gui(self, *_args, **_kwargs):
        try:
            self.tk.mainloop()
        except KeyboardInterrupt:
            return


    # @staticmethod
    # def InitAsync():
    #     set_event_loop_policy(AsyncTkinterEventLoopPolicy())


# ------------------------------------------------------------------------------------------


class _BaseFrameMixin:
    InstanceID: Optional[Union[str, int, Enum]]
    def __init__(self):
        self.InstanceID = None

    def SetID(self, InstanceID: Union[str, int, Enum]):
        self.InstanceID = InstanceID
        return self

    @property
    def __name__(self):
        try:
            base = super().__name__()
        except AttributeError:
            base = nameof(self)

        if self.InstanceID:
            if isinstance(self.InstanceID, Enum):
                InstanceID = self.InstanceID.value
            else:
                InstanceID = self.InstanceID

            return f'{base}_{InstanceID}'.lower()

        return base


# noinspection DuplicatedCode
class Frame(tk.Frame, BaseTkinterWidget, _BaseFrameMixin):
    __doc__ = """Frame widget which may contain other widgets and can have a 3D border."""
    __slots__ = ['InstanceID']
    def __init__(self, master, Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        _BaseFrameMixin.__init__(self)

    # noinspection PyProtectedMember
    def _options(self, cnf, kwargs=None) -> dict:
        # noinspection PyUnresolvedReferences
        return super()._options(cnf, convert_kwargs(kwargs))


class LabelFrame(tk.LabelFrame, BaseTextTkinterWidget, _BaseFrameMixin):
    __doc__ = """Construct a labelframe _widget with the master MASTER.

    STANDARD OPTIONS

        borderwidth, cursor, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, padx, pady, relief,
        takefocus, text

    WIDGET-SPECIFIC OPTIONS

        background, class, colormap, container,
        Height, labelanchor, labelwidget,
        visual, Width
    """
    __slots__ = ['InstanceID']
    def __init__(self, master, text: str = '', Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        tk.LabelFrame.__init__(self, master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, None, Color, loop, configure=False)
        _BaseFrameMixin.__init__(self)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)

    # noinspection PyProtectedMember
    def _options(self, cnf, kwargs=None) -> dict:
        # noinspection PyUnresolvedReferences
        return super()._options(cnf, convert_kwargs(kwargs))


# noinspection DuplicatedCode
class FrameThemed(ttk.Frame, BaseTkinterWidget, _BaseFrameMixin):
    __doc__ = """Ttk Frame widget is a container, used to group other widgets together."""
    __slots__ = ['InstanceID']
    def __init__(self, master, Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        _BaseFrameMixin.__init__(self)

    # noinspection PyProtectedMember
    def _options(self, cnf, kwargs=None) -> dict:
        # noinspection PyUnresolvedReferences
        return super()._options(cnf, convert_kwargs(kwargs))


class LabelFrameThemed(ttk.LabelFrame, BaseTextTkinterWidget, _BaseFrameMixin):
    __doc__ = """Construct a labelframe _widget with the master MASTER.

    STANDARD OPTIONS

        borderwidth, cursor, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, padx, pady, relief,
        takefocus, text

    WIDGET-SPECIFIC OPTIONS

        background, class, colormap, container,
        Height, labelanchor, labelwidget,
        visual, Width
    """
    __slots__ = ['InstanceID']
    def __init__(self, master, text: str = '', Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        ttk.LabelFrame.__init__(self, master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, None, Color, loop, configure=False)
        _BaseFrameMixin.__init__(self)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)

    # noinspection PyProtectedMember
    def _options(self, cnf, kwargs=None) -> dict:
        # noinspection PyUnresolvedReferences
        return super()._options(cnf, convert_kwargs(kwargs))


# ------------------------------------------------------------------------------------------


_TBaseApp = TypeVar('_TBaseApp', bound=BaseApp)
class _WindowMixin(Generic[_TBaseApp]):
    __log_name__: str
    _app: _TBaseApp
    def __init__(self, app: _TBaseApp):
        assert (isinstance(app, BaseApp))
        self._app = app
        self._logger = app.logger.getChild(str(class_name(self)))

    def OnPress(self, event: TkinterEvent): pass
    def OnKeyPress(self, event: TkinterEvent): pass


class BaseWindow(Frame, _WindowMixin[_TBaseApp]):
    def __init__(self, master, app: _TBaseApp, **kwargs):
        Frame.__init__(self, master, **kwargs)
        _WindowMixin.__init__(self, app)

    @classmethod
    def Root(cls, app: _TBaseApp, **kwargs):
        return cls(app, app, **kwargs)


class BaseLabelWindow(LabelFrame, _WindowMixin[_TBaseApp]):
    def __init__(self, master, app: _TBaseApp, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        _WindowMixin.__init__(self, app)

    @classmethod
    def Root(cls, app: _TBaseApp, **kwargs):
        return cls(app, app, **kwargs)
