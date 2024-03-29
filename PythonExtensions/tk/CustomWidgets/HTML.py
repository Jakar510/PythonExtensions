"""
tkinter HTML text widgets
"""

import sys
from typing import *

import tk_html_widgets as tk_html

from ..Enumerations import ViewState
from ..Events import Bindings, tkEvent
from ..Widgets import ScrolledText




__all__ = [
    'HTMLScrolledText', 'HTMLText', 'HTMLLabel'
    ]

class HTMLScrolledText(ScrolledText):
    __doc__ = tk_html.HTMLScrolledText.__doc__
    _bindIDs: Set[str]
    __slots__ = ['_bindIDs', '_html_parser']
    def __init__(self, html: str = None, **frame_kwargs):
        super().__init__(**frame_kwargs)
        self._w_init(frame_kwargs)
        self._html_parser = tk_html.html_parser.HTMLTextParser()
        self._bindIDs = set()
        if isinstance(html, str): self.set_html(html)

    def _w_init(self, kwargs: Dict[str, Any]):
        if not 'wrap' in kwargs:
            self.tb.configure(wrap='word')
        if not 'background' in kwargs:
            if sys.platform.startswith('win'):
                self.tb.configure(background='SystemWindow')
            else:
                self.tb.configure(background='white')
    def fit_height(self):
        """ Fit widget Height to wrapped lines """
        for h in range(1, 4):
            self.tb.configure(height=h)
            self.update()
            if self.tb.yview()[1] >= 1:
                break
        else:
            self.tb.configure(height=0.5 + 3 / self.tb.yview()[1])

        return self
    def set_html(self, html, strip: bool = True):
        """ Set HTML widget text. If strip is enabled (default) it ignores spaces and new lines. """
        self.UnbindIDs(self._bindIDs)
        prev_state = ViewState(self.tb['state'])
        self.tb.Enable()
        self.tb.Clear()
        self.tb.ClearTags()
        self._html_parser.w_set_html(self.tb, html, strip=strip)

        self._bindIDs.clear()
        self._setupBindings()
        return self.tb.Enable(state=prev_state)

    def _setupBindings(self):
        self._bindIDs.add(self.tb.Bind(Bindings.ButtonPress, func=self.HandlePress, add=True))
        self._bindIDs.add(self.tb.Bind(Bindings.ButtonRelease, func=self.HandleRelease, add=True))

        self._bindIDs.add(self.tb.Bind(Bindings.FocusIn, func=self.HandleFocusIn, add=True))
        self._bindIDs.add(self.tb.Bind(Bindings.FocusOut, func=self.HandleFocusOut, add=True))

    def HandlePress(self, event: tkEvent): pass
    def HandleRelease(self, event: tkEvent): pass
    def HandleFocusIn(self, event: tkEvent): pass
    def HandleFocusOut(self, event: tkEvent): pass

    @property
    def txt(self) -> str: return self.tb.txt
    @txt.setter
    def txt(self, value: str): self.set_html(value)

# ------------------------------------------------------------------------------------------

class HTMLText(HTMLScrolledText):
    __doc__ = tk_html.HTMLText.__doc__
    """ HTML text widget """
    def _w_init(self, kwargs: Dict[str, Any]):
        super()._w_init(kwargs)
        self.vbar.hide()
        self.hbar.hide()

    def fit_height(self):
        super().fit_height()
        # self.master.update()
        self.vbar.hide()

# ------------------------------------------------------------------------------------------

class HTMLLabel(HTMLText):
    __doc__ = tk_html.HTMLLabel.__doc__
    def _w_init(self, kwargs: Dict[str, Any]):
        super()._w_init(kwargs)
        if not 'background' in kwargs:
            if sys.platform.startswith('win'):
                self.tb.config(background='SystemButtonFace')
            else:
                self.tb.config(background='#d9d9d9')

        if not 'borderwidth' in kwargs:
            self.tb.config(borderwidth=0)

        if not 'padx' in kwargs:
            self.tb.config(padx=3)

    def set_html(self, *args, **kwargs): return super().set_html(*args, **kwargs).Disable()
