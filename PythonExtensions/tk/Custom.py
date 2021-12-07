# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import base64
import platform
import sys
from abc import ABC
from asyncio import AbstractEventLoop
from tkinter.messagebox import *
from typing import *

import tk_html_widgets as tk_html
from PIL.Image import Image, open as img_open
from PIL.ImageTk import PhotoImage

from .Base import *
from .Enumerations import *
from .Enumerations import ViewState
from .Events import Bindings, TkinterEvent
from .Themed import ScrollbarThemed
from .Widgets import *
from .Widgets import ScrolledText




__all__ = [
    'ButtonGrid',
    'AutoScroll',
    'AnimatedGIF',
    'HTMLScrolledText',
    'HTMLText',
    'HTMLLabel',
    'tkMessageBox',
    ]

class ButtonGrid(Frame, ABC):
    __slots__ = ['_buttons']
    _buttons: Dict[int, Button]
    def __init__(self, *, master, rows: int = None, cols: int = None, padx: int = 0, pady: int = 0, **Button_kwargs):
        """
        :param master: parent of this grid
        :type master: Frame, LabelFrame, tkRoot, tkTopLevel
        :param rows: number of rows
        :type rows: int
        :param cols: number of columns
        :type cols: int
        :param kwargs: Button kwargs
        :type kwargs: dict
        :param padx: cell padding in x axis
        :type padx: int
        :param pady: cell padding in y axis
        :type pady: int
        """
        Frame.__init__(self, master)
        self._buttons = { }
        self._rows = rows or len(self.ButtonTitles)
        self._cols = cols or 1

        if len(self.ButtonCommands) != self._Count:
            raise ValueError(f"len(self.ButtonCommands) [ {len(self.ButtonCommands)} ]  does not match Number Of Buttons [ {self._Count} ]")

        if len(self.ButtonTitles) != self._Count:
            raise ValueError(f"len(self.ButtonTitles) [ {len(self.ButtonTitles)} ]  does not match Number Of Buttons [ {self._Count} ]")

        self._MakeGrid(padx, pady, **Button_kwargs)
    def _MakeGrid(self, padx: int, pady: int, **Button_kwargs):
        for r in range(self._rows): self.Grid_RowConfigure(r, weight=1)
        for c in range(self._cols): self.Grid_ColumnConfigure(c, weight=1)

        r = 0
        c = 0
        for i in range(self._Count):
            if c >= self._cols:
                r += 1
                c = 0

            self._buttons[i] = Button(self, text=self.ButtonTitles[i], **Button_kwargs).Grid(row=r, column=c, padx=padx, pady=pady).SetCommand(self.ButtonCommands[i])
            c += 1

    def HideAll(self):
        for w in self._buttons.values(): w.hide()
    def ShowAll(self):
        for w in self._buttons.values(): w.show()

    def UpdateText(self, Titles: Dict[int, str] = None):
        if Titles is None: Titles = self.ButtonTitles
        if len(Titles) != self._Count: raise ValueError("len(Titles) Doesn't Match NumberOfButtons")

        for i, title in Titles.items():
            self._buttons[i].txt = title
    def UpdateCommands(self, commands: Dict[int, callable], kwz: Dict[int, Any] = { }, z: Dict[int, Any] = { }):
        if len(commands) != self._Count: raise ValueError("len(commands) Doesn't Match NumberOfButtons")

        for i, Command in commands.items():
            self._buttons[i].SetCommand(Command, z=z.get(i), **kwz.get(i, { }))

    @property
    def _Count(self) -> int:
        return self._rows * self._cols

    @property
    def ButtonTitles(self) -> Dict[int, str]:
        raise NotImplementedError()
    @property
    def ButtonCommands(self) -> Dict[int, callable]:
        raise NotImplementedError()


# ------------------------------------------------------------------------------------------


class AutoScroll(Frame):
    __doc__ = """ 
    The following code is added to facilitate the Scrolled widgets you specified.

    Configure the scrollbars for a widget. 

    Example: 

        class ScrolledTreeView(AutoScroll, TreeViewThemed):
            __doc__ = "   A standard TreeViewThemed widget with scrollbars that will automatically show/hide as needed.   "
            @AutoScroll.create_container
            def __init__(self, master: FrameTypes, **kw):
                TreeViewThemed.__init__(self, master, **kw)
                AutoScroll.__init__(self, master)  
                ...
            ...
            
            
    # GUI module generated by PAGE version 5.4
    #  in conjunction with Tcl version 8.6
    #    Nov 23, 2020 10:53:16 AM CST  platform: Windows NT
    """
    __slots__ = ['vsb', 'hsb']
    vsb: ScrollbarThemed
    hsb: ScrollbarThemed
    def __init__(self, master: BaseTkinterWidget, Color: Dict[str, str] = None, loop: Optional[AbstractEventLoop] = None):
        Frame.__init__(self, master, Color, loop)

        if hasattr(self, 'xview') and callable(self.xview):
            self.hsb = ScrollbarThemed(master, orientation=Orient.Horizonal, command=self.xview).Grid(column=0, row=1, sticky=AnchorAndSticky.EastWest)
            # noinspection PyArgumentList
            self.configure(xscrollcommand=self._autoscroll(self.hsb))

        if hasattr(self, 'yview') and callable(self.yview):
            self.vsb = ScrollbarThemed(master, orientation=Orient.Vertical, command=self.yview).Grid(column=1, row=0, sticky=AnchorAndSticky.NorthSouth)
            # noinspection PyArgumentList
            self.configure(yscrollcommand=self._autoscroll(self.vsb))

        self.Grid(column=0, row=0, sticky=AnchorAndSticky.All)

        master.Grid_RowConfigure(0, weight=1)
        master.Grid_ColumnConfigure(0, weight=1)

    @staticmethod
    def _autoscroll(bar: ScrollbarThemed):
        """   Hide and show scrollbar as needed.   """
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                bar.hide()
            else:
                bar.show()

            bar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


    @staticmethod
    def create_container(func: Callable[[BaseTkinterWidget, Frame, Dict[str, Any]], Frame]):
        """   Creates a tk Frame with a given master, and use this new frame to place the scrollbars and the widget.   """
        def wrapped(cls: BaseTkinterWidget, master: BaseTkinterWidget, **kw):
            container = Frame(master)
            container.Bind(Bindings.Enter, lambda e: AutoScroll._bound_to_mousewheel(TkinterEvent(e), container))
            container.Bind(Bindings.Leave, lambda e: AutoScroll._unbound_to_mousewheel(TkinterEvent(e), container))
            return func(cls, container, **kw)

        return wrapped

    @classmethod
    def create(cls, func: Callable[['AutoScroll', Dict[str, Any]], Frame]):
        """   Creates a AutoScroll with a given master, and use this new frame to place the scrollbars and the widget.   """
        def wrapped(master: BaseTkinterWidget, **kw):
            container = cls(master)
            container.Bind(Bindings.Enter, lambda e: AutoScroll._bound_to_mousewheel(TkinterEvent(e), container))
            container.Bind(Bindings.Leave, lambda e: AutoScroll._unbound_to_mousewheel(TkinterEvent(e), container))
            return func(container, **kw)

        return wrapped


    # noinspection PyUnusedLocal
    @staticmethod
    def _bound_to_mousewheel(event: TkinterEvent, widget: BaseTkinterWidget):
        child = widget.winfo_children()[0]
        assert (isinstance(child, BaseTkinterWidget))

        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            child.BindAll(Bindings.MouseWheel, lambda e: AutoScroll._on_mousewheel(TkinterEvent(e), child))
            child.BindAll(Bindings.ShiftMouseWheel, lambda e: AutoScroll._on_shift_mouse(TkinterEvent(e), child))
        else:
            child.BindAll(Bindings.ButtonPress4, lambda e: AutoScroll._on_mousewheel(TkinterEvent(e), child))
            child.BindAll(Bindings.ButtonPress5, lambda e: AutoScroll._on_mousewheel(TkinterEvent(e), child))
            child.BindAll(Bindings.ShiftButtonPress4, lambda e: AutoScroll._on_shift_mouse(TkinterEvent(e), child))
            child.BindAll(Bindings.ShiftButtonPress5, lambda e: AutoScroll._on_shift_mouse(TkinterEvent(e), child))

    # noinspection PyUnusedLocal
    @staticmethod
    def _unbound_to_mousewheel(event: TkinterEvent, widget: BaseTkinterWidget):
        assert (isinstance(widget, BaseTkinterWidget))
        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            widget.UnBindAll(Bindings.MouseWheel)
            widget.UnBindAll(Bindings.ShiftMouseWheel)
        else:
            widget.UnBindAll(Bindings.ButtonPress4)
            widget.UnBindAll(Bindings.ButtonPress5)
            widget.UnBindAll(Bindings.ShiftButtonPress4)
            widget.UnBindAll(Bindings.ShiftButtonPress5)

    @staticmethod
    def _on_mousewheel(event: TkinterEvent, widget: tk.Widget):
        if hasattr(widget, 'yview_scroll'):
            if platform.system() == 'Windows':
                widget.yview_scroll(-1 * int(event.delta / 120), 'units')
            elif platform.system() == 'Darwin':
                widget.yview_scroll(-1 * int(event.delta), 'units')
            else:
                if event.num == 4:
                    widget.yview_scroll(-1, 'units')
                elif event.num == 5:
                    widget.yview_scroll(1, 'units')

    @staticmethod
    def _on_shift_mouse(event: TkinterEvent, widget: tk.Widget):
        if hasattr(widget, 'xview_scroll'):
            if platform.system() == 'Windows':
                widget.xview_scroll(-1 * int(event.delta / 120), 'units')
            elif platform.system() == 'Darwin':
                widget.xview_scroll(-1 * int(event.delta), 'units')
            else:
                if event.num == 4:
                    widget.xview_scroll(-1, 'units')
                elif event.num == 5:
                    widget.xview_scroll(1, 'units')


# ------------------------------------------------------------------------------------------


class AnimatedGIF(Label, object):
    """
    Creates an Animated loading screen with a GIF whose animation is started by AnimatedGIF.Pack/Place/Grid/show and stopped by AnimatedGIF.hide.

    Based off of:
        AnimatedGIF - a class to show an animated gif without blocking the tkinter mainloop()
        Copyright (c) 2016 Ole Jakob Skjelten <olesk@pvv.org>
        Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md.md
        https://github.com/olesk75/AnimatedGIF/blob/master/AnimatedGif.py
    """
    _callback_id = None
    _is_running: bool = False
    _forever: bool = False

    _loc: int = 0
    _frames: List[PhotoImage] = []
    def __init__(self, master: tk.Widget, *, root: Union[tk.Tk, tk.Toplevel] = None, path: str, forever=True, defaultDelay: int = 100):
        super().__init__(master)
        self._master = master
        self._forever = forever
        self.Root = root

        with img_open(path) as img:
            assert (isinstance(img, Image))

            try:
                self._delay = img.info['duration']
            except (AttributeError, KeyError):
                self._delay = defaultDelay

            i = 0
            while True:
                try:
                    frame = PhotoImage(image=img.copy().convert(mode='RGBA'), master=self.Root or self)
                    self._frames.append(frame)

                    i += 1
                    img.seek(i)
                except EOFError:
                    break

        self._setFrame()
    def start_animation(self, frame: int = None):
        if self._is_running: return

        if frame is not None:
            self._loc = frame
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True
    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False
    def _setFrame(self):
        self.configure(image=self._frames[self._loc])
    def _animate_GIF(self):
        self._loc += 1
        self._setFrame()

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    @property
    def _last_index(self) -> int:
        return len(self._frames) - 1



    def Pack(self, start_animation: bool = True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Pack(**kwargs)
    def Grid(self, start_animation: bool = True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Grid(**kwargs)
    def Place(self, start_animation: bool = True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Place(**kwargs)

    def show(self, _event: TkinterEvent = None, start_animation: bool = True, **kwargs) -> bool:
        if start_animation: self.start_animation()
        return super().show()
    def hide(self, _event: TkinterEvent = None, new_focus: tk.Widget = None) -> bool:
        self.stop_animation()
        return super().hide(_event, new_focus=new_focus)


    @classmethod
    def FromBase64Data(cls, master, *, root: Union[tk.Tk, tk.Toplevel] = None, data: Union[str, bytes], path: str, forever=True, defaultDelay: int = 100):
        with open(path, 'wb') as fp:
            fp.write(base64.urlsafe_b64decode(data))

        return cls(master, root=root, path=path, forever=forever, defaultDelay=defaultDelay)


# ------------------------------------------------------------------------------------------


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

    def HandlePress(self, event: tkEvent):
        pass
    def HandleRelease(self, event: tkEvent):
        pass
    def HandleFocusIn(self, event: tkEvent):
        pass
    def HandleFocusOut(self, event: tkEvent):
        pass

    @property
    def txt(self) -> str:
        return self.tb.txt
    @txt.setter
    def txt(self, value: str):
        self.set_html(value)

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

    def set_html(self, *args, **kwargs):
        return super().set_html(*args, **kwargs).Disable()


# ------------------------------------------------------------------------------------------


class tkMessageBox(tkTopLevel):
    """
    Not Implemented Yet.

    https://www.tutorialspoint.com/python3/tk_messagebox.htm
    """
    def __init__(self, master: tkRoot, *, width: int = None, height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        tkTopLevel.__init__(self, master, width=width, height=height, x=x, y=y, fullscreen=fullscreen, **kwargs)
        self._frame = Frame(self).PlaceFull()


    @classmethod
    def show_info(cls): showinfo()

    @classmethod
    def show_warning(cls): pass

    @classmethod
    def show_error(cls): pass

    @classmethod
    def ask_question(cls): pass

    @classmethod
    def ask_ok_cancel(cls): pass

    @classmethod
    def ask_yes_no(cls): pass

    @classmethod
    def ask_retry_cancel(cls): pass
