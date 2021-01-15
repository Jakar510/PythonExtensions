# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------


import base64
import io
import os
from abc import ABC
from enum import Enum
from pprint import PrettyPrinter
from types import FunctionType, MethodType
from typing import Union
from urllib.request import urlopen

from PIL import Image, ImageTk

from ..Enumerations import *
from BaseExtensions.Images import *
from ..Widgets.base import *




pp = PrettyPrinter(indent=4)

__all__ = [
        'BaseTkinterWidget', 'BaseTextTkinterWidget',
        'Image', 'ImageTk',
        'CurrentValue', 'CallWrapper', 'CurrentValue',
        'CommandMixin', 'ImageMixin',
        ]

class BaseTkinterWidget(tk.Widget, ABC):
    # noinspection PyMissingConstructor
    def __init__(self, Color: dict = None, ):
        if Color: self.configure(**Color)

    _state_: ViewState = ViewState.Hidden
    _pi: dict = { }
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
        if IncludeState is None: return f'<{start}. State: {pp.pformat(self.Details)}>'
        if IncludeState: return f'<{start}. State: {pp.pformat(self.FullDetails)}>'

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
    def width(self) -> int: return self.winfo_width()
    @property
    def height(self) -> int: return self.winfo_height()

    @property
    def x(self) -> int: return self.winfo_rootx()
    @property
    def y(self) -> int: return self.winfo_rooty()


    def show(self, **kwargs) -> bool:
        """
        Shows the current widget or _root_frame, based on the current geometry manager.
        Can be overridden to add additional functionality if needed.
        """
        if self._manager_ is None: return False

        state = kwargs.get('state', None) or kwargs.get('State', ViewState.Normal)
        assert (isinstance(state, ViewState))

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

    def hide(self) -> bool:
        """
        Hides the current widget or _root_frame, based on the current geometry manager.
        Can be overridden to add additional functionality if needed.
        """
        if self._manager_ is None: return False

        self.OnDisppearing()
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



    def Bind(self, sequence: str or Enum = None, func: callable = None, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind(sequence, func, add)

    def BindAll(self, sequence: str or Enum = None, func: callable = None, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind_all(sequence, func, add)
    def UnBindAll(self, sequence: str or Enum = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.unbind_all(sequence)

    def BindClass(self, className, sequence: str or Enum = None, func: callable = None, add: bool = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind_class(className, sequence, func, add)
    def UnBindClass(self, className, sequence: str or Enum = None) -> str:
        if isinstance(sequence, Enum): sequence = sequence.value
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
    def OnDisppearing(self):
        """ this is called just before widget disappears. override to implement desired effects """
        pass


class BaseTextTkinterWidget(BaseTkinterWidget):
    _txt: tk.StringVar
    # noinspection PyMissingConstructor
    def __init__(self, *, Override_var: tk.StringVar = None, text: str, Color: dict = None, configure: bool = True):
        if Override_var is not None: self._txt = Override_var
        else: self._txt = tk.StringVar(master=self, value=text)

        if configure: self.configure(textvariable=self._txt)
        BaseTkinterWidget.__init__(self, Color)
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


class CallWrapper(tk.CallWrapper):
    """ Internal class. Stores function to call when some user defined Tcl function is called e.g. after an event occurred. """

    _func: callable
    _widget: Union[BaseTextTkinterWidget, BaseTkinterWidget] = None
    def __init__(self, func: callable, widget: BaseTkinterWidget = None):
        """Store FUNC, SUBST and WIDGET as members."""
        self._func: callable = func
        self._widget = widget

    def __call__(self, *args, **kwargs):
        """Apply first function SUBST to arguments, than FUNC."""
        try:
            return self._func(*args, **kwargs)
        except SystemExit: raise
        except Exception:
            if hasattr(self._widget, '_report_exception'):
                # noinspection PyProtectedMember
                self._widget._report_exception()
            else: raise

    def __repr__(self) -> str: return f'{super().__repr__().replace(">", "")} [ {dict(func=self._func, widget=self._widget)} ]>'
    def __str__(self) -> str: return repr(self)

    def SetWidget(self, w: BaseTkinterWidget):
        """ Internal Method """
        assert (isinstance(w, BaseTkinterWidget))
        self._widget = w
        return self

    @classmethod
    def Create(cls, func: callable, z: int or str = None, widget: BaseTkinterWidget = None, **kwargs):
        if z is not None and kwargs and func:
            return cls(lambda x=kwargs: func(z, **x), widget=widget)
        elif kwargs and func:
            return cls(lambda x=kwargs: func(**x), widget=widget)
        elif z is not None and func:
            return cls(lambda x=z: func(x), widget=widget)
        elif func:
            return cls(func, widget=widget)

        return None
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



class CommandMixin:
    _cmd: CallWrapper
    configure: callable
    command_cb: str
    def __call__(self, *args, **kwargs):
        """ Execute the Command """
        if callable(self._cmd): self._cmd(*args, **kwargs)
    def SetCommand(self, func: Union[callable, FunctionType, MethodType, CurrentValue], z: Union[int, float, str, Enum] = None, add: bool = False, **kwargs):
        """
        :param func: function or method being called.
        :type func: Union[callable, FunctionType, MethodType, CurrentValue]
        :param z: arg passed to the fucntion.
        :type z: Union[int, float, str, Enum]
        :param add: if False, replaces the current function.
        :type add: bool
        :param kwargs: keyword args passed to the function.
        :type kwargs: Dict[str, Any]
        :return: returns self to enable chaining.
        """
        if not callable(func):
            raise ValueError(f'func is not callable. got {type(func)}')

        if isinstance(func, CurrentValue): self._cmd = func.SetWidget(self)
        else: self._cmd = CallWrapper.Create(func, z, **kwargs)

        return self._setCommand(add)
    def _setCommand(self, add: bool):
        self.configure(command=self._cmd)
        return self
class ImageMixin:
    width: int
    height: int
    configure: callable
    update_idletasks: callable
    update: callable
    _IMG: Union[ImageTk.PhotoImage, tk.PhotoImage] = None
    def SetImage(self, path: str = None, *, WidthMax: int = None, HeightMax: int = None):
        if not os.path.isfile(path): raise FileNotFoundError(path)
        with open(path, 'rb') as f:
            return self._open(f, WidthMax, HeightMax)
    def SetPhoto(self, base64Data: bytes or str = None, *, WidthMax: int = None, HeightMax: int = None):
        with io.BytesIO(base64.b64decode(base64Data)) as buf:
            return self._open(buf, WidthMax, HeightMax)
    def DownloadImage(self, url: str, *, WidthMax: int = None, HeightMax: int = None):
        with io.BytesIO(urlopen(url).read()) as buf:
            return self._open(buf, WidthMax, HeightMax)

    def _open(self, f, WidthMax: int, HeightMax: int):
        self.update_idletasks()
        if WidthMax is None: WidthMax = self.width
        if HeightMax is None: HeightMax = self.height

        if WidthMax <= 0: raise ValueError(f'WidthMax must be positive. Value: {WidthMax}')
        if HeightMax <= 0: raise ValueError(f'HeightMax must be positive. Value: {HeightMax}')
        with Image.open(f) as img:
            self._IMG = ImageTk.PhotoImage(master=self, image=ResizePhoto(img, WidthMax=WidthMax, HeightMax=HeightMax))
            self.configure(image=self._IMG)

        return self
