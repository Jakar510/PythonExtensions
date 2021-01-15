# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
from enum import Enum, IntEnum

from .BaseWidgets import BaseTkinterWidget
from ..Widgets.Style import *
from ..Widgets.base import *




__all__ = [
        'tkRoot', 'tkTopLevel', 'Orientation',
        ]

class Orientation(IntEnum):
    Landscape = 0
    Portrait = 1


class _rootMixin:
    Style: Style = None
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

    attributes: callable
    resizable: callable
    def SetDimmensions(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0):
        self.Screen_Width = Screen_Width or int(self.winfo_screenwidth())
        self.Screen_Height = Screen_Height or int(self.winfo_screenheight())
        return self.geometry(self.Dimmensions(x, y))
    def Dimmensions(self, x: int = 0, y: int = 0) -> str: return f"{self.Screen_Width}x{self.Screen_Height}+{x}+{y}"

    def HideCursor(self):
        self.config(cursor="none")
        return self

    def SetFullScreen(self, fullscreen: bool = False, ):
        self.attributes('-fullscreen', fullscreen)
        return self
    def SetTitle(self, title: str):
        self.title(title)
        return self
    def SetResizable(self, resizable: bool):
        self.resizable(width=resizable, height=resizable)
        return self

    def Bind(self, sequence: str or Enum = None, func: callable = None, add: bool = None):
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind(sequence, func, add)

    def MultiUnbindAll(self, *args: str or Enum):
        for arg in args: self.UnbindAll(arg)
    def UnbindAll(self, sequence: str or Enum = None):
        """Unbind for all widgets for event SEQUENCE all functions."""
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.unbind_all(sequence)

    def BindAll(self, sequence: str or Enum = None, func: callable = None, add: bool = None):
        """Bind to all widgets at an event SEQUENCE a call to function FUNC.
        An additional boolean parameter ADD specifies whether FUNC will
        be called additionally to the other bound function or whether
        it will replace the previous function. See bind for the return value."""
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind_all(sequence, func, add)

    @property
    def width(self) -> int: return self.winfo_width()
    @property
    def height(self) -> int: return self.winfo_height()

    @property
    def x(self) -> int: return self.winfo_x()
    @property
    def y(self) -> int: return self.winfo_y()


    @property
    def Orientation(self) -> Orientation: return Orientation.Landscape if self.Screen_Width > self.Screen_Height else Orientation.Portrait

    def SetTransparency(self, v: float):
        assert (0.0 <= v <= 1.0)
        return self.attributes('-alpha', v)


# noinspection DuplicatedCode
class tkRoot(tk.Tk, _rootMixin):
    def __init__(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)
        self.style = Style(master=self)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))


# noinspection DuplicatedCode
class tkTopLevel(tk.Toplevel, _rootMixin):
    def __init__(self, master, *, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.style = master.style

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))
