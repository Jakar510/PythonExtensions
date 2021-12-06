# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import string
from enum import IntEnum, IntFlag
from typing import *

from ..Base import *
from ..Enumerations import EventType
from ..Events import *
from ..Roots import *
from ..Widgets import *
from ... import AssertType
from ...HID_BUFFER import HID_BUFFER
from ...Names import nameof




__all__ = [
    'KeyboardMixin', 'KeyBoardState',
    'PopupKeyboard', 'Placement', 'PlacementSet',
    'value_title_mixin', 'BaseFramed', 'BaseFramedKeyboard', 'BaseTitled', 'BaseTitledKeyboard',
    ]

class KeyBoardState(IntEnum):
    Idle = 0
    Virtual = 1
    Typing = 2

class Placement(IntFlag):
    Auto = 0x100000

    Top = 0x010000
    Bottom = 0x001000

    Left = 0x000001
    Right = 0x000010
    Center = 0x000100

class PlacementSet(object):
    """ https://blog.magnussen.casa/post/using-enum-as-bitmasks-in-python/ """
    def __init__(self, *flags: Placement):
        self._state = Placement(0)  # Initiate no permissions
        for _flag in flags: self._state |= _flag

    def __contains__(self, o: Placement) -> bool: return (self._state & o) == o

    def __repr__(self): return repr(self._state)

# ------------------------------------------------------------------------------------------

class PopupKeyboard(tkTopLevel):
    """
    A Toplevel instance that displays a keyboard that is attached to another widget.
    Only the Entry widget has a subclass in this version.
    https://www.alt-codes.net/arrow_alt_codes.php
    """
    __slots__ = ['_attach', '_key_color', '_root_frame', '_x', '_y', '__root']
    _space = '[ space ]'
    _shift = 'Aa'
    _next = '>>>' or '→'  # &#x2192
    _previous = '<<<' or '←'  # &#x2190
    _enter = '↲'  # &#x21B2
    _backspace = '<-'
    _delete = 'Clr'
    _sign = '±'

    _key_size: int = -1
    _is_number: bool = False
    _root_frame: Frame
    _Frames: Dict[int, Frame] = { }
    _letters: Dict[int, Dict[int, Button]] = { }
    _numbers: Dict[int, Dict[int, Button]] = { }
    _hid = HID_BUFFER()
    _attach: Union['KeyboardMixin', BaseTextTkinterWidget]
    def __init__(self, root: tkRoot, *, attach,
                 x: int, y: int,
                 key_size: int = -1,
                 key_color: str = 'white',
                 transparency: float = 0.85,
                 take_focus: bool = False,
                 font: str = '-family {Segoe UI Black} -size 13'):
        assert (isinstance(root, tkRoot))
        self.__root = root
        tkTopLevel.__init__(self, master=root, fullscreen=False, takefocus=take_focus, Screen_Width=1, Screen_Height=1)

        self.overrideredirect(True)
        self.SetTransparency(transparency)

        if not isinstance(attach, KeyboardMixin) and isinstance(attach, BaseTextTkinterWidget): raise TypeError(type(attach), (KeyboardMixin, BaseTextTkinterWidget))
        self._attach = attach

        self._key_color = key_color

        self._x = x
        self._y = y

        self._root_frame = Frame(self).Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)

        if self._attach.IsAutoSize: self._SetDimensions()

        Row0: List[str] = [self._backspace] + [str(i) for i in range(10)] + [self._delete]
        Row1: List[str] = ['|', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '/']
        Row2: List[str] = [self._shift, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', '^']
        Row3: List[str] = ['', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', self._enter]
        Row4: List[str] = ['@', '#', '!', '*', self._space, '-', '_', '+', '=']

        offset = 0
        for r, row in enumerate([Row0, Row1, Row2, Row3, Row4]):
            if r not in self._letters: self._letters[r] = { }
            self._root_frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                self._root_frame.Grid_ColumnConfigure(c, weight=1)

                if text == '': continue
                w = Button(master=self._root_frame, text=text, bg=self._key_color, takefocus=take_focus).SetCommand(CurrentValue(self._handle_key_press))

                if self._shift == text:
                    w.Grid(row=r, column=c, rowspan=2)

                elif 'space' in text:
                    w.Grid(row=r, column=c, columnspan=3)
                    offset = 2

                elif self._enter == text:
                    w.Grid(row=r, column=c, rowspan=2)

                else:
                    w.Grid(row=r, column=c + offset)

                self._letters[r][c] = w

        if key_size > 0: self.SetSize(key_size)
        if font: self.SetFont(font)

        self.Bind(Bindings.Key, lambda e: self._attach.destroy_popup())  # destroy _PopupKeyboard on keyboard interrupt



    def SwitchCase(self):
        for row in self._letters.values():
            for w in row.values():
                if w.txt not in string.ascii_letters: continue
                if w.txt in string.ascii_uppercase:
                    w.txt = w.txt.lower()
                else:
                    w.txt = w.txt.upper()

        return self._resize()
    # noinspection DuplicatedCode
    def SetSize(self, size: int):
        self._key_size = size

        for row in self._letters.values():
            for w in row.values():
                w.configure(width=size)

        for row in self._numbers.values():
            for w in row.values():
                w.configure(width=size)

        return self._resize()
    # noinspection DuplicatedCode
    def SetFont(self, font: str):
        for row in self._letters.values():
            for w in row.values(): w.configure(font=font)

        for row in self._numbers.values():
            for w in row.values(): w.configure(font=font)

        return self._resize()


    def _resize(self):
        """ resize to fit keys """
        self.update_idletasks()
        self.update()

        self._SetDimensions()
        return self
    def _SetDimensions(self):
        frame_width: int = self.frame_width
        frame_height: int = self.frame_height
        y = self._get_y(y=self._y, frame_height=frame_height, entry_height=self._attach.Height, placement=self._attach.placement)
        x = self._get_x(x=self._x, frame_width=frame_width, entry_width=self._attach.Width, placement=self._attach.placement)
        self.SetDimensions(frame_width, frame_height, x, y)
    def _get_x(self, *, x: int, frame_width: int, entry_width: int, placement: PlacementSet):
        def left():
            return int(x - frame_width + entry_width)
        def right():
            return int(x)
        def center():
            return int((x + (entry_width / 2)) - (frame_width / 2))
        def middle():
            return int((self.__root.width - frame_width) / 2 + self.__root.x)

        if Placement.Auto in placement:
            root_x = self.__root.x
            root_width = self.__root.width
            x_plus_frame_width = x + frame_width
            x_minus_frame_width = x - frame_width
            if x_minus_frame_width < root_x:
                return middle()

            if x_plus_frame_width > root_width:
                return middle()

            if x_plus_frame_width < root_width and x_minus_frame_width > root_x:
                return center()

            return center()

        if Placement.Center in placement: return center()
        if Placement.Left in placement: return left()
        if Placement.Right in placement: return right()

        raise ValueError(f'placement is unknown. {placement}')
    def _get_y(self, *, y: int, frame_height: int, entry_height: int, placement: PlacementSet):
        def above():
            return y - frame_height
        def below():
            return y + entry_height

        if Placement.Top in placement:
            return above()
        elif Placement.Bottom in placement:
            return below()
        elif Placement.Auto in placement:
            if above() < self.__root.height: return below()
            if below() > self.__root.y: return above()

            return below()

        raise ValueError(f'self.entry.position is unknown. {placement}')


    @property
    def frame_width(self) -> int:
        if self._attach.IsFixedSize: return self._attach.popup_width
        if self._attach.IsRelativeSize: return self._attach.popup_relwidth
        return self._root_frame.Width
    @property
    def frame_height(self) -> int:
        if self._attach.IsFixedSize: return self._attach.popup_height
        if self._attach.IsRelativeSize: return self._attach.popup_relheight
        return self._root_frame.Height



    def _handle_key_press(self, _event: Optional[tkEvent], value: str, *_args, **_kwargs):
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
        if isinstance(self._attach, KeyboardMixin):
            self._attach.destroy_popup()
            return True

        raise AttributeError('self.attach.destroy_popup() not found')

class KeyboardMixin:
    """
    Popup Keyboard is a module to be used with Python's Tkinter library
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
    kb: Optional[PopupKeyboard]
    tk_focusNext: callable
    tk_focusPrev: callable
    Append: callable
    insert: callable
    state: KeyBoardState

    width: int
    height: int

    x: int
    y: int

    _popup_width: Optional[int]
    _popup_height: Optional[int]
    _popup_relwidth: Optional[float]
    _popup_relheight: Optional[float]
    # noinspection SpellCheckingInspection
    def __init__(self, master, *, root: tkRoot, keysize: int = None, keycolor: str = None,
                 placement: PlacementSet = PlacementSet(Placement.Auto),
                 popup_width: int = None, popup_height: int = None,
                 popup_relwidth: float = None, popup_relheight: float = None):
        if not isinstance(self, BaseTextTkinterWidget) and isinstance(self, KeyboardMixin):
            raise TypeError(f'{nameof(self)} must be used on a sub-class of {BaseTextTkinterWidget}')

        self.master = master

        assert (isinstance(root, tkRoot))
        self.__root = root

        self.placement = placement

        self.key_size = keysize or -1
        self.key_color = keycolor

        self._popup_width = popup_width
        self._popup_relwidth = popup_relwidth
        self._popup_height = popup_height
        self._popup_relheight = popup_relheight

        self.state = KeyBoardState.Idle

        assert (isinstance(self, BaseTkinterWidget) and isinstance(self, KeyboardMixin))

        BaseTkinterWidget.Bind(self, Bindings.FocusIn, self._handle_FocusIn)
        BaseTkinterWidget.Bind(self, Bindings.FocusOut, self._handle_FocusOut)
        BaseTkinterWidget.Bind(self, Bindings.Key, self._handle_KeyPress)
        BaseTkinterWidget.Bind(self, Bindings.ButtonPress, self._handle_ButtonPress)


    def _handle_FocusIn(self, _event: tkEvent):
        # self._debug_event_(EventType.FocusIn, e)
        if self.state == KeyBoardState.Idle:
            self._call_popup()
            self.state = KeyBoardState.Virtual
    def _handle_FocusOut(self, _event: tkEvent):
        # self._debug_event_(EventType.FocusOut, e)
        if self.state == KeyBoardState.Typing:
            self.state = KeyBoardState.Idle

        elif self.state == KeyBoardState.Virtual:
            self.state = KeyBoardState.Typing
            self.destroy_popup()
    def _handle_KeyPress(self, _event: tkEvent):
        # self._debug_event_(EventType.KeyPress, e)
        if self.state == KeyBoardState.Virtual:
            self.destroy_popup()
            self.state = KeyBoardState.Typing
    def _handle_ButtonPress(self, _event: tkEvent):
        # self._debug_event_(EventType.ButtonPress, e)
        if self.state != KeyBoardState.Virtual or self.kb is None:
            self._call_popup()
            self.state = KeyBoardState.Virtual
    def _debug_event_(self, tag: EventType, event: tkEvent):
        print('__KeyboardMixin__state__', self.state)
        print(f'__KeyboardMixin__Event__{tag.name}__', str(TkinterEvent(event)))
        print()



    def _call_popup(self):
        self.destroy_popup()
        self.kb = PopupKeyboard(self.__root, attach=self, x=self.x, y=self.y, key_size=self.key_size, key_color=self.key_color)

    def destroy_popup(self):
        if self.kb:
            self.kb.destroy()
            self.kb = None


    @property
    def IsFixedSize(self) -> bool:
        return isinstance(self._popup_width, int) and isinstance(self._popup_height, int)
    @property
    def IsRelativeSize(self) -> bool:
        return isinstance(self._popup_relwidth, float) and isinstance(self._popup_relheight, float)
    @property
    def IsAutoSize(self) -> bool:
        return not (self.IsFixedSize or self.IsRelativeSize)


    @property
    def popup_width(self) -> Optional[int]:
        return self._popup_width
    @property
    def popup_height(self) -> Optional[int]:
        return self._popup_height
    @property
    def popup_relwidth(self) -> Optional[int]:
        return int(self.__root.width * self._popup_relwidth) if self._popup_relwidth is not None else None
    @property
    def popup_relheight(self) -> Optional[int]:
        return int(self.__root.height * self._popup_relheight) if self._popup_relheight is not None else None

# ------------------------------------------------------------------------------------------

class value_title_mixin:
    Title: Label
    Entry: BaseTextTkinterWidget

    @property
    def title(self) -> str:
        return self.Title.txt
    @title.setter
    def title(self, value: str):
        self.Title.txt = value

    @property
    def value(self) -> str:
        return self.Entry.txt
    @value.setter
    def value(self, value: str):
        self.Entry.txt = value

    @staticmethod
    def IsKeyBoard(cls):
        return isinstance(cls, BaseTextTkinterWidget) and isinstance(cls, KeyboardMixin)
    @staticmethod
    def IsKeyBoardType(cls: Type):
        return issubclass(cls, BaseTextTkinterWidget) and issubclass(cls, KeyboardMixin)
    @staticmethod
    def AssertKeyBoardType(cls: Type):
        if not value_title_mixin.IsKeyBoardType(cls): raise TypeError(type(cls), (BaseTextTkinterWidget, KeyboardMixin))


    @staticmethod
    def _ConvertTitle(value: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(value, str): return dict(text=value)
        return value

# ------------------------------------------------------------------------------------------

class BaseTitled(Frame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a grid.

        Example:
            class TitledEntry(BaseTitled):
                def __init__(self, master, *, RowPadding: int = 1, factor: int = 3, value: Dict = { }, title: Dict = { }, cls: Type[Entry] = Entry, **kwargs):
                    assert (issubclass(cls, Entry))
                    BaseTitled.__init__(self, master, cls=cls, value=value, RowPadding=RowPadding, title=title, factor=factor, **kwargs)

    """
    @overload
    def __init__(self, master, cls: Type, RowPadding: int, factor: int,
                 frame: Dict[str, Any], title: str, **value_kwargs: Union[Placement, str, int]): ...
    @overload
    def __init__(self, master, cls: Type, RowPadding: int, factor: int,
                 frame: Dict[str, Any], title: Dict[str, Any], **value_kwargs: Union[Placement, str, int]): ...

    def __init__(self, master, cls: Type, RowPadding: int, factor: int,
                 frame: Dict[str, Any], title: Union[str, Dict[str, Any]], **value_kwargs: Union[Placement, str, int]):
        AssertType(cls, value_title_mixin, BaseTextTkinterWidget)
        Frame.__init__(self, master, **frame)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **self._ConvertTitle(title)).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        # noinspection PyArgumentList
        self.Entry = cls(self, **value_kwargs).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)

    # @classmethod
    # def TEST(cls, master, root: tkRoot, d: Dict[str, Dict[str, Union[PlacePosition, str, int]]], frame_bg: str = 'light blue'):
    #     frame: KeyBaordTestFrame[cls] = KeyBaordTestFrame(master, background=frame_bg)
    #     for key, value in d.items():
    #         w = cls(frame, title=key, **value).PackHorizontal()
    #         setattr(frame, key, w)
    #
    #     return frame
class BaseTitledKeyboard(Frame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a grid.

        Example:
            class TitledKeyboardEntry(BaseTitledKeyboard):
                def __init__(self, master, *, root: tkRoot, RowPadding: int = 1, factor: int = 3, value: Dict = { }, title: Dict = { }, cls: Type[KeyboardEntry] =
                KeyboardEntry, **kwargs):
                    assert (issubclass(cls, KeyboardEntry))
                    BaseTitledKeyboard.__init__(self, master, cls=cls, root=root, value=value, RowPadding=RowPadding, title=title, factor=factor, **kwargs)

    """
    @overload
    def __init__(self, master, cls: Type, root: tkRoot, RowPadding: int, factor: int,
                 title: str, value: Dict, **value_kwargs: Union[Placement, str, int]): ...
    @overload
    def __init__(self, master, cls: Type, root: tkRoot, RowPadding: int, factor: int,
                 title: Dict[str, Any], value: Dict, **value_kwargs: Union[Placement, str, int]): ...

    def __init__(self, master, cls: Type, root: tkRoot, RowPadding: int, factor: int,
                 frame: Dict[str, Any], title: Union[str, Dict[str, Any]], **value_kwargs: Union[Placement, str, int]):
        value_title_mixin.AssertKeyBoardType(cls)
        Frame.__init__(self, master, **frame)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **self._ConvertTitle(title)).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Entry = cls(self, root=root, **value_kwargs).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)

    # @classmethod
    # def TEST(cls, master, root: tkRoot, d: Dict[str, Dict[str, Union[PlacePosition, str, int]]], frame_bg: str = 'light blue'):
    #     frame: KeyBaordTestFrame[cls] = KeyBaordTestFrame(master, background=frame_bg)
    #     for key, value in d.items():
    #         w = cls(frame, root=root, title=key, **value).PackHorizontal()
    #         setattr(frame, key, w)
    #
    #     return frame

# ------------------------------------------------------------------------------------------

class BaseFramed(LabelFrame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a LabelFrame.

        Example:
            class FramedEntry(BaseFramed):
                def __init__(self, master, *, value: Dict = { }, cls: Type[Entry] = Entry, **kwargs):
                    assert (issubclass(cls, Entry))
                    BaseFramed.__init__(self, master, cls=cls, value=value, **kwargs)

    """
    @overload
    def __init__(self, master, cls: Type, title: str, **value_kwargs: Union[Placement, str, int]): ...
    @overload
    def __init__(self, master, cls: Type, title: Dict[str, Any], **value_kwargs: Union[Placement, str, int]): ...

    def __init__(self, master, cls: Type, title: Union[str, Dict[str, Any]], **value_kwargs: Union[Placement, str, int]):
        AssertType(cls, value_title_mixin, BaseTextTkinterWidget)
        LabelFrame.__init__(self, master, **self._ConvertTitle(title))

        # noinspection PyArgumentList
        self.Entry = cls(self, **value_kwargs).PlaceFull()

    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

    # @classmethod
    # def TEST(cls, master, root: tkRoot, d: Dict[str, Dict[str, Union[PlacePosition, str, int]]], frame_bg: str = 'light blue'):
    #     frame: KeyBaordTestFrame[cls] = KeyBaordTestFrame(master, background=frame_bg)
    #     for key, value in d.items():
    #         w = cls(frame, title=key, **value).PackHorizontal()
    #         setattr(frame, key, w)
    #
    #     return frame
class BaseFramedKeyboard(LabelFrame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a LabelFrame.

        Example:
            class FramedKeyboardEntry(BaseFramedKeyboard):
                def __init__(self, master, *, root: tkRoot, value: Dict = { }, cls: Type[KeyboardEntry] = KeyboardEntry, **kwargs):
                    assert (issubclass(cls, KeyboardEntry))
                    BaseFramedKeyboard.__init__(self, master, cls=cls, root=root, value=value, **kwargs)

    """
    @overload
    def __init__(self, master, cls: Type, root: tkRoot, title: str, **value_kwargs: Union[Placement, str, int]): ...
    @overload
    def __init__(self, master, cls: Type, root: tkRoot, title: Dict[str, Any], **value_kwargs: Union[Placement, str, int]): ...

    def __init__(self, master, cls: Type, root: tkRoot, title: Union[str, Dict[str, Any]], **value_kwargs: Union[Placement, str, int]):
        value_title_mixin.AssertKeyBoardType(cls)
        LabelFrame.__init__(self, master, **self._ConvertTitle(title))

        self.Entry = cls(self, root=root, **value_kwargs).PlaceFull()

    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

    # @classmethod
    # def TEST(cls, master, root: tkRoot, d: Dict[str, Dict[str, Union[PlacePosition, str, int]]], frame_bg: str = 'light blue'):
    #     frame: KeyBaordTestFrame[cls] = KeyBaordTestFrame(master, background=frame_bg)
    #     for key, value in d.items():
    #         w = cls(frame, root=root, title=key, **value).PackHorizontal()
    #         setattr(frame, key, w)
    #
    #     return frame
