# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import string
import traceback
from enum import IntEnum
from typing import *

from .Base import *
from .Events import *
from .Themed import *
from .Widgets import *
from ..Core.Debug import PrettyPrint
from ..Core.HID_BUFFER import HID_BUFFER





__all__ = [
    'KeyboardMixin', 'KeyBoardState',
    'PopupOptions', 'PopupKeyboard',
    'KeyboardComboBoxThemed', 'TitledKeyboardComboBoxThemed', 'TitledComboBoxThemed', 'FramedKeyboardComboBoxThemed', 'FramedComboBoxThemed',
    'TitledEntry', 'TitledKeyboardEntry', 'FramedKeyboardEntry', 'FramedEntry', 'KeyboardEntry',
    ]

class KeyBoardState(IntEnum):
    Idle = 0
    Virtual = 1
    Typing = 2


# ------------------------------------------------------------------------------------------


class PopupOptions(dict, Dict[str, Union[float, int, str, bool]]):
    __slots__ = [
        'key_size',
        'key_color',
        'space',
        'shift',
        'next',
        'previous',
        'enter',
        'backspace',
        'delete',
        'sign',
        'transparency',
        'font',
        ]

    @overload
    def __init__(self, relwidth: float, relheight: float,
                 key_size: int = -1,
                 key_color: str = 'white',
                 transparency: float = 0.85,
                 font: str = '-family {Segoe UI Black} -size 13',
                 _space: str = '[ space ]',
                 _shift: str = 'Aa',
                 _next: str = '→',  # &#x2192
                 _previous: str = '←',  # &#x2190
                 _enter: str = '↲',  # &#x21B2
                 _backspace: str = '<-',
                 _delete: str = 'Clr',
                 _sign: str = '±'
                 ):
        ...

    @overload
    def __init__(self, relx: float, rely: float, relwidth: float, relheight: float,
                 key_size: int = -1,
                 key_color: str = 'white',
                 transparency: float = 0.85,
                 font: str = '-family {Segoe UI Black} -size 13',
                 _space: str = '[ space ]',
                 _shift: str = 'Aa',
                 _next: str = '→',  # &#x2192
                 _previous: str = '←',  # &#x2190
                 _enter: str = '↲',  # &#x21B2
                 _backspace: str = '<-',
                 _delete: str = 'Clr',
                 _sign: str = '±'
                 ):
        ...

    @overload
    def __init__(self, width: float, height: float,
                 key_size: int = -1,
                 key_color: str = 'white',
                 transparency: float = 0.85,
                 font: str = '-family {Segoe UI Black} -size 13',
                 _space: str = '[ space ]',
                 _shift: str = 'Aa',
                 _next: str = '→',  # &#x2192
                 _previous: str = '←',  # &#x2190
                 _enter: str = '↲',  # &#x21B2
                 _backspace: str = '<-',
                 _delete: str = 'Clr',
                 _sign: str = '±'
                 ): ...

    @overload
    def __init__(self, x: float, y: float, width: float, height: float,
                 key_size: int = -1,
                 key_color: str = 'white',
                 transparency: float = 0.85,
                 font: str = '-family {Segoe UI Black} -size 13',
                 _space: str = '[ space ]',
                 _shift: str = 'Aa',
                 _next: str = '→',  # &#x2192
                 _previous: str = '←',  # &#x2190
                 _enter: str = '↲',  # &#x21B2
                 _backspace: str = '<-',
                 _delete: str = 'Clr',
                 _sign: str = '±'
                 ): ...

    @overload
    def __init__(self, key_size: int = -1,
                 key_color: str = 'white',
                 transparency: float = 0.85,
                 font: str = '-family {Segoe UI Black} -size 13',
                 _space: str = '[ space ]',
                 _shift: str = 'Aa',
                 _next: str = '→',  # &#x2192
                 _previous: str = '←',  # &#x2190
                 _enter: str = '↲',  # &#x21B2
                 _backspace: str = '<-',
                 _delete: str = 'Clr',
                 _sign: str = '±'
                 ): ...

    def __init__(self, **kwargs):
        self.key_size: Final[int] = int(kwargs.pop('key_size', -1))
        self.key_color: Final[str] = str(kwargs.pop('key_color', 'white'))
        self.transparency: Final[float] = float(kwargs.pop('transparency', 0.85))
        self.font: Final[str] = str(kwargs.pop('font', '-family {Segoe UI Black} -size 13'))
        self.space: Final[str] = str(kwargs.pop('_space', '[ space ]'))
        self.shift: Final[str] = str(kwargs.pop('_shift', 'Aa'))
        self.next: Final[str] = str(kwargs.pop('_next', '→'))
        self.previous: Final[str] = str(kwargs.pop('_previous', '←'))
        self.enter: Final[str] = str(kwargs.pop('_enter', '↲'))
        self.backspace: Final[str] = str(kwargs.pop('_backspace', '<-'))
        self.delete: Final[str] = str(kwargs.pop('_delete', 'Clr'))
        self.sign: Final[str] = str(kwargs.pop('_sign', '±'))

        dict.__init__(self, kwargs)

class PopupKeyboard(tkTopLevel):
    """
    A Toplevel instance that displays a keyboard that is attached to another widget.
    Only the Entry widget has a subclass in this version.
    https://www.alt-codes.net/arrow_alt_codes.php
    """
    __slots__ = ['_attach',
                 '_frame',
                 '_key_color',
                 '__root',
                 '_space',
                 '_shift',
                 '_next',
                 '_previous',
                 '_enter',
                 '_backspace',
                 '_delete',
                 '_sign',
                 '_hid',
                 '_numbers',
                 '_letters',
                 '_Frames',
                 '_key_size',
                 ]

    _key_size: int
    _frame: Frame
    _attach: Union['KeyboardMixin', BaseTextTkinterWidget]
    def __init__(self, root: tkRoot, attach: 'KeyboardMixin', options: PopupOptions = None):
        assert (isinstance(root, tkRoot))
        self.__root = root
        tkTopLevel.__init__(self, master=root, fullscreen=False, takefocus=False)

        self.overrideredirect(True)
        self.SetTransparency(options.transparency)

        if 'relx' in options:
            x = options['relx'] * root.Width
            y = options['rely'] * root.Height
            frame_width = options['relwidth'] * root.Width
            frame_height = options['relheight'] * root.Height

        elif 'x' in options:
            x = options['x']
            y = options['y']
            frame_width = options['width']
            frame_height = options['height']

        else:
            if 'relwidth' in options:
                frame_width = options['relwidth'] * root.Width
            elif 'width' in options:
                frame_width = options['width']
            else:
                frame_width = attach.winfo_width()

            if 'relheight' in options:
                frame_height = options['relheight'] * root.Height
            elif 'height' in options:
                frame_height = options['height']
            else:
                frame_height = attach.winfo_height()

            x = abs(attach.winfo_width() - attach.winfo_x()) / 2 - (frame_width / 2)
            y = attach.winfo_y() + attach.winfo_height()
            if y >= root.Height:
                y = attach.winfo_y() - frame_height

        self.SetDimensions(int(frame_width), int(frame_height), int(x), int(y))

        assert (isinstance(attach, KeyboardMixin) and isinstance(attach, BaseTextTkinterWidget))
        self._hid = HID_BUFFER(attach.txt)
        self._attach = attach
        self._Frames: Dict[int, Frame] = { }
        self._letters: Dict[int, Dict[int, Button]] = { }
        self._numbers: Dict[int, Dict[int, Button]] = { }
        self._key_color: Final[str] = options.key_color
        self._space: Final[str] = options.space
        self._shift: Final[str] = options.shift
        self._next: Final[str] = options.next
        self._previous: Final[str] = options.previous
        self._enter: Final[str] = options.enter
        self._backspace: Final[str] = options.backspace
        self._delete: Final[str] = options.delete
        self._sign: Final[str] = options.sign

        # self.Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        # self._frame = Frame(self).Grid(row=0, column=0)
        self._frame = Frame(self, takefocus=False).PlaceFull()

        Row0: List[str] = [self._backspace] + [str(i) for i in range(10)] + [self._delete]
        Row1: List[str] = ['|', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '/']
        Row2: List[str] = [self._shift, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', '^']
        Row3: List[str] = ['', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', self._enter]
        Row4: List[str] = ['@', '#', '!', '*', self._space, '-', '_', '+', '=']

        offset = 0
        for r, row in enumerate([Row0, Row1, Row2, Row3, Row4]):
            if r not in self._letters: self._letters[r] = { }

            self._frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                self._frame.Grid_ColumnConfigure(c, weight=1)

                if text == '': continue
                w = Button(master=self._frame, text=text, bg=self._key_color, takefocus=False).SetCommand(CurrentValue(self._handle_key_press))

                if self._shift == text:
                    w.Grid(row=r, column=c, rowspan=2)

                elif 'space' in text.lower():
                    w.Grid(row=r, column=c, columnspan=3)
                    offset = 2

                elif self._enter == text:
                    w.Grid(row=r, column=c, rowspan=2)

                else:
                    w.Grid(row=r, column=c + offset)

                self._letters[r][c] = w

        if options.key_size > 0: self.SetSize(options.key_size)
        if options.font: self.SetFont(options.font)

        self.Bind(Bindings.Key, lambda e: self._attach.destroy_popup())  # destroy _PopupKeyboard on keyboard interrupt
        self._updateFocus(self)
        self._update()

    def _updateFocus(self, w: tk.Misc):
        for child in w.winfo_children():
            # noinspection PyArgumentList
            child.configure(takefocus=False)
            self._updateFocus(child)


    def SwitchCase(self):
        for row in self._letters.values():
            for w in row.values():
                if w.txt not in string.ascii_letters: continue
                if w.txt in string.ascii_uppercase:
                    w.txt = w.txt.lower()
                else:
                    w.txt = w.txt.upper()

        return self._update()
    # noinspection DuplicatedCode
    def SetSize(self, size: int):
        self._key_size = size

        for row in self._letters.values():
            for w in row.values():
                w.configure(width=size)

        for row in self._numbers.values():
            for w in row.values():
                w.configure(width=size)

        return self._update()
    # noinspection DuplicatedCode
    def SetFont(self, font: str):
        for row in self._letters.values():
            for w in row.values(): w.configure(font=font)

        for row in self._numbers.values():
            for w in row.values(): w.configure(font=font)

        return self._update()


    def _update(self):
        self.update_idletasks()
        self.update()
        return self



    def _handle_key_press(self, _event: Optional[tkEvent], value: str, *_args, **_kwargs):
        print(_event)
        if value == self._shift:
            self.SwitchCase()

        elif value == self._space:
            self._append_space(self._attach)

        elif value == self._enter:
            self._handle_enter()

        elif value == self._backspace:
            self._handle_backspace()

        elif value == self._delete:
            self._hid.Value = self._attach.txt = ''

        elif self._handle_navigation(value):
            pass

        else:
            self._hid += value
            self._attach.txt = self._hid.Value
    def _append_space(self, w):
        if isinstance(w, BaseTextTkinterWidget):
            self._hid.Value = w.txt
            self._hid += ' '
            w.txt = self._hid.Value
    def _handle_backspace(self):
        if isinstance(self._attach, Entry):
            index = self._attach.index(tk.INSERT)
            del self._hid[index]
            self._attach.txt = self._hid.Value

        else:
            self._hid.Value = self._attach.txt
            self._hid.Backspace()
            self._attach.txt = self._hid.Value

    def _handle_navigation(self, value: str) -> bool:
        if value == self._next or value == self._previous:
            if isinstance(self._attach, Entry):
                index = self._attach.index(tk.INSERT)
                if value == self._next:
                    self._attach.icursor(index + 1)
                    return True

                elif value == self._previous:
                    self._attach.icursor(index - 1)
                    return True

                else:
                    self._attach.insert(index, value)
                    return True

            elif isinstance(self._attach, BaseTextTkinterWidget):
                return self._navigate(value)

        return False
    def _navigate(self, value: str) -> bool:
        if value == self._next:
            self._attach.tk_focusNext().focus_set()
            return self._handle_enter()

        elif value == self._previous:
            self._attach.tk_focusPrev().focus_set()
            return self._handle_enter()
    def _handle_enter(self) -> True:
        self._attach.destroy_popup()
        return True

class KeyboardMixin:
    __doc__ = """
    Popup Keyboard is a module to be used with Python's Tkinter library.
    It subclasses the Entry widget as KeyboardEntry to make a pop-up keyboard appear when the widget gains focus.
    Still early in development.


    An extension/subclass of the Tkinter Entry widget, capable
    of accepting all existing args, plus a _keysize and _key_color option.
    Will pop up an instance of _PopupKeyboard when focus moves into
    the widget

    Usage:
    KeyboardEntry(master, key_size=6, key_color='white').pack()

    Example Class:

        class KeyboardEntry(Entry, KeyboardMixin):
            def __init__(self, master, *,
                         root: tkRoot,
                         placement: PlacementSet = PlacementSet(PlacePosition.Auto),
                         key_size: int = None,
                         key_color: str = None,
                         insertbackground: str = 'red',
                         insertborderwidth: int = 3,
                         insertofftime: int = 1,
                         insertontime: int = 1,
                         insertwidth: int = 3,
                         text: str = '',
                         Override_var: tk.StringVar = None,
                         Color: Dict[str, str] = None, **kwargs):
                Entry.__init__(self, master,
                               text=text,
                               Override_var=Override_var,
                               Color=Color,
                               insertbackground=insertbackground,
                               insertborderwidth=insertborderwidth,
                               insertofftime=insertofftime,
                               insertontime=insertontime,
                               insertwidth=insertwidth,
                               **kwargs)
                KeyboardMixin.__init__(self,
                                       master,
                                       root=root,
                                       placement=placement,
                                       key_size=key_size,
                                       key_color=key_color)

    """

    Width: int
    Height: int
    winfo_width: Callable[[], int]
    winfo_height: Callable[[], int]
    winfo_x: Callable[[], int]
    winfo_y: Callable[[], int]
    focus_get: Callable[[], Optional[tk.Misc]]
    tk_focusNext: Callable
    tk_focusPrev: Callable
    Append: Callable
    insert: Callable

    __options: Final[PopupOptions]
    kb: Optional[PopupKeyboard]
    state: KeyBoardState
    def __init__(self, master, root: tkRoot, options: PopupOptions = None):
        assert (isinstance(self, BaseTextTkinterWidget) and isinstance(self, KeyboardMixin))
        assert (isinstance(root, tkRoot))
        self.__root = root
        self.master = master
        self.__options = options or PopupOptions()
        self.kb: Optional[PopupKeyboard] = None
        self.state = KeyBoardState.Idle

        BaseTkinterWidget.Bind(self, Bindings.FocusIn, self._handle_FocusIn)
        BaseTkinterWidget.Bind(self, Bindings.FocusOut, self._handle_FocusOut)
        BaseTkinterWidget.Bind(self, Bindings.Key, self._handle_KeyPress)
        BaseTkinterWidget.Bind(self, Bindings.ButtonPress, self._handle_ButtonPress)


    def _handle_FocusIn(self, _event: tkEvent):
        if self.state == KeyBoardState.Idle:
            self._call_popup()
            self.state = KeyBoardState.Virtual
    def _handle_FocusOut(self, _event: tkEvent):
        if self.state == KeyBoardState.Typing:
            self.state = KeyBoardState.Idle

        elif self.state == KeyBoardState.Virtual:
            self.state = KeyBoardState.Typing
            if _event.widget is not self:
                self.destroy_popup()
                self.state = KeyBoardState.Idle
    def _handle_KeyPress(self, _event: tkEvent):
        if self.state == KeyBoardState.Virtual:
            self.destroy_popup()
            self.state = KeyBoardState.Typing
    def _handle_ButtonPress(self, _event: tkEvent):
        if self.state != KeyBoardState.Virtual or self.kb is None:
            self._call_popup()
            self.state = KeyBoardState.Virtual


    def _debug_event_(self, _event: tkEvent):
        _event = TkinterEvent(_event)

        PrettyPrint(event=_event.ToDict(),
                    state=self.state,
                    focus_get=self.focus_get())



    def _call_popup(self):
        if self.kb:
            self.kb.destroy()
            self.kb = None

        print()
        focus_get = self.focus_get()
        print(f'BEFORE.{focus_get=}')

        self.kb = PopupKeyboard(self.__root, attach=self, options=self.__options)

        print()
        focus_get = self.focus_get()
        print(f'BEFORE.{focus_get=}')



    def destroy_popup(self):
        focus_get = self.focus_get()
        print()
        print()
        print(f'{focus_get=}')
        print()
        print()
        traceback.print_stack()
        print()
        print()

        if self.kb:
            self.kb.destroy()
            self.kb = None


# ------------------------------------------------------------------------------------------


class KeyboardComboBoxThemed(ComboBoxThemed, KeyboardMixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, root: tkRoot, options: PopupOptions = None, *, text: str = '', Override_var: tk.StringVar = None, Color: Dict = None, **kwargs):
        ComboBoxThemed.__init__(self, master, text=text, Override_var=Override_var, Color=Color, postcommand=self._OnDropDown, **kwargs)
        KeyboardMixin.__init__(self, master, root=root, options=options)
        BaseTkinterWidget.Bind(self, Bindings.ComboboxSelected, self._OnSelect)

    def _OnDropDown(self):
        """ By default, destroys the popup when the dropdown list is expanded. Override to add functionality """
        self.destroy_popup()

    # noinspection PyUnusedLocal
    def _OnSelect(self, event: tkEvent = None):
        """ By default, destroys the popup when an item is selected. Override to add functionality """
        self.destroy_popup()

class KeyboardEntry(Entry, KeyboardMixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    # noinspection SpellCheckingInspection
    def __init__(self, master, root: tkRoot, options: PopupOptions = None, *,
                 insertbackground: str = 'red', insertborderwidth: int = 3, insertofftime: int = 500, insertontime: int = 500, insertwidth: int = 3,
                 text: str = '', Override_var: tk.StringVar = None, Color: Dict = None, **kwargs):
        Entry.__init__(self, master,
                       text=text,
                       Override_var=Override_var,
                       Color=Color,
                       insertbackground=insertbackground,
                       insertborderwidth=insertborderwidth,
                       insertofftime=insertofftime,
                       insertontime=insertontime,
                       insertwidth=insertwidth,
                       **kwargs)
        KeyboardMixin.__init__(self, master, root=root, options=options)


# ------------------------------------------------------------------------------------------


class entry_mixin:
    Value: BaseTextTkinterWidget

    @property
    def value(self) -> str:
        return self.Value.txt
    @value.setter
    def value(self, value: str):
        self.Value.txt = value

    @staticmethod
    def IsKeyBoard(cls):
        return isinstance(cls, BaseTextTkinterWidget) and isinstance(cls, KeyboardMixin)
    @staticmethod
    def IsKeyBoardType(cls: Type):
        return issubclass(cls, BaseTextTkinterWidget) and issubclass(cls, KeyboardMixin)
    @staticmethod
    def AssertKeyBoardType(cls: Type):
        if not entry_mixin.IsKeyBoardType(cls): raise TypeError(type(cls), (BaseTextTkinterWidget, KeyboardMixin))


    @staticmethod
    def _ConvertTitle(value: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(value, str): return dict(text=value)
        return value


# ------------------------------------------------------------------------------------------


class TitledComboBoxThemed(Frame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, *, RowPadding: int = 1, factor: int = 3, **frame):
        Frame.__init__(self, master, **frame)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **frame).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Value = ComboBoxThemed(self).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)




    @property
    def title(self) -> str:
        return self.Title.txt
    @title.setter
    def title(self, value: str):
        self.Title.txt = value

class TitledKeyboardComboBoxThemed(Frame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, root: tkRoot, options: PopupOptions = None, *, RowPadding: int = 1, factor: int = 3, **frame):
        Frame.__init__(self, master, **frame)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Value = KeyboardComboBoxThemed(self, root, options).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)




    @property
    def title(self) -> str:
        return self.Title.txt
    @title.setter
    def title(self, value: str):
        self.Title.txt = value

class FramedComboBoxThemed(LabelFrame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, **frame):
        LabelFrame.__init__(self, master, **frame)
        self.Value = ComboBoxThemed(self).PlaceFull()



    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

class FramedKeyboardComboBoxThemed(LabelFrame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, root: tkRoot, options: PopupOptions = None, **frame):
        LabelFrame.__init__(self, master, **frame)

        self.Value = KeyboardComboBoxThemed(self, root, options).PlaceFull()



    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value


# ------------------------------------------------------------------------------------------


class TitledEntry(Frame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, *, RowPadding: int = 1, factor: int = 3, **frame):
        Frame.__init__(self, master, **frame)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Value = Entry(self).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)




    @property
    def title(self) -> str:
        return self.Title.txt
    @title.setter
    def title(self, value: str):
        self.Title.txt = value

class TitledKeyboardEntry(Frame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, root: tkRoot, options: PopupOptions = None, *, RowPadding: int = 1, factor: int = 3, **frame):
        Frame.__init__(self, master, **frame)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Value = KeyboardEntry(self, root, options).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)




    @property
    def title(self) -> str:
        return self.Title.txt
    @title.setter
    def title(self, value: str):
        self.Title.txt = value

class FramedEntry(LabelFrame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, **frame):
        LabelFrame.__init__(self, master, **frame)
        self.Value = Entry(self).PlaceFull()



    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

class FramedKeyboardEntry(LabelFrame, entry_mixin):
    __slots__ = ['kb',
                 'state',
                 '__options',
                 'master',
                 '__root',
                 'key_size',
                 'key_color']
    def __init__(self, master, root: tkRoot, options: PopupOptions = None, **frame):
        LabelFrame.__init__(self, master, **frame)

        self.Value = KeyboardEntry(self, root, options).PlaceFull()


    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value
