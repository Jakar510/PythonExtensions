# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from typing import *

from .BaseWidgets import *
from .KeyBoard import *
from .Root import *
from .Widgets import *
from .base import *




__all__ = [
        'TitledEntry', 'TitledKeyboardEntry', 'FramedKeyboardEntry', 'FramedEntry', 'KeyboardEntry'
        ]

class KeyboardEntry(Entry, KeyboardMixin):
    def __init__(self, master, *, root: tkRoot, placement: PlacementSet = PlacementSet(Placement.Auto), keysize: int = None, keycolor: str = None,
                 insertbackground: str = 'red', insertborderwidth: int = 3, insertofftime: int = 500, insertontime: int = 500, insertwidth: int = 3,
                 text: str = '', Override_var: tk.StringVar = None, Color: Dict = None, **kwargs):
        Entry.__init__(self, master, text=text, Override_var=Override_var, Color=Color,
                       insertbackground=insertbackground, insertborderwidth=insertborderwidth, insertofftime=insertofftime, insertontime=insertontime, insertwidth=insertwidth,
                       **kwargs)
        KeyboardMixin.__init__(self, master, root=root, placement=placement, keysize=keysize, keycolor=keycolor)

    def _options(self, cnf, kwargs=None) -> Dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))





class TitledEntry(BaseTitled):
    def __init__(self, master, *, RowPadding: int = 1, factor: int = 3,
                 frame: Dict[str, Any] = { }, title: Union[str, Dict[str, Any]] = { }, cls: Type[Entry] = Entry, **value_kwargs):
        assert (issubclass(cls, Entry))
        BaseTitled.__init__(self, master, cls, RowPadding, factor, frame, title, **value_kwargs)
class TitledKeyboardEntry(BaseTitledKeyboard):
    def __init__(self, master, *, root: tkRoot, RowPadding: int = 1, factor: int = 3,
                 frame: Dict[str, Any] = { }, title: Union[str, Dict[str, Any]] = { }, cls: Type[KeyboardEntry] = KeyboardEntry, **value_kwargs):
        assert (issubclass(cls, KeyboardEntry))
        BaseTitledKeyboard.__init__(self, master, cls, root, RowPadding, factor, frame, title, **value_kwargs)





class FramedEntry(BaseFramed):
    def __init__(self, master, *, value: Dict = { }, cls: Type[Entry] = Entry, **value_kwargs):
        assert (issubclass(cls, Entry))
        BaseFramed.__init__(self, master, cls, value, **value_kwargs)
class FramedKeyboardEntry(BaseFramedKeyboard):
    def __init__(self, master, *, root: tkRoot, title: Union[str, Dict[str, Any]] = { }, cls: Type[KeyboardEntry] = KeyboardEntry, **value_kwargs):
        assert (issubclass(cls, KeyboardEntry))
        BaseFramedKeyboard.__init__(self, master, cls, root, title, **value_kwargs)
