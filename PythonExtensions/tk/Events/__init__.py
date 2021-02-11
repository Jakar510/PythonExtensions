# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

import pprint
from tkinter import Event as tkEvent, EventType as tkEventType
from typing import *

from .Bindings import Bindings
from ...Json import Point
from ...Names import nameof
from ...misc import lazy_property




__all__ = ['TkinterEvent', 'Bindings', 'tkEvent']

class TkinterEvent(tkEvent):
    """
    Event Container for the properties of an event.
    See tkinter.Misc._substitute for event creation

        Instances of this type are generated if one of the following events occurs:

            For keyboard events

                • KeyPress
                • KeyRelease


            For mouse events:

                • ButtonPress
                • ButtonRelease
                • Motion
                • Enter
                • Leave
                • MouseWheel
                • Visibility
                • Unmap
                • Map
                • Expose
                • FocusIn
                • FocusOut
                • Circulate


            For window events:

                • Colormap
                • Gravity
                • Reparent
                • Property
                • Destroy
                • Activate
                • Deactivate

        If a callback function for one of these events is registered using bind, bind_all, bind_class, or tag_bind, the callback is called with an Event as first argument.
        It will have the following attributes (in braces are the event types for which the attribute is valid):

            serial - serial number of event

            num - mouse button pressed (ButtonPress, ButtonRelease)

            focus - whether the window has the focus (Enter, Leave)

            height - height of the exposed window (Configure, Expose)

            width - width of the exposed window (Configure, Expose)

            keycode - keycode of the pressed key (KeyPress, KeyRelease)

            state - state of the event as a number (ButtonPress, ButtonRelease, Enter, KeyPress, KeyRelease, Leave, Motion) OR state as a string (Visibility)

            time - when the event occurred

            x - x-position of the mouse

            y - y-position of the mouse

            x_root - x-position of the mouse on the screen (ButtonPress, ButtonRelease, KeyPress, KeyRelease, Motion)

            y_root - y-position of the mouse on the screen (ButtonPress, ButtonRelease, KeyPress, KeyRelease, Motion)

            char - pressed character (KeyPress, KeyRelease)

            send_event - see X/Windows documentation

            keysym - keysym of the event as a string (KeyPress, KeyRelease)

            keysym_num - keysym of the event as a number (KeyPress, KeyRelease)

            type - type of the event as a number or <enum 'tkinter.EventType'>

            widget - widget in which the event occurred

            delta - delta of wheel movement (MouseWheel)

    """
    __slots__ = ['serial', 'num', 'height', 'keycode', 'state', 'time', 'width', 'x', 'y', 'char', 'keysym', 'keysym_num', 'type', 'widget', 'x_root', 'y_root', 'delta',
                 'send_event']

    def __init__(self, source: tkEvent = None):
        super().__init__()
        if source is not None:
            assert (isinstance(source, tkEvent))
            self.__dict__.update(source.__dict__)
            for name, value in source.__dict__.items(): setattr(self, name, value)


    def __str__(self) -> str: return self.ToString()
    # def __repr__(self) -> str: return self.ToString()

    def ToString(self) -> str: return f"""<{nameof(self)} ({repr(self).replace('>', '').replace('<', '')}) Object.
{pprint.pformat(self.ToDict(), indent=4)} >"""
    def ToDict(self) -> dict:
        """
            {
                'num': self.num,
                'height': self.height,
                'width': self.width,
                'widget': self.widget,
                'keysym': self.keysym,
                'keycode': self.keycode,
                'keysym_num': self.keysym_num,
                'state': self.state,
                'time': self.time,
                'x': self.x,
                'y': self.y,
                'char': self.char,
                'type': self.type,
                'x_root': self.x_root,
                'y_root': self.y_root,
                'delta': self.delta,
            }
        :return:
        """
        d = self.__dict__.copy()
        d['KeySynonym'] = self.KeySynonym
        return d

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass
    def __call__(self, *, keysym: Bindings = None) -> bool:
        if keysym is not None: return self.KeySynonym == keysym

        raise ValueError('Unknown value passed')

    @staticmethod
    def IsDigit(keysym: int or str) -> bool:
        """
        :param keysym:
        :type keysym: int or str or TkinterEvent
        :return:
        :rtype: bool
        """
        if isinstance(keysym, TkinterEvent): keysym = keysym.keysym
        return Bindings.IsDigit(keysym)

    @property
    def EventType(self) -> tkEventType: return self.type

    @lazy_property
    def KeySynonym(self) -> Bindings: return Bindings.FromEvent(self)

    def IsEnter(self) -> bool: return Bindings.IsEnter(self.keysym)

    @staticmethod
    def IsValid(o: str):
        try:
            return o != '??'
        except (TypeError, ValueError) as e:
            raise TypeError(f'expected str, got {type(o)}') from e

    @classmethod
    def FromShiftTabEvent(cls, event: tkEvent):
        e = cls(event)
        e.keysym = Bindings.ShiftTab.value
        return e


    @staticmethod
    def Debug(event: tkEvent):
        print('Debug.tkEvent', event)
        event = TkinterEvent(event)
        print('Debug.TkinterEvent', event.ToString())
        print(event.KeySynonym)

    def Point(self) -> Optional[Point]:
        if isinstance(self.x, (float, int)) and isinstance(self.y, (float, int)): return Point.Create(self.x, self.y)
        return None
