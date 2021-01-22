# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
from enum import Enum
from time import time
from typing import *

from .BaseWidgets import BaseTkinterWidget
from ..Enumerations import Orientation
from ..Events import Bindings
from ..Widgets.Style import *
from ..Widgets.base import *




__all__ = [
    'tkRoot', 'tkTopLevel',
    ]



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

    update: callable
    update_idletasks: callable
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


class tkRoot(tk.Tk, _rootMixin):
    def __init__(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)
        self.style = Style(master=self)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    def Create_Event(self, tag: Union[str, Bindings], *, num: int = '??', height: int = '??', width: int = '??', key_code: int = '??', state: int = '??',
                     x: int = '??', y: int = '??', char: str = '??', keysym: int = '??', keysym_num: int = '??', delta: int = '??',
                     event_type: tk.EventType, widget: tk.Widget, current_time=time()):
        """
            example:
                <TkinterEvent Object. Configuration:
                {   'char': 'a',
                    'delta': 0,
                    'height': '??',
                    'keycode': 65,
                    'keysym': 'a',
                    'keysym_num': 97,
                    'num': '??',
                    'state': 8,
                    'time': 329453312,
                    'type': <EventType.KeyPress: '2'>,
                    'widget': <spf.Workers.Views.Carousel.CarouselView object .!carouselview>,
                    'width': '??',
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
                height - height of the exposed window (Configure, Expose)
                width - width of the exposed window (Configure, Expose)
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
        :param height: height of the exposed window (Configure, Expose)
        :param width: width of the exposed window (Configure, Expose)
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

        self.event_generate(sequence=tag, num=num, height=height, keycode=key_code, state=state, time=current_time, width=width, x=x, y=y, char=char, keysym=keysym,
                            keysym_num=keysym_num, type=event_type, widget=widget, x_root=self.winfo_rootx(), y_root=self.winfo_rooty(), delta=delta)

class tkTopLevel(tk.Toplevel, _rootMixin):
    def __init__(self, master, *, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(master, **kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.style = master.style

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))
