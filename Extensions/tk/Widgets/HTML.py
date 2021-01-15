"""
tkinter HTML text widgets
"""

import sys

import tk_html_widgets as tk_html
from ..Events import Bindings

from ..Widgets.Widgets import ScrolledText, ViewState, tkEvent




__all__ = [
        'HTMLScrolledText', 'HTMLText', 'HTMLLabel'
        ]

class HTMLScrolledText(ScrolledText):
    _bindIDs = set()
    __doc__ = tk_html.HTMLScrolledText.__doc__
    def __init__(self, *args, html=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._w_init(kwargs)
        self.html_parser = tk_html.html_parser.HTMLTextParser()
        if isinstance(html, str):
            self.set_html(html)

    def _w_init(self, kwargs):
        if not 'wrap' in kwargs.keys():
            self.tb.config(wrap='word')
        if not 'background' in kwargs.keys():
            if sys.platform.startswith('win'):
                self.tb.config(background='SystemWindow')
            else:
                self.tb.config(background='white')
    def fit_height(self):
        """ Fit widget height to wrapped lines """
        for h in range(1, 4):
            self.tb.config(height=h)
            self.root.update()
            if self.tb.yview()[1] >= 1:
                break
        else:
            self.tb.config(height=0.5 + 3 / self.tb.yview()[1])

        return self
    def set_html(self, html, strip=True):
        # ------------------------------------------------------------------------------------------
        """
        Set HTML widget text. If strip is enabled (default) it ignores spaces and new lines.

        """
        for ID in self._bindIDs: self.unbind(ID)
        prev_state = ViewState(self.tb['state'])
        self.tb.Enable()
        self.tb.Clear()
        self.tb.tag_delete(self.tb.tag_names)
        self.html_parser.w_set_html(self.tb, html, strip=strip)

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



class HTMLText(HTMLScrolledText):
    __doc__ = tk_html.HTMLText.__doc__
    """ HTML text widget """
    def _w_init(self, kwargs):
        # ------------------------------------------------------------------------------------------
        super()._w_init(kwargs)
        self.vbar.hide()

    def fit_height(self):
        # ------------------------------------------------------------------------------------------
        super().fit_height()
        # self.master.update()
        self.vbar.hide()


class HTMLLabel(HTMLText):
    __doc__ = tk_html.HTMLLabel.__doc__
    def _w_init(self, kwargs):
        # ------------------------------------------------------------------------------------------
        super()._w_init(kwargs)
        if not 'background' in kwargs.keys():
            if sys.platform.startswith('win'):
                self.tb.config(background='SystemButtonFace')
            else:
                self.tb.config(background='#d9d9d9')

        if not 'borderwidth' in kwargs.keys():
            self.tb.config(borderwidth=0)

        if not 'padx' in kwargs.keys():
            self.tb.config(padx=3)

    def set_html(self, *args, **kwargs): return super().set_html(*args, **kwargs).Disable()
