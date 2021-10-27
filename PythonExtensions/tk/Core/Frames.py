from asyncio import BaseEventLoop
from enum import Enum
from typing import *

from ..Base import *
from ...Names import nameof




__all__ = [
    'Frame', 'LabelFrame',
    'FrameThemed', 'LabelFrameThemed',
    ]

class _BaseFrameMixin:
    InstanceID: Optional[Union[str, int, Enum]]
    def __init__(self): self.InstanceID = None

    def SetID(self, InstanceID: Union[str, int, Enum]):
        self.InstanceID = InstanceID
        return self

    @property
    def __name__(self):
        try: base = super().__name__()
        except AttributeError: base = nameof(self)

        if self.InstanceID:
            if isinstance(self.InstanceID, Enum): InstanceID = self.InstanceID.value
            else: InstanceID = self.InstanceID

            return f'{base}_{InstanceID}'.lower()

        return base



# noinspection DuplicatedCode
class Frame(tk.Frame, BaseTkinterWidget, _BaseFrameMixin):
    __doc__ = """Frame widget which may contain other widgets and can have a 3D border."""
    __slots__ = ['InstanceID']
    def __init__(self, master, Color: Optional[Dict[str, str]] = None, loop: Optional[BaseEventLoop] = None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        _BaseFrameMixin.__init__(self)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

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
    def __init__(self, master, text: str = '', Color: Optional[Dict[str, str]] = None, loop: Optional[BaseEventLoop] = None, **kwargs):
        tk.LabelFrame.__init__(self, master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, None, Color, loop, configure=False)
        _BaseFrameMixin.__init__(self)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



# noinspection DuplicatedCode
class FrameThemed(ttk.Frame, BaseTkinterWidget, _BaseFrameMixin):
    __doc__ = """Ttk Frame widget is a container, used to group other widgets together."""
    __slots__ = ['InstanceID']
    def __init__(self, master, Color: Optional[Dict[str, str]] = None, loop: Optional[BaseEventLoop] = None, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        _BaseFrameMixin.__init__(self)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

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
    def __init__(self, master, text: str = '', Color: Optional[Dict[str, str]] = None, loop: Optional[BaseEventLoop] = None, **kwargs):
        ttk.LabelFrame.__init__(self, master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, None, Color, loop, configure=False)
        _BaseFrameMixin.__init__(self)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))
