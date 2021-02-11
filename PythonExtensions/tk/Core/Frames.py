from enum import Enum
from typing import *

from ..Base import *




__all__ = [
    'Frame', 'LabelFrame',
    'FrameThemed', 'LabelFrameThemed',
    ]

class _BaseFrameMixin:
    InstanceID: Union[str, int, Enum] = None

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



class Frame(tk.Frame, BaseTkinterWidget, _BaseFrameMixin):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

class LabelFrame(tk.LabelFrame, BaseTextTkinterWidget, _BaseFrameMixin):
    """Construct a labelframe _widget with the master MASTER.

    STANDARD OPTIONS

        borderwidth, cursor, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, padx, pady, relief,
        takefocus, text

    WIDGET-SPECIFIC OPTIONS

        background, class, colormap, container,
        height, labelanchor, labelwidget,
        visual, width
    """
    def __init__(self, master, text: str = '', Color: Dict[str, str] = None, **kwargs):
        tk.LabelFrame.__init__(self, master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, None, Color, configure=False)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



class FrameThemed(ttk.Frame, BaseTkinterWidget, _BaseFrameMixin):
    def __init__(self, master, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

class LabelFrameThemed(ttk.LabelFrame, BaseTextTkinterWidget, _BaseFrameMixin):
    """Construct a labelframe _widget with the master MASTER.

    STANDARD OPTIONS

        borderwidth, cursor, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, padx, pady, relief,
        takefocus, text

    WIDGET-SPECIFIC OPTIONS

        background, class, colormap, container,
        height, labelanchor, labelwidget,
        visual, width
    """
    def __init__(self, master, text: str = '', Color: Dict[str, str] = None, **kwargs):
        ttk.LabelFrame.__init__(self, master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, None, Color, configure=False)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))
