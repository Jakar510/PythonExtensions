from enum import Enum




__all__ = ['Bindings']

class Bindings(Enum):
    """ https://www.tcl.tk/man/tcl8.6/TkCmd/event.htm """
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


    @staticmethod
    def IsUnknown(keysym) -> bool:
        """
        :param keysym:
        :type keysym: Bindings or str
        :return:
        :rtype: bool
        """
        if isinstance(keysym, str): return keysym == Bindings.UNKNOWN.value

        return keysym == Bindings.UNKNOWN

    @staticmethod
    def IsDigit(keysym: int or str) -> bool:
        """
        :param keysym:
        :type keysym: int or str or Bindings
        :return:
        :rtype: bool
        """
        if isinstance(keysym, Bindings): keysym = keysym.value

        return keysym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'period', 'comma', ',', '.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    @staticmethod
    def IsEnter(keysym) -> bool:
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
    def FromEvent(event):
        """
        :param event: associated event
        :type event: TkinterEvent
        :return: resulting Binding match
        :rtype: Bindings
        """
        assert (isinstance(event, TkinterEvent))
        if Bindings.IsUnknown(event.keysym) and event.num != Bindings.UNKNOWN.value:
            return Bindings.FromKeysym(f'{event.EventType.name}{event.num}')

        return Bindings.FromKeysym(event.keysym)
