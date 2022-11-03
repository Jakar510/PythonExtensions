import re
from enum import StrEnum, Enum
from pprint import pformat

from PIL.Image import Image
from PIL.ImageTk import PhotoImage

from .Enums import *
import tkinter as tk
import tkinter.ttk as ttk
from typing import *

from libcpp import bool as cppbool, nullptr_t




#region tkEventType

cpdef class tkEventType(StrEnum):
    pass

#endregion Events

#region Bindings

cpdef class Bindings(StrEnum):
    __doc__ = """ https://www.tcl.tk/man/tcl8.6/TkCmd/event.htm """
    __slots__ = []
    UNKNOWN = '??'

    # class Special(Enum):
    Activate = '<Activate>'
    Configure = '<Configure>'
    Deactivate = '<Deactivate>'
    Destroy = '<Destroy>'
    Expose = '<Expose>'
    Map = '<Map>'
    Motion = '<Motion>'
    MouseWheel = '<MouseWheel>'
    ShiftMouseWheel = '<Shift-MouseWheel>'
    Unmap = '<Unmap>'
    Visibility = '<Visibility>'
    WM_DELETE_WINDOW = 'WM_DELETE_WINDOW'

    # class Mouse(Enum):
    B1_Motion = '<B1-Motion>'
    B2_Motion = '<B2-Motion>'
    B3_Motion = '<B3-Motion>'
    B4_Motion = '<B4-Motion>'
    B5_Motion = '<B5-Motion>'

    ButtonPress = '<Button>'
    ButtonPress1 = '<Button-1>'
    ButtonPress2 = '<Button-2>'
    ButtonPress3 = '<Button-3>'
    ButtonPress4 = '<Button-4>'
    ButtonPress5 = '<Button-5>'

    ShiftButtonPress = '<Shift-Button>'
    ShiftButtonPress1 = '<Shift-Button-1>'
    ShiftButtonPress2 = '<Shift-Button-2>'
    ShiftButtonPress3 = '<Shift-Button-3>'
    ShiftButtonPress4 = '<Shift-Button-4>'
    ShiftButtonPress5 = '<Shift-Button-5>'

    ButtonRelease = '<ButtonRelease>'
    ButtonRelease1 = '<ButtonRelease-1>'
    ButtonRelease2 = '<ButtonRelease-2>'
    ButtonRelease3 = '<ButtonRelease-3>'
    ButtonRelease4 = '<ButtonRelease-4>'
    ButtonRelease5 = '<ButtonRelease-5>'

    Double_Button = '<Double-Button>'
    Double_Button2 = '<Double-Button-2>'
    Double_Button3 = '<Double-Button-3>'
    Double_Button4 = '<Double-Button-4>'
    Double_Button5 = '<Double-Button-5>'

    # class UpperCase(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'
    J = 'J'
    K = 'K'
    L = 'L'
    M = 'M'
    N = 'N'
    O = 'O'
    P = 'P'
    Q = 'Q'
    R = 'R'
    S = 'S'
    T = 'T'
    U = 'U'
    V = 'V'
    W = 'W'
    X = 'X'
    Y = 'Y'
    Z = 'Z'

    # class LowerCase(Enum):
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'
    f = 'f'
    g = 'g'
    h = 'h'
    i = 'i'
    j = 'j'
    k = 'k'
    l = 'l'
    m = 'm'
    n = 'n'
    o = 'o'
    p = 'p'
    q = 'q'
    r = 'r'
    s = 's'
    t = 't'
    u = 'u'
    v = 'v'
    w = 'w'
    x = 'x'
    y = 'y'
    z = 'z'

    Zero = '0'
    One = '1'
    Two = '2'
    Three = '3'
    Four = '4'
    Five = '5'
    Size = '6'
    Seven = '7'
    Eight = '8'
    Nine = '9'

    # class Custom(Enum):
    ShiftTab = 'Shift_Tab',
    ShiftTabEvent = '<Shift-KeyPress-Tab>'

    # class FunctionKeys(Enum):
    F1 = '<F1>'
    F2 = '<F2>'
    F3 = '<F3>'
    F4 = '<F4>'
    F5 = '<F5>'
    F6 = '<F6>'
    F7 = '<F7>'
    F8 = '<F8>'
    F9 = '<F9>'
    F10 = '<F10>'
    F11 = '<F11>'
    F12 = '<F12>'

    # class Foucs(Enum):
    Next = 'Next'
    Prior = 'Prior'
    FocusIn = '<FocusIn>'
    FocusOut = '<FocusOut>'
    Enter = '<Enter>'
    Leave = '<Leave>'
    NextWindow = '<<NextWindow>>'
    PrevWindow = '<<PrevWindow>>'

    # class Core(Enum):
    Alt = 'Alt'
    Alt_L = 'Alt_L'
    Alt_R = 'Alt_R'
    AsciiTilde = 'asciitilde'
    BackSlash = 'backslash'
    BackSpace = 'BackSpace'
    BracketLeft = 'bracketleft'
    BracketRight = 'bracketright'
    Cancel = 'Cancel'
    Caps_Lock = 'Caps_Lock'
    Comma = 'comma'
    Control = 'Control'
    Control_L = 'Control_L'
    Control_R = 'Control_R'
    Delete = 'Delete'
    Down = 'Down'
    End = 'End'
    EnterKey = 'Enter'
    ControlEnter = '<Control-KeyPress-Return>'
    Equal = 'equal'
    Escape = 'Escape'
    Home = 'Home'
    Insert = 'Insert'
    KP_Add = 'KP_Add'
    KP_Enter = 'KP_Enter'
    KP_Subtract = 'KP_Subtract'
    Key = '<Key>'
    Left = 'Left'
    Minus = 'minus'
    Num_Lock = 'Num_Lock'
    Pause = 'Pause'
    Period = 'period'
    Plus = 'plus'
    Print = 'Print'
    QuoteLeft = 'quoteleft'
    QuoteRight = 'quoteright'
    Return = 'Return'
    Right = 'Right'
    Scroll_Lock = 'Scroll_Lock'
    Semicolon = 'semicolon'
    Shift = 'Shift'
    Shift_R = 'Shift_R'
    Shift_L = 'Shift_L'
    Shift_Down = '<Shift-Down>'
    Shift_Left = '<Shift-Left>'
    Shift_Right = '<Shift-Right>'
    Shift_Up = '<Shift-Up>'
    Slash = 'slash'
    Space = 'space'
    Tab = 'Tab'
    Up = 'Up'

    # class ListBox(Enum):
    ListboxSelect = '<<ListboxSelect>>'

    # class ComboBox(Enum):
    ComboboxSelected = '<<ComboboxSelected>>'

    # class Text(Enum):
    Selection = '<<Selection>>'

    # class Numbers(Enum):
    eight = '8'
    five = '5'
    four = '4'
    nine = '9'
    one = '1'
    seven = '7'
    six = '6'
    three = '3'
    two = '2'
    zero = '0'

    # class ThemedTreeView(Enum):
    TreeViewSelect = '<<TreeviewSelect>>'
    TreeviewOpen = '<<TreeviewOpen>>'
    TreeviewClose = '<<TreeviewClose>>'

    # media controls XF86Audio
    XF86AudioPlay = 'XF86AudioPlay'
    XF86AudioRaiseVolume = 'XF86AudioRaiseVolume'
    XF86AudioLowerVolume = 'XF86AudioLowerVolume'
    XF86AudioMute = 'XF86AudioMute'
    XF86AudioPrev = 'XF86AudioPrev'
    XF86AudioNext = 'XF86AudioNext'
    XF86Sleep = 'XF86Sleep'
    XF86Search = 'XF86Search'
    XF86TouchpadToggle = 'XF86TouchpadToggle'

    @staticmethod
    cpdef bool IsUnknown(str keysym):
        """
        :param keysym:
        :type keysym: Bindings or str
        :return:
        :rtype: bool
        """
        if isinstance(keysym, str): return keysym == Bindings.UNKNOWN.value

        return keysym == Bindings.UNKNOWN

    @staticmethod
    cpdef bool IsKnown(str keysym):
        """
        :param keysym:
        :type keysym: Bindings or str
        :return:
        :rtype: bool
        """
        if isinstance(keysym, str): return keysym != Bindings.UNKNOWN.value

        return keysym != Bindings.UNKNOWN

    @staticmethod
    cpdef bool IsDigit(TkinterEvent event):
        """
        :param event:
        :type event: int or str or Bindings
        :return:
        :rtype: bool
        """
        return event.keysym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'period', 'comma', ',', '.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    @staticmethod
    cpdef bool IsDigit(Bindings event):
        """
        :param event:
        :type event: int or str or Bindings
        :return:
        :rtype: bool
        """
        return event.value in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'period', 'comma', ',', '.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    @staticmethod
    cpdef bool IsEnter(str keysym):
        """
        :param keysym:
        :type keysym: Bindings or str
        :return:
        :rtype: bool
        """
        if isinstance(keysym, str): keysym = Bindings.FromKeysym(keysym)

        return keysym == Bindings.EnterKey or keysym == Bindings.KP_Enter or keysym == Bindings.Return

    @staticmethod
    cpdef Bindings FromKeysym(str keysym):
        """
        :param keysym: binding type string
        :type keysym: str
        :return: resulting Binding match
        :rtype: Bindings
        """
        try:
            return Bindings(keysym)
        except ValueError as e:
            if hasattr(Bindings, keysym): return getattr(Bindings, keysym)
            for name in dir(Bindings):
                if name.lower() == keysym.lower():
                    return getattr(Bindings, name)

            raise ValueError(f'Cannot find matching event: "{keysym}"') from e

    @staticmethod
    cpdef Bindings FromEvent(TkinterEvent event):
        """
        :param event: associated event
        :type event: TkinterEvent
        :return: resulting Binding match
        :rtype: Bindings
        """
        if Bindings.IsKnown(event.keysym) and Bindings.IsKnown(event.num):
            return Bindings.FromKeysym(f'{event.EventType.name}{event.num}')

        return Bindings.FromKeysym(event.keysym)

#endregion Events

#region Events

cpdef class TkinterEvent(object):
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

            Height - Height of the exposed window (Configure, Expose)

            Width - Width of the exposed window (Configure, Expose)

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

    """
    cpdef readonly int num
    cpdef readonly int width
    cpdef readonly int height
    cpdef readonly int state
    cpdef readonly int time
    cpdef readonly float x
    cpdef readonly float y
    cpdef readonly float x_root
    cpdef readonly float y_root
    cpdef readonly float delta
    cpdef readonly str * keycode
    cpdef readonly str * character
    cpdef readonly str * keysym
    cpdef readonly str * keysym_num
    cpdef readonly str * send_event
    cpdef readonly tkEventType * type
    cpdef readonly Widget * widget
    cpdef readonly bool focus

    def __cinit__(self, str keycode, int num, int height =-1, int width, int key_code, int state, int  x, int y, str char, str keysym, int keysym_num, int delta,
                  float x_root = 0, float y_root = 0, tkEventType event_type, Widget widget, float time, bool focus):
        self.num = num
        self.width = width
        self.height = height
        self.state = state
        self.time = time
        self.x = x
        self.y = y
        self.x_root = x_root
        self.y_root = y_root
        self.keycode = keycode
        self.character = char
        self.keysym = keysym
        self.type = event_type
        self.widget = widget
        self.focus = focus

    @classmethod
    cpdef TkinterEvent Create(cls, tkRoot root, int num = -1, int height =-1, int width = -1, int key_code = -1, int state = -1,
                              int  x = -1, int y = -1, str keycode = '??', str keysym = '??', int keysym_num = -1, int delta = -1,
                              tkEventType event_type, Widget widget, current_time=time()):
        return cls.__new__(cls, keycode, num, width, height, state, x, y, char, keysym, keysym_num, type, widget, root.winfo_rootx(), root.winfo_rooty(), delta, current_time)

    def __str__(self) -> str:
        return f"""<TkinterEvent(). {pformat(self.ToDict(), indent=4)} >"""

    def ToDict(self):
        return {
            'KeySynonym': self.KeySynonym,
            'IsDigit':    self.IsDigit(self.KeySynonym),
            'IsEnter':    self.IsEnter(),
            'IsValid':    self.IsValid(),
            # 'serial':     self.serial,
            'num':        self.num,
            'Height':     self.height,
            'keycode':    self.keycode,
            'state':      self.state,
            'time':       self.time,
            'Width':      self.width,
            'x':          self.x,
            'y':          self.y,
            'char':       self.character,
            'keysym':     self.keysym,
            'keysym_num': self.keysym_num,
            'type':       self.type,
            'widget':     self.widget,
            'x_root':     self.x_root,
            'y_root':     self.y_root,
            'delta':      self.delta,
            'send_event': self.send_event
            }

    cpdef bool __call__(self, Bindings keysym):
        return self.KeySynonym == keysym

    @staticmethod
    cpdef bool IsDigit(TkinterEvent keysym):
        """
        :param keysym:
        :type keysym: int or str or TkinterEvent
        :return:
        :rtype: bool
        """
        if isinstance(keysym, TkinterEvent): keysym = keysym.keysym
        return Bindings.IsDigit(keysym)

    cpdef tkEventType EventType(self):
        return &self.type

    cpdef Bindings KeySynonym(self):
        return Bindings.FromEvent(self)

    cpdef bool IsEnter(self):
        return Bindings.IsEnter(self.keysym)

    cpdef bool IsValid(self):
        return Bindings.IsKnown(self.keysym)

    @classmethod
    cpdef TkinterEvent FromShiftTabEvent(cls, TkinterEvent event):
        e = cls.__new__(event)
        e.keysym = Bindings.ShiftTab.value
        return e

    cpdef (float, float) Point(self):
        return self.x, self.y

#endregion Events


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

    def Bind(self, sequence: Bindings = None, func: callable = None, add: bool = None):
        return self.bind(sequence.value, func, add)

    def MultiUnbindAll(self, *args: Bindings):
        for arg in args: self.UnbindAll(arg)
    def UnbindAll(self, sequence: Bindings = None):
        """Unbind for all widgets for event SEQUENCE all functions."""
        return self.unbind_all(sequence.value)

    def BindAll(self, sequence: Bindings = None, func: callable = None, add: bool = None):
        """Bind to all widgets at an event SEQUENCE a call to function FUNC.
        An additional boolean parameter ADD specifies whether FUNC will
        be called additionally to the other bound function or whether
        it will replace the previous function. See bind for the return value."""
        return self.bind_all(sequence.value, func, add)

    @property
    def Width(self) -> int:
        return self.winfo_width()
    @property
    def Height(self) -> int:
        return self.winfo_height()

    @property
    def X(self) -> int:
        return self.winfo_x()
    @property
    def Y(self) -> int:
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

_magic_re = re.compile(r'([\\{}])')
_space_re = re.compile(r'([\s])', re.ASCII)

def _join(value):
    """Internal function."""
    return ' '.join(map(_stringify, value))

def _stringify(value):
    """Internal function."""
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            value = _stringify(value[0])
            if _magic_re.search(value):
                value = '{%s}' % value
        else:
            value = '{%s}' % _join(value)
    else:
        value = str(value)
        if not value:
            value = '{}'
        elif _magic_re.search(value):
            # add '\' before special characters and spaces
            value = _magic_re.sub(r'\\\1', value)
            value = value.replace('\n', r'\n')
            value = _space_re.sub(r'\\\1', value)
            if value[0] == '"':
                value = '\\' + value
        elif value[0] == '"' or _space_re.search(value):
            value = '{%s}' % value
    return value

def _flatten(seq: Iterable):
    """Internal function."""
    res = ()
    for item in seq:
        if isinstance(item, (tuple, list)):
            res = res + _flatten(item)
        elif item is not None:
            res = res + (item,)
    return res

def _cnfmerge(cnfs):
    """Internal function."""
    if isinstance(cnfs, dict):
        return cnfs
    elif isinstance(cnfs, (type(None), str)):
        return cnfs
    else:
        cnf = { }
        for c in _flatten(cnfs):
            try:
                cnf.update(c)
            except (AttributeError, TypeError) as msg:
                print("_cnfmerge: fallback due to:", msg)
                for k, v in c.items():
                    cnf[k] = v
        return cnf

def convert_kwargs(kwargs: Dict[str, Any], lower: bool = True) -> Optional[Dict[str, Any]]:
    """
        Converts all keys to lowercase strings, for tkinter
    :param kwargs:
    :param lower:
    :return:
    """
    if kwargs is None: return None

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

    def merge_options(self, cnf: Dict[str, Any], kwargs: Dict[str, Any] = None) -> Tuple[str, ...]:
        """Internal function."""
        kw = convert_kwargs(kwargs)

        if kw:
            cnf = _cnfmerge((cnf, kw))
        else:
            cnf = _cnfmerge(cnf)

        res = []
        for k, v in cnf.items():
            if v is not None:
                if k[-1] == '_': k = k[:-1]
                if callable(v):
                    v = self.register(v)
                elif isinstance(v, (tuple, list)):
                    nv = []
                    for item in v:
                        if isinstance(item, int):
                            nv.append(str(item))
                        elif isinstance(item, str):
                            nv.append(_stringify(item))
                        else:
                            break
                    else:
                        v = ' '.join(nv)

                res.append('-' + k)
                res.append(v)
        return tuple(res)

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

    @property
    def size(self) -> Tuple[int, int]:
        """ :return: width, height """
        return self.Width, self.Height

    @property
    def Width(self) -> int:
        return self.winfo_width()
    @property
    def Height(self) -> int:
        return self.winfo_height()

    @property
    def X(self) -> int:
        return self.winfo_x()
    @property
    def Y(self) -> int:
        return self.winfo_y()

    def Dimensions(self) -> Tuple[int, int, int, int]:
        """ :return: x, y, width, height """
        return self.X, self.Y, self.Width, self.Height

    def Left(self) -> int:
        """ :return: Left Plane """
        return self.X
    def Right(self) -> int:
        """ :return: Right Plane """
        return self.X + self.Width
    def Top(self) -> int:
        """ :return: Top Plane """
        return self.Y
    def Bottom(self) -> int:
        """ :return: Bottom Plane """
        return self.Y + self.Height

    def TopLeft(self) -> Tuple[int, int]:
        """ :return: (X, Y) """
        return self.X, self.Y
    def TopRight(self) -> Tuple[int, int]:
        """ :return: (X, Y) """
        return self.X + self.Width, self.Y
    def BottomLeft(self) -> Tuple[int, int]:
        """ :return: (X, Y) """
        return self.X, self.Y + self.Height
    def BottomRight(self) -> Tuple[int, int]:
        """ :return: (X, Y) """
        return self.X + self.Width, self.Y + self.Height

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
        """
        Bind to all widgets at an event SEQUENCE a call to function FUNC.
        An additional boolean parameter ADD specifies whether FUNC will be called additionally to the other bound function or whether it will replace the previous function.
        See bind for the return value.
        """
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


SyncCallable = Callable[[Optional[TkinterEvent], Tuple, Dict[str, Any]], Any]
SimpleSyncCallable = Callable[[Optional[TkinterEvent]], Any]
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


AsyncCallable = Callable[[Optional[TkinterEvent], Tuple, Dict[str, Any]], Coroutine]
SimpleAsyncCallable = Callable[[Optional[TkinterEvent]], Coroutine]
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
        if _event is not None:
            _event = TkinterEvent(_event)

        try:
            try:
                result = self._func(_event, self._args, self._kwargs)
            except TypeError:
                result = self._func(_event)

            if iscoroutine(result) or iscoroutinefunction(result):
                if self._loop is None: raise RuntimeError(f'_loop is None for method "{nameof(self._func)}"')
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


# _TUpdater = TypeVar('_TUpdater', Updater, AsyncUpdater)
cpdef class BaseApp(object):
    """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
    __slots__ = ['NAME']
    cpdef str * NAME
    cpdef tkRoot * root


    def __init__(self, app_name: str, root: tkRoot):
        self.NAME = app_name
        self.root = root
        self.root.SetTitle(app_name)
        self.root.protocol('WM_DELETE_WINDOW', self.Close)
        self.root.Bind(Bindings.ButtonPress, self.Handle_Press)
        self.root.Bind(Bindings.Key, self.Handle_KeyPress)
    def __cinit__(self, str app_name, tkRoot root):
        self.NAME = app_name
        self.root = root
        self.root.SetTitle(app_name)
        self.root.protocol('WM_DELETE_WINDOW', self.Close)
        self.root.Bind(Bindings.ButtonPress, self.Handle_Press)
        self.root.Bind(Bindings.Key, self.Handle_KeyPress)


    # def CreateLogger(self, source, *, debug: bool = __debug__) -> Logger:
    #     return self._logging_manager.CreateLogger(source, debug=debug)
    #
    # def GetLogger(self, source: Union[Type, Any]) -> Logger:
    #     return self.logger.getChild(typeof(source).__name__)


    def Close(self):
        """ Override to add functionality. Closes updater loop then closes application. """
        self.root.quit()
    def start_gui(self, *_args, **_kwargs): raise NotImplementedError()


    def Handle_Press(self, event: TkinterEvent) -> Optional[bool]:
        raise NotImplementedError()
    def Handle_KeyPress(self, event: TkinterEvent) -> Optional[bool]:
        raise NotImplementedError()



# class BaseAsyncApp(BaseApp[AsyncUpdater], ABC):
#     """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
#     __slots__ = ['_updater']
#     def __init__(self, app_name: str,
#                  *types: Type,
#                  width: Optional[int] = None,
#                  height: Optional[int] = None,
#                  x: int = 0,
#                  y: int = 0,
#                  fullscreen: Optional[bool] = None,
#                  loop: Type[AbstractEventLoop] = None,
#                  root_path: Union[str, FilePath] = '.',
#                  updater: Type[AsyncUpdater] = None,
#                  **kwargs):
#         if fullscreen is None: fullscreen = not self.DEBUG
#         _updater = (updater or AsyncUpdater)(loop or get_event_loop())
#
#         BaseApp.__init__(self, _updater, app_name, *types, root_path=root_path, width=width, height=height, fullscreen=fullscreen, x=x, y=y, **kwargs)
#
#     @property
#     def loop(self) -> AbstractEventLoop:
#         return self._updater.loop
#
#     def start_gui(self, *_args, **_kwargs):
#         try:
#             self.tk.mainloop()
#         except KeyboardInterrupt:
#             self._updater.stop()
#             return
# class BaseSyncApp(BaseApp[Updater], ABC):
#     """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
#     __slots__ = ['queue']
#     queue: Queue
#     def __init__(self, app_name: str,
#                  *types: Type,
#                  x: int = 0,
#                  y: int = 0,
#                  width: Optional[int] = None,
#                  height: Optional[int] = None,
#                  fullscreen: Optional[bool] = None,
#                  root_path: Union[str, FilePath] = '.',
#                  updater: Type[Updater] = None,
#                  queue: Queue = Queue(),
#                  **kwargs):
#         if fullscreen is None: fullscreen = not self.DEBUG
#         self.queue = queue
#         _updater = (updater or Updater)(self, queue)
#         BaseApp.__init__(self, _updater, app_name, *types, root_path=root_path, width=width, height=height, fullscreen=fullscreen, x=x, y=y, **kwargs)
#
#     def start_gui(self, *_args, **_kwargs):
#         try:
#             self.tk.mainloop()
#         except KeyboardInterrupt:
#             return
#
#
#     # @staticmethod
#     # def InitAsync():
#     #     set_event_loop_policy(AsyncTkinterEventLoopPolicy())


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





class Style(ttk.Style):
    def Configure_Root(self, background: str, foreground: str, selected: str, active: str, font: str):
        self.configure('.', background=background, foreground=foreground, font=font)
        self.map('.', background=[('selected', selected), ('active', active)])

    def Configure_NotebookTab(self, background: str, foreground: str, selected: str, active: str, font: str, padding: Tuple[int, int]):
        self.configure('TNotebook.Tab', background=background, foreground=foreground)
        self.map('TNotebook.Tab', background=[('selected', selected), ('active', active)])
        self.theme_settings(self.CurrentTheme, { "TNotebook.Tab": { "configure": { "padding": padding, 'font': font } } })

    def SetConfig(self, cfg: Dict[Type, Dict[str, Any]]):
        assert (isinstance(cfg, dict))
        for obj, kw in cfg.items(): self.Configure(obj, **kw)
    def Configure(self, obj: Type, **kwargs): return self.configure(obj.__name__, **kwargs)

    @property
    def Themes(self) -> List[str]: return self.theme_names()

    @property
    def CurrentTheme(self): return self.theme_use()
    @CurrentTheme.setter
    def CurrentTheme(self, theme: str): self.theme_use(theme)


class ComboBoxThemed(ttk.Combobox, BaseTextTkinterWidget, CommandMixin):
    """Construct a Ttk Combobox _widget with the master master.

    STANDARD OPTIONS

        class, cursor, style, takefocus

    WIDGET-SPECIFIC OPTIONS

        exportselection
        postcommand

        textvariable

        values

        justify
        state
        Height
        Width
    """
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: Dict[str, str] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        ttk.Combobox.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)

    @property
    def value(self) -> str: return self._txt.get()
    @value.setter
    def value(self, v: str): self._txt.set(v)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ComboboxSelected, self._cmd, add=add)
        return self

    def SetValues(self, values: Union[List[str], Iterable[str]]):
        self.configure(values=values)

    def _options(self, cnf, kwargs=None): return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class ScrollbarThemed(ttk.Scrollbar, BaseTkinterWidget):
    __slots__ = ['_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, orientation: Orient, **kwargs):
        ttk.Scrollbar.__init__(self, master, orient=orientation.value, **kwargs)

    def _options(self, cnf, kwargs=None): return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class ListItem(BaseDictModel[str, Union['ListItem', str]]):
    __slots__ = []
    @property
    def ID(self) -> str:
        return self.get("ID", None)
    @property
    def Name(self) -> str:
        return self.get("Name", None)
    @property
    def Children(self):
        """
        :return:
        :rtype: ItemCollection or None
        """
        return self.get("Children", None)

    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            if "Children" in d:
                if not isinstance(d["Children"], list): raise TypeError(f"""Expecting {list} got type {type(d["Children"])}""")
                d["Children"] = ItemCollection.Parse(d["Children"])

            return ListItem(d)

        raise TypeError(f"""Expecting {dict} got type {type(d)}""")

    @staticmethod
    def Create(ID: str, Name: str, Children: List['ListItem'] = None):
        """
        :param ID: Unique Identifier
        :type ID: str
        :param Name: Display Name
        :type Name: str
        :param Children: Nested ListItems
        :type Children: List[ListItem]
        :return:
        :rtype: ListItem
        """
        return ListItem.Parse(dict(ID=ID, Name=Name, Children=Children))
class ItemCollection(BaseListModel[ListItem]):
    __slots__ = []
    def __init__(self, d: Union[List[ListItem], Iterable[ListItem]]):
        list.__init__(self, d)

    def enumerate(self) -> Iterable[Tuple[int, ListItem]]: return enumerate(self)
    def Iter(self) -> Iterable[int]: return range(len(self))
    def Names(self) -> Iterable[str]: return map(lambda o: getattr(o, 'Name'), self)
    def IDs(self) -> Iterable[str]: return map(lambda o: getattr(o, 'ID'), self)

    @classmethod
    def Parse(cls, d):
        if isinstance(d, list):
            return cls(map(ListItem.Parse, d))

        raise TypeError(f"""Expecting {list} got type {type(d)}""")
class TreeViewThemed(ttk.Treeview, BaseTkinterWidget, CommandMixin):
    """Construct a Ttk Treeview with parent master.

    STANDARD OPTIONS

        class, cursor, style, takefocus, xscrollcommand,
        yscrollcommand

    WIDGET-SPECIFIC OPTIONS

        columns, displaycolumns, Height, padding, selectmode, show

    ITEM OPTIONS

        text, image, values, open, tags

    TAG OPTIONS

        foreground, background, font, image
    """
    __slots__ = ['last_focus', 'focus_tags', 'SelectedItems', 'items', '_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    last_focus: Union[int, str, None]
    focus_tags: List[str]
    SelectedItems: List[Any]
    items: Union[ListItem, ItemCollection, None]

    def __init__(self, master, Color: Dict[str, str] = None, select_mode: SelectionMode = SelectionMode.Extended, loop: Optional[AbstractEventLoop] = None, **kwargs):
        ttk.Treeview.__init__(self, master, selectmode=select_mode.value, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self.items = None
        self.last_focus = None
        self.focus_tags = []
        self.SelectedItems = []
        self.SetCommand(self.OnSelectRow)

        self.foreground = self.CreateForegroundColorTags()
        self.background = self.CreateBackgroundColorTags()
        for color, kw in self.foreground.items(): self.tag_configure(color, **kw)
        for color, kw in self.background.items(): self.tag_configure(color, **kw)

    @staticmethod
    def CreateForegroundColorTags(*colors) -> dict:
        return TreeViewThemed.CreateColorTags(*colors, kw='foreground')
    @staticmethod
    def CreateBackgroundColorTags(*colors) -> dict:
        return TreeViewThemed.CreateColorTags(*colors, kw='background')
    @staticmethod
    def CreateColorTags(*colors, kw: str) -> dict:
        """
            https://stackoverflow.com/questions/48358084/how-to-change-the-foreground-or-background-colour-of-a-selected-cell-in-tkinter/48361639

        :param colors: a list of strings passed as arguments to be converted into tag dictionaries
        :type colors: str
        :param kw: the keyword to change in the tag dictionary
        :type kw: str
        :return: tag dictionary
        :rtype: dict
        """
        if not colors: colors = ("red", "green", "black", "blue", "white", "yellow", "orange", "pink", "grey", "purple", "brown")
        return { f'{kw}_{c}': { kw: c } for c in colors }

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.TreeViewSelect, self._cmd, add=add)
        return self

    def SetTags(self, **tags: Dict[str, Any]):
        for _ in self.SetTagsIter(tags): pass
    def SetTagsIter(self, tags: Dict[str, Dict[str, Any]]) -> Generator[Tuple[str, Union[Dict[str, Any], str]], Dict[str, Dict[str, Any]], None]:
        if tags:
            for tag, kwargs in tags.items():
                yield tag, self.tag_configure(tag, **kwargs)

    def Clear(self):
        self.delete(*self.get_children())

    def SetItems(self, items: Union[ListItem, ItemCollection], *, clear: bool = True, Open: bool = True):
        if clear: self.Clear()
        self.items = items
        self._json_tree(self.items, Open=Open)
    def _json_tree(self, d: Union[ListItem, ItemCollection], *, parent: str = '', Open: bool):
        if not d: return
        if not isinstance(parent, str): raise TypeError(type(parent), (str,))

        if isinstance(d, ListItem):
            self.insert(parent, index=tk.END, iid=d.ID, text=d.Name, open=Open)
            self._json_tree(d.Children, parent=d.ID, Open=Open)

        elif isinstance(d, ItemCollection):
            for item in d:
                if not isinstance(item, ListItem): raise TypeError(type(item), (ListItem,))
                self.insert(parent, index=tk.END, iid=item.ID, text=item.Name, open=Open)
                self._json_tree(item.Children, parent=item.ID, Open=Open)

        else:
            raise TypeError(type(d), (ListItem, ItemCollection))

    def column(self, column, option=None, **kw):
        return super(TreeViewThemed, self).column(column, option, **convert_kwargs(kw))
    def heading(self, column, option=None, **kw):
        return super(TreeViewThemed, self).heading(column, option, **convert_kwargs(kw))

    def selection(self) -> Tuple[str]:
        return super(TreeViewThemed, self).selection()

    # noinspection PyUnusedLocal
    def OnSelect(self, event: tkEvent = None):
        if not isinstance(event, TkinterEvent):
            event = TkinterEvent(event)
        _iid = self.identify_row(event.y)
        if _iid != self.last_focus:
            if self.last_focus:
                self.item(self.last_focus, tags=[])
            self.item(_iid, tags=self.focus_tags)
            self.last_focus = _iid
    # noinspection PyUnusedLocal
    def OnSelectRow(self, event: tkEvent = None):
        for _id in self.selection():
            fg = random.choice(tuple(self.foreground.values()))
            bg = random.choice(tuple(self.background.values()))
            if self.tag_has('sel', _id):
                self.item(_id, tags=[''])
            else:
                self.item(_id, tags=['sel', fg, bg])

        self.SelectedItems = list(self.tag_has('sel'))

    def _options(self, cnf, kwargs=None):
        return self.merge_options(cnf, kwargs)
class TreeViewHolderThemed(Frame):
    """Construct a Ttk Treeview with master scale.

    STANDARD OPTIONS
        class, cursor, style, takefocus, xscrollcommand,
        yscrollcommand

    WIDGET-SPECIFIC OPTIONS
        columns, displaycolumns, Height, padding, selectmode, show

    ITEM OPTIONS
        text, image, values, open, tags

    TAG OPTIONS
        foreground, background, font, image

    --------------------------------------------------------------
    Also creates ttk.scrollbar and the _root_frame that conatins
    both ThemedTreeView and ScrollBar objects
    """
    __slots__ = ['TreeView', 'vsb', 'hsb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    TreeView: TreeViewThemed
    vsb: ScrollbarThemed
    hsb: ScrollbarThemed
    def __init__(self, master, backgroundColor: str, showScrollBars: ShowScrollBars = ShowScrollBars.Always, **kwargs):
        Frame.__init__(self, master, bg=backgroundColor, **kwargs)

        for i in range(1): self.Grid_RowConfigure(i, weight=1)
        for i in range(1): self.Grid_ColumnConfigure(i, weight=1)

        self.TreeView = TreeViewThemed(master=self, **kwargs).Grid(row=0, column=0)

        self.vsb = ScrollbarThemed(master=self, orientation=Orient.Vertical, command=self.TreeView.yview).Grid(row=0, column=1, rowspan=2)
        self.hsb = ScrollbarThemed(master=self, orientation=Orient.Horizonal, command=self.TreeView.xview).Grid(row=1, column=0)

        self.TreeView.configure(yscrollcommand=self.vsb.set)
        self.TreeView.configure(xscrollcommand=self.hsb.set)

        if showScrollBars == ShowScrollBars.Never:
            self.vsb.hide()
            self.hsb.hide()

        elif showScrollBars == ShowScrollBars.Always:
            self.vsb.show()
            self.hsb.show()

    def _options(self, cnf, kwargs=None):
        return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class ButtonThemed(ttk.Button, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a button _widget with the master MASTER.

        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        WIDGET-SPECIFIC OPTIONS

        command, compound, default, Height,
        overrelief, state, Width
    """
    __slots__ = ['_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        cmd = kwargs.pop('Command', None) or kwargs.pop('command', None)
        ttk.Button.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)
        if cmd: self.SetCommand(cmd)

    def _options(self, cnf, kwargs=None): return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class LabelThemed(ttk.Label, BaseTextTkinterWidget, ImageMixin):
    __doc__ = """Construct a label _widget with the master MASTER.

    STANDARD OPTIONS

        activebackground, activeforeground, anchor,
        background, bitmap, borderwidth, cursor,
        disabledforeground, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, image, justify,
        padx, pady, relief, takefocus, text,
        textvariable, underline, wraplength

    WIDGET-SPECIFIC OPTIONS

        Height, state, Width

    """
    __slots__ = ['_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: Dict[str, str] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        ttk.Label.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)
        ImageMixin.__init__(self)

    def _options(self, cnf, kwargs=None): return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class EntryThemed(ttk.Entry, BaseTextTkinterWidget, CommandMixin):
    __doc__ = """Construct an entry _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, Width,
    xscrollcommand.
    """
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: Dict[str, str] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        ttk.Entry.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)

    def Clear(self): self.delete(0, Tags.End.value)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, self._cmd, add=add)
        return self

    @property
    def txt(self) -> str: return self.get()
    @txt.setter
    def txt(self, value: str):
        self.Clear()
        self.insert(Tags.End.value, value)

    def Append(self, value: str):
        self.insert(Tags.End.value, value)

    def _options(self, cnf, kwargs=None): return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class NotebookThemed(BaseTextTkinterWidget, ttk.Notebook):
    __slots__ = ['_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, Color: Dict[str, str] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        ttk.Notebook.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)

    def Add(self, w: BaseTkinterWidget, add: dict = dict(padding=2), *, title: str, **kwargs) -> int:
        """Adds a new tab to the notebook.

        If window is currently managed by the notebook but hidden, it is restored to its previous position."""
        index = self.add(w, **add)
        self.tab(index, text=title, **kwargs)
        return index
    def add(self, child: BaseTkinterWidget, **kw) -> int:
        """Adds a new tab to the notebook.

        If window is currently managed by the notebook but hidden, it is restored to its previous position.

        Returns the index of the child. """
        ttk.Notebook.add(self, child, **kw)
        return self.index_of(child)

    def hide_tab(self, tab_id: Union[int, str]):
        """Hides the tab specified by tab_id.

        The tab will not be displayed, but the associated window remains managed by the notebook and its configuration remembered.
        Hidden tabs may be restored with the add command."""
        return ttk.Notebook.hide(self, tab_id)
    def forget(self, tab_id: Union[int, str]):
        """Removes the tab specified by tab_id, unmaps and unmanages the associated window."""
        return ttk.Notebook.forget(self, tab_id)
    def identify(self, x: int, y: int) -> Union[int, str]:
        """Returns the name of the tab element at position x, y, or the empty string if none."""
        return ttk.Notebook.identify(self, x, y)

    def index_of(self, widget: Union[BaseTkinterWidget, str]) -> int:
        if not isinstance(widget, str):
            _w = str(widget)
        else:
            _w = widget

        for i, w in enumerate(self.tabs()):
            if w == _w: return i

        raise ValueError(f'widget {widget} is not found in the tabs.')
    def index(self, tab_id: Union[int, str]):
        """Returns the numeric index of the tab specified by tab_id, or the total number of tabs if tab_id is the string "end"."""
        return ttk.Notebook.index(self, tab_id)

    def insert(self, pos: int, child: BaseTkinterWidget, **kw):
        """Inserts a pane at the specified position.

        pos is either the string end, an integer index, or the name of a managed child.
        If child is already managed by the notebook, moves it to the specified position."""
        return ttk.Notebook.insert(self, pos, child, **kw)

    def select(self, tab_id: Union[int, str] = None) -> Union[int, str]:
        """Selects the specified tab.

        The associated child window will be displayed, and the previously-selected window (if different) is unmapped.
        If tab_id is omitted, returns the widget name of the currently selected pane."""
        return ttk.Notebook.select(self, tab_id)

    def tab(self, tab_id: Union[int, str], option: str = None, **kw) -> Union[dict, Union[int, str]]:
        """Query or modify the options of the specific tab_id.

        If kw is not given, returns a dict of the tab option values.

        If option is specified, returns the value of that option.

        Otherwise, sets the options to the corresponding values."""
        return ttk.Notebook.tab(self, tab_id, option, **kw)
    def tabs(self) -> List[BaseTkinterWidget]:
        """Returns a list of windows managed by the notebook."""
        return ttk.Notebook.tabs(self)

    def enable_traversal(self):
        """Enable keyboard traversal for a toplevel window containing this notebook.

        This will extend the bindings for the toplevel window containing this notebook as follows:

            Control-Tab: selects the tab following the currently selected one

            Shift-Control-Tab: selects the tab preceding the currently selected one

            Alt-K: where K is the mnemonic (underlined) character of any tab, will select that tab.


        Multiple notebooks in a single toplevel may be enabled for traversal, including nested notebooks.
        However, notebook traversal only works properly if all panes are direct children of the notebook.


        The only, and good, difference I see is about mnemonics, which works after calling this method.
        Control-Tab and Shift-Control-Tab always works (here at least).
        """
        return ttk.Notebook.enable_traversal(self)

    @property
    def ActiveTab(self) -> Union[int, str]:
        return self.select()
    @ActiveTab.setter
    def ActiveTab(self, tab_id: Union[int, str]):
        self.select(tab_id)

    @property
    def txt(self) -> str:
        return self.tab(self.ActiveTab, option='text')
    @txt.setter
    def txt(self, value: str):
        self.tab(self.ActiveTab, text=value)

    @property
    def wrap(self) -> int:
        return self.tab(self.ActiveTab, option='wraplength')
    @wrap.setter
    def wrap(self, value: int):
        assert (isinstance(value, int))
        self.tab(self.ActiveTab, wraplength=self._wrap)

    def _options(self, cnf, kwargs=None):
        return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class SeparatorThemed(ttk.Separator, BaseTkinterWidget):
    __slots__ = ['_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, orientation: Orient = Orient.Horizonal):
        ttk.Separator.__init__(self, master, orient=orientation.value)

    def _options(self, cnf, kwargs=None): return self.merge_options(cnf, kwargs)

# ------------------------------------------------------------------------------------------

class CheckButtonThemed(ttk.Checkbutton, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Ttk Checkbutton widget which is either in on- or off-state.

    Construct a Ttk Checkbutton widget with the parent master.

    STANDARD OPTIONS

        class, compound, cursor, image, state, style, takefocus,
        text, textvariable, underline, Width

    WIDGET-SPECIFIC OPTIONS

        command, offvalue, onvalue, variable
    """
    __slots__ = ['_value', '_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    _value: tk.BooleanVar
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        ttk.Checkbutton.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)
        ImageMixin.__init__(self)
        self._value = tk.BooleanVar(master=self, value=False)
        self.configure(variable=self._value)

    @property
    def value(self) -> bool: return self._value.get()
    @value.setter
    def value(self, b: bool):  # FIXME: ignores value passed. only toggles true/false.
        self._value.set(b)

        self.invoke()

    def _options(self, cnf, kwargs=None): return self.merge_options(cnf, kwargs)


# noinspection DuplicatedCode
class Button(tk.Button, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a button _widget with the master MASTER.

        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        WIDGET-SPECIFIC OPTIONS

        command, compound, default, Height,
        overrelief, state, Width
    """
    __slots__ = ['_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 Command: callable = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)
        cmd = kwargs.pop('command', None)
        if cmd: self.SetCommand(cmd)

        if Command: self.SetCommand(Command)

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]:
        return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Label(tk.Label, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    __doc__ = """Construct a label _widget with the master MASTER.

    STANDARD OPTIONS

        activebackground, activeforeground, anchor,
        background, bitmap, borderwidth, cursor,
        disabledforeground, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, image, justify,
        padx, pady, relief, takefocus, text,
        textvariable, underline, wraplength

    WIDGET-SPECIFIC OPTIONS

        Height, state, Width

    """
    __slots__ = ['_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]: return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Message(tk.Message, BaseTextTkinterWidget, CommandMixin):
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 loop: Optional[AbstractEventLoop] = None,
                 Color: Optional[Dict[str, str]] = None,
                 **kwargs):
        tk.Message.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]: return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Entry(tk.Entry, BaseTextTkinterWidget, CommandMixin):
    __doc__ = """Construct an entry _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, Width,
    xscrollcommand.
    """
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)

    def Clear(self):
        self.delete(0, Tags.End.value)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress.value, self._cmd, add=add)
        return self

    # @property
    # def txt(self) -> str: return self.get()
    # @txt.setter
    # def txt(self, value: str):
    #     self.Clear()
    #     self.insert(0, value)

    def Append(self, value: str):
        self.insert(Tags.End.value, value)

    def __iadd__(self, other: str): self.Append(other)

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]: return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class CheckButton(tk.Checkbutton, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a checkbutton _widget with the master MASTER.

        Valid resource names:

                Width
                Height

                fg
                foreground
                bg
                background
                activebackground
                activeforeground
                highlightbackground
                highlightcolor
                highlightthickness
                disabledforeground
                selectcolor

                selectimage
                bitmap
                image

                indicatoron
                justify
                offvalue
                onvalue
                padx
                pady
                relief

                state
                takefocus

                text
                textvariable
                variable
                font

                command

                bd
                anchor
                cursor
                borderwidth
                underline
                wraplength

    """
    __slots__ = ['_value', '_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    _value: tk.BooleanVar
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Checkbutton.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)
        ImageMixin.__init__(self)
        self._value = tk.BooleanVar(master=self, value=False)
        self.configure(variable=self._value)

    @property
    def value(self) -> bool:
        return self._value.get()
    @value.setter
    def value(self, b: bool):
        self._value.set(b)
        if b:
            self.select()
        else:
            self.deselect()

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]:
        return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Listbox(tk.Listbox, BaseTextTkinterWidget, CommandMixin):
    """Construct a listbox _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, Height, highlightbackground,
    highlightcolor, highlightthickness, relief, selectbackground,
    selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
    Width, xscrollcommand, yscrollcommand, listvariable.

    Allowed WordWrap modes are ('word', 'none', 'char')
    """
    __slots__ = ['_Current_ListBox_Index', '_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    _Current_ListBox_Index: Optional[int]
    def __init__(self, master,
                 *,
                 Command: callable = None,
                 z=None,
                 selectMode: Union[str, SelectionMode] = tk.SINGLE,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Listbox.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self.SetSelectMode(selectMode)
        if Command is not None: self.SetCommand(Command, z=z)
        self._Current_ListBox_Index = None
    def SetSelectMode(self, mode: Union[str, SelectionMode] = tk.SINGLE):
        if isinstance(mode, SelectionMode): mode = mode.value
        self.configure(selectmode=mode)
    def SelectRow(self, index: int = None):
        if index is None: index = self._Current_ListBox_Index
        if index is None: return
        self.activate(index)
        self.selection_clear(0, Tags.End.value)
        self.selection_set(index)
        self._Current_ListBox_Index = index
    def SelectRows(self, *args):
        if args:
            self.selection_clear(0, Tags.End.value)
            for index in args:
                if isinstance(index, int):
                    self.activate(index)
                    self.selection_set(index)
                    self._Current_ListBox_Index = index
    def Current_Index(self, event: TkinterEvent = None) -> Optional[int]:
        """ :return: int or None """
        try:
            selections = self.curselection()
            if selections != ():
                return selections[0]
            elif self._Current_ListBox_Index is not None:
                return self._Current_ListBox_Index
            else:
                return self.nearest(event.y)
        except (IndexError, AttributeError):
            return None

    def Clear(self):
        """ delete all lines from the listbox. """
        self.delete(0, Tags.End.value)
    def DeleteAtIndex(self, index: int = None):
        """        delete a selected line from the listbox.        """
        if index is None: index = self.Current_Index()  # get selected line index
        if index is None: return
        self.delete(index)
    def ReplaceAtIndex(self, index: int, value: int or float or str):
        if value is not None:
            self.DeleteAtIndex(index)
            self.insert(index, value)
    def GetAtIndex(self, index: int) -> str:
        return self.get(index)
    def Advance(self, *, forward: bool = True, amount: int = 1, extend: bool = False):
        """
            Advance the row either up or down.

        :param forward: direction to change: True moves down, False moves up.
        :type forward: bool
        :param amount: offset to change the line focus index
        :type amount: int
        :param extend: if forward is True, and extend is True, append new row on advance
        :type extend: bool
        :return:
        :rtype:
        """
        i = self.Index
        if forward:
            i += amount
        else:
            i -= amount

        if i > self.Count:
            if extend:
                for _ in range(amount): self.Append('')
            else:
                i = self.Count
        elif i < 0:
            i = 0

        self.Index = i

    def SetList(self, temp_list: Iterable):
        """        clear the listbox and set the new items.        """
        self.Clear()
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def AddList(self, temp_list: Iterable):
        """        Append items from the list into the listbox.        """
        for item in temp_list:
            self.Append(item)
    def SortList(self, key: Callable = str.lower):
        """        function to sort listbox items case insensitive by default.        """
        temp_list = self.Items
        temp_list.sort(key=key)
        # delete contents of present listbox
        self.delete(0, Tags.End.value)
        # load listbox with sorted data
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def Append(self, value: str):
        self.insert(Tags.End.value, value)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ListboxSelect, self._cmd, add=add)
        return self
    def ResetColors(self, color: str):
        for i in range(self.Count):
            self.itemconfig(i, background=color)

    @property
    def Items(self) -> list:
        """ returns the current listbox contents """
        return list(self.get(0, Tags.End.value))

    def IsAllValidItems(self) -> bool:
        return all(self.Items)
    def ValidCount(self) -> int:
        count = 0
        for item in self.Items:
            if item: count += 1

        return count

    @property
    def Count(self) -> int:
        return tk.Listbox.size(self)

    @property
    def Index(self) -> int or None:
        return self._Current_ListBox_Index
    @Index.setter
    def Index(self, value: int or None):
        self._Current_ListBox_Index = value
        if value is not None: self.SelectRow(value)

    @property
    def txt(self) -> str:
        return self.GetAtIndex(self._Current_ListBox_Index)
    @txt.setter
    def txt(self, value: str):
        self.ReplaceAtIndex(self._Current_ListBox_Index, value)

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]:
        return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Canvas(tk.Canvas, BaseTkinterWidget):
    __slots__ = ['_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self._setupBindings()

    def DownloadImage(self, url: Union[URL, str], x: int, y: int, *formats: str, width: int = None, height: int = None, **kwargs):
        if isinstance(url, URL) or isinstance(url, str) and url.lower().strip().startswith('http'):
            reply = get(url, **kwargs)
            return self.SetImageFromBytes(reply.content, x, y, *formats, width=width, height=height)

        raise TypeError(typeof(url), (str, URL))
    async def DownloadImageAsync(self, url: Union[URL, str], x: int, y: int, *formats: str, width: int = None, height: int = None, **kwargs):
        if isinstance(url, URL) or isinstance(url, str) and url.lower().strip().startswith('http'):
            async with ClientSession() as session:
                reply: ClientResponse = await session.get(url, **kwargs)
                content = await reply.read()
                return self.SetImageFromBytes(content, x, y, *formats, width=width, height=height)

        raise TypeError(typeof(url), (str, URL))

    def OpenImage(self, path: PathLike, x: int, y: int, *formats: str, width: int = None, height: int = None) -> Tuple[PhotoImage, int]:
        assert (isfile(path))

        with open(path, 'rb') as f:
            img = ImageMixin.open(self, f, width, height, *formats)
            return self.CreateImage(image=img, x=x, y=y)
    async def OpenImageAsync(self, path: PathLike, x: int, y: int, *formats: str, width: int = None, height: int = None) -> Tuple[PhotoImage, int]:
        assert (isfile(path))

        async with async_file_open(path, 'rb') as f:
            _bytes = await f.read()

        with BytesIO(_bytes) as buf:
            img = ImageMixin.open(self, buf, width, height, *formats)
            return self.CreateImage(image=img, x=x, y=y)

    def SetImageFromBytes(self, data: bytes, x: int, y: int, *formats: str, width: int = None, height: int = None) -> Tuple[PhotoImage, int]:
        assert (isinstance(data, bytes))

        with BytesIO(data) as buf:
            img = ImageMixin.open(self, buf, width, height, *formats)
            return self.CreateImage(image=img, x=x, y=y)

    def CreateImage(self, image: Union[Image, tkPhotoImage], x: int, y: int, anchor: Union[str, AnchorAndSticky] = tk.NW) -> Tuple[tkPhotoImage, int]:
        if not isinstance(image, tkPhotoImage): image = tkPhotoImage(image, size=image.size)

        return image, self.create_image(x, y, anchor=anchor, image=image)

    def GetItemPosition(self, _id) -> Optional[Tuple[int, int]]:
        try:
            return self.coords(_id)
        except tk.TclError:
            return None

    def _setupBindings(self):
        self.bind(Bindings.ButtonPress.value, func=self.HandleRelease)
        self.bind(Bindings.ButtonRelease.value, func=self.HandlePress)

        self.bind(Bindings.FocusIn.value, func=self.HandleFocusIn)
        self.bind(Bindings.FocusOut.value, func=self.HandleFocusOut)

    def HandlePress(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandlePress(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass
    def HandleRelease(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleRelease(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass

    def HandleFocusIn(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleFocusIn(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass
    def HandleFocusOut(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleFocusOut(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]:
        return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Scrollbar(tk.Scrollbar, BaseTkinterWidget, CommandMixin):
    """Construct a scrollbar widget with the parent MASTER.

    Valid resource names: activebackground, activerelief,
    background, bd, bg, borderwidth, command, cursor,
    elementborderwidth, highlightbackground,
    highlightcolor, highlightthickness, jump, orient,
    relief, repeatdelay, repeatinterval, takefocus,
    troughcolor, Width."""
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 orientation: Orient,
                 Color: Optional[Dict[str, str]] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Scrollbar.__init__(self, master, orient=orientation.value, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]: return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Text(tk.Text, BaseTextTkinterWidget, CommandMixin):
    class Index(str):
        @classmethod
        def Create(cls, line: int, char: int): return cls(f'{line}.{char}')
        @classmethod
        def End(cls): return cls(tk.END)



    __doc__ = """Construct a text widget with the parent MASTER.

    STANDARD OPTIONS

        background, borderwidth, cursor,
        exportselection, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, insertbackground,
        insertborderwidth, insertofftime,
        insertontime, insertwidth, padx, pady,
        relief, selectbackground,
        selectborderwidth, selectforeground,
        setgrid, takefocus,
        xscrollcommand, yscrollcommand,

    WIDGET-SPECIFIC OPTIONS

        autoseparators, Height, maxundo,
        spacing1, spacing2, spacing3,
        state, tabs, undo, Width, wrap,

    """
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']

    def __init__(self, master,
                 text: str = '',
                 Color: Optional[Dict[str, str]] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Text.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self.txt = text

    def Clear(self): self.delete(self.Index.Create(1, 0), self.Index.End())
    def ClearTags(self): return self.tag_delete(*self.Tags())
    def Tags(self, index: int = None) -> Tuple[str, ...]: return self.tag_names(index)

    def Replace(self, new_text: str, start: Index, end: Index):
        self.delete(start, end)
        return self.insert(start, new_text)

    @property
    def txt(self) -> str: return self.get(self.Index.Create(1, 0), self.Index.End())
    @txt.setter
    def txt(self, value: str): self.insert(self.Index.Create(1, 0), value)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]: return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class ScrolledText(Frame, BaseTextTkinterWidget, CommandMixin):
    tb: Text
    vbar: Scrollbar
    hbar: Scrollbar
    __slots__ = ['tb', 'vbar', 'hbar', '_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, text: str = '', Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **frame_kwargs):
        Frame.__init__(self, master, **frame_kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self.Grid_RowConfigure(0, weight=10)
        self.Grid_RowConfigure(1, weight=1)
        self.Grid_ColumnConfigure(0, weight=10)
        self.Grid_ColumnConfigure(1, weight=1)
        self.tb = Text(master=self).Grid(0, 0)
        self.tb.txt = text

        self.vbar = Scrollbar(self, orientation=Orient.Vertical)
        self.vbar.Grid(0, 1)
        self.vbar.SetCommand(self.tb.yview)
        self.tb.configure(yscrollcommand=self.vbar.set)

        self.hbar = Scrollbar(self, orientation=Orient.Horizonal)
        self.hbar.Grid(1, 0, columnspan=2)
        self.hbar.SetCommand(self.tb.xview)
        self.tb.configure(xscrollcommand=self.hbar.set)

    @property
    def txt(self) -> str: return self.tb.txt
    @txt.setter
    def txt(self, value: str): self.tb.txt = value

    def _setCommand(self, add: bool):
        self.command_cb = self.tb.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]: return self.merge_options(cnf, convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Scale(tk.Scale, BaseTkinterWidget):
    __slots__ = ['_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        tk.Scale.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)

    def _options(self, cnf, kwargs=None) -> Tuple[str, ...]: return self.merge_options(cnf, convert_kwargs(kwargs))
