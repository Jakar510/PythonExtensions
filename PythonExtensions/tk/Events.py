# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

import pprint
from enum import Enum
from tkinter import Event as tkEvent, EventType, EventType as tkEventType, Widget
from typing import *

from ..Misc import lazy_property
from ..Names import nameof




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

    """
    __slots__ = ['serial',
                 'num',
                 'Height',
                 'keycode',
                 'state',
                 'time',
                 'Width',
                 'x',
                 'y',
                 'char',
                 'keysym',
                 'keysym_num',
                 'type',
                 'widget',
                 'x_root',
                 'y_root',
                 'delta',
                 'send_event']

    serial: Union[str, int]
    num: Optional[Union[str, int]]
    focus: Optional[Union[int, bool]]
    width: Optional[int]
    height: Optional[int]
    keycode: Optional[Union[str, int]]
    state: int
    time: int
    x: Union[str, float]
    y: Union[str, float]
    x_root: Union[str, float]
    y_root: Union[str, float]
    char: Optional[str]
    keysym: Optional[str]
    type: EventType
    widget: Widget
    delta: Optional[float]

    def __init__(self, source: Optional[tkEvent]):
        super().__init__()
        if source is not None:
            assert (isinstance(source, tkEvent))
            for name, value in source.__dict__.items(): setattr(self, name, value)


    def __str__(self) -> str: return f"""<{nameof(self)} ({repr(self).replace('>', '').replace('<', '')}) Object.
{pprint.pformat(self.ToDict(), indent=4)} >"""


    def ToDict(self) -> Dict[str, Union[int, str, float, Widget, 'Bindings']]:
        return {
            'KeySynonym': self.KeySynonym,
            'IsDigit':    self.IsDigit(self.KeySynonym),
            'IsEnter':    self.IsEnter(),
            'IsValid':    self.IsValid(),
            'serial':     self.serial,
            'num':        self.num,
            'Height':     self.height,
            'keycode':    self.keycode,
            'state':      self.state,
            'time':       self.time,
            'Width':      self.width,
            'x':          self.x,
            'y':          self.y,
            'char':       self.char,
            'keysym':     self.keysym,
            'keysym_num': self.keysym_num,
            'type':       self.type,
            'widget':     self.widget,
            'x_root':     self.x_root,
            'y_root':     self.y_root,
            'delta':      self.delta,
            'send_event': self.send_event
            }

    def __call__(self, keysym: 'Bindings' = None) -> bool:
        if keysym is not None: return self.KeySynonym == keysym

        raise ValueError('Unknown value passed')

    @staticmethod
    def IsDigit(keysym: Union[int, str, 'TkinterEvent']) -> bool:
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
    def KeySynonym(self) -> 'Bindings': return Bindings.FromEvent(self)


    def IsEnter(self) -> bool: return Bindings.IsEnter(self.keysym)


    def IsValid(self): return Bindings.IsKnown(self.keysym)


    @classmethod
    def FromShiftTabEvent(cls, event: tkEvent):
        e = cls(event)
        e.keysym = Bindings.ShiftTab.value
        return e


    @staticmethod
    def Debug(event: tkEvent):
        print('Debug.tkEvent', event)
        event = TkinterEvent(event)
        print('Debug.TkinterEvent')
        print(str(event))
        print(event.KeySynonym)

    def Point(self) -> Optional[Tuple[int, int]]:
        if isinstance(self.x, (float, int)) and isinstance(self.y, (float, int)): return self.x, self.y
        return None



class Bindings(Enum):
    __doc__ = """ https://www.tcl.tk/man/tcl8.6/TkCmd/event.htm """
    __slots__ = []

    @staticmethod
    def IsUnknown(keysym: Union[str, 'Bindings']) -> bool:
        """
        :param keysym:
        :type keysym: Bindings or str
        :return:
        :rtype: bool
        """
        if isinstance(keysym, str): return keysym == Bindings.UNKNOWN.value

        return keysym == Bindings.UNKNOWN

    @staticmethod
    def IsKnown(keysym: Union[str, 'Bindings']) -> bool:
        """
        :param keysym:
        :type keysym: Bindings or str
        :return:
        :rtype: bool
        """
        if isinstance(keysym, str): return keysym != Bindings.UNKNOWN.value

        return keysym != Bindings.UNKNOWN

    @staticmethod
    def IsDigit(keysym: Union[int, str, TkinterEvent]) -> bool:
        """
        :param keysym:
        :type keysym: int or str or Bindings
        :return:
        :rtype: bool
        """
        if isinstance(keysym, TkinterEvent): keysym = keysym.keysym
        if isinstance(keysym, Bindings): keysym = keysym.value

        return keysym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'period', 'comma', ',', '.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    @staticmethod
    def IsEnter(keysym: Union[str, 'Bindings']) -> bool:
        """
        :param keysym:
        :type keysym: Bindings or str
        :return:
        :rtype: bool
        """
        if isinstance(keysym, str): keysym = Bindings.FromKeysym(keysym)

        return keysym == Bindings.EnterKey or keysym == Bindings.KP_Enter or keysym == Bindings.Return

    @staticmethod
    def FromKeysym(keysym: str):
        """
        :param keysym: binding type string
        :type keysym: str
        :return: resulting Binding match
        :rtype: Bindings
        """
        try: return Bindings(keysym)
        except ValueError as e:
            if hasattr(Bindings, keysym): return getattr(Bindings, keysym)
            for name in dir(Bindings):
                if name.lower() == keysym.lower():
                    return getattr(Bindings, name)

            raise ValueError(f'Cannot find matching event: "{keysym}"') from e

    @staticmethod
    def FromEvent(event: TkinterEvent):
        """
        :param event: associated event
        :type event: TkinterEvent
        :return: resulting Binding match
        :rtype: Bindings
        """
        if Bindings.IsKnown(event.keysym) and Bindings.IsKnown(event.num):
            return Bindings.FromKeysym(f'{event.EventType.name}{event.num}')

        return Bindings.FromKeysym(event.keysym)



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
