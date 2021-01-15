# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

import base64
import io
import os
from typing import Tuple, Union
from urllib.request import urlopen

from .BaseWidgets import *
from .Frames import Frame
from ..Events import *
from ..Enumerations import *
from ..Widgets.base import *




__all__ = [
        'Entry', 'Label', 'Button', 'Listbox', 'CheckButton', 'Canvas', 'Text', 'CheckButton', 'ScrolledText', 'Scrollbar', 'Scale',
        ]

TODO = """
--Button
--Canvas
--CheckButton
--Entry
--Frame
--LabelFrame
--Label
--ListBox
--Message
Popupmenu
RadioButton
--Scale
Spinbox
Scrollbar
--text
"""

# noinspection DuplicatedCode
class Button(tk.Button, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a button _widget with the master MASTER.

        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        WIDGET-SPECIFIC OPTIONS

        command, compound, default, height,
        overrelief, state, width
    """
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, Command: callable = None, **kwargs):
        tk.Button.__init__(self, master=master, **kwargs)
        cmd = kwargs.pop('command', None)
        if cmd: self.SetCommand(cmd)

        if Command: self.SetCommand(Command)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




# noinspection DuplicatedCode
class Label(tk.Label, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    __doc__ = """Construct a label _widget with the master MASTER.

    STANDARD OPTIONS

        activebackground, activeforeground, anchor,
        background, bitmap, borderwidth, cursor,
        disabledforeground, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, image, justify,
        padx, pady, relief, takefocus, text,
        textvariable, underline, wraplength

    WIDGET-SPECIFIC OPTIONS

        height, state, width

    """
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        tk.Label.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)



    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))


class Message(tk.Message, BaseTextTkinterWidget, CommandMixin):
    def __init__(self, master, **kwargs):
        tk.Message.__init__(self, master, **kwargs)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))


# noinspection DuplicatedCode
class Entry(tk.Entry, BaseTextTkinterWidget, CommandMixin):
    __doc__ = """Construct an entry _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand.
    """
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        tk.Entry.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    def Clear(self):
        self.delete(0, Tags.End.value)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress.value, self._cmd, add=add)
        return self

    @property
    def txt(self) -> str: return self.get()
    @txt.setter
    def txt(self, value: str):
        self.Clear()
        self.insert(Tags.End.value, value)

    def Append(self, value: str):
        self.insert(Tags.End.value, value)

    def __iadd__(self, other: str): self.Append(other)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




class CheckButton(tk.Checkbutton, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a checkbutton _widget with the master MASTER.

        Valid resource names:

                width
                height

                fg
                foreground
                bg
                background
                activebackground
                activeforeground
                highlightbackground
                highlightcolor
                highlightthickness
                disabledforeground
                selectcolor

                selectimage
                bitmap
                image

                indicatoron
                justify
                offvalue
                onvalue
                padx
                pady
                relief

                state
                takefocus

                text
                textvariable
                variable
                font

                command

                bd
                anchor
                cursor
                borderwidth
                underline
                wraplength

    """
    _value: tk.BooleanVar
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        tk.Checkbutton.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)
        self._value = tk.BooleanVar(master=self, value=False)
        self.configure(variable=self._value)


    @property
    def value(self) -> bool: return self._value.get()
    @value.setter
    def value(self, b: bool):
        self._value.set(b)
        if b:
            self.select()
        else:
            self.deselect()

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



class Listbox(tk.Listbox, BaseTextTkinterWidget, CommandMixin):
    """Construct a listbox _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, height, highlightbackground,
    highlightcolor, highlightthickness, relief, selectbackground,
    selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
    width, xscrollcommand, yscrollcommand, listvariable.

    Allowed WordWrap modes are ('word', 'none', 'char')
    """
    _Current_ListBox_Index: int = None
    def __init__(self, master, *, Command: callable = None, z=None, selectMode: Union[str, SelectionMode] = tk.SINGLE, Color: dict = None, **kwargs):
        tk.Listbox.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text='', Color=Color, configure=False)
        self.SetSelectMode(selectMode)
        if Command is not None: self.SetCommand(Command, z=z)
    def SetSelectMode(self, mode: Union[str, SelectionMode] = tk.SINGLE):
        if isinstance(mode, SelectionMode): mode = mode.value
        self.configure(selectmode=mode)
    def SelectRow(self, index: int = None):
        if index is None: index = self._Current_ListBox_Index
        if index is None: return
        self.activate(index)
        self.selection_clear(0, Tags.End.value)
        self.selection_set(index)
        self._Current_ListBox_Index = index
    def SelectRows(self, *args):
        if args:
            self.selection_clear(0, Tags.End.value)
            for index in args:
                if isinstance(index, int):
                    self.activate(index)
                    self.selection_set(index)
                    self._Current_ListBox_Index = index
    def Current_Index(self, event: TkinterEvent = None) -> int or None:
        """ :return: int or None """
        try:
            selections = self.curselection()
            if selections != ():
                return selections[0]
            elif self._Current_ListBox_Index is not None:
                return self._Current_ListBox_Index
            else:
                return self.nearest(event.y)
        except (IndexError, AttributeError):
            return None

    def Clear(self):
        """ delete all lines from the listbox. """
        self.delete(0, Tags.End.value)
    def DeleteAtIndex(self, index: int = None):
        """        delete a selected line from the listbox.        """
        if index is None: index = self.Current_Index()  # get selected line index
        if index is None: return
        self.delete(index)
    def ReplaceAtIndex(self, index: int, value: int or float or str):
        if value is not None:
            self.DeleteAtIndex(index)
            self.insert(index, value)
    def GetAtIndex(self, index: int) -> str: return self.get(index)
    def Advance(self, *, forward: bool = True, amount: int = 1, extend: bool = False):
        """
            Advance the row either up or down.

        :param forward: direction to change: True moves down, False moves up.
        :type forward: bool
        :param amount: offset to change the line focus index
        :type amount: int
        :param extend: if forward is True, and extend is True, append new row on advance
        :type extend: bool
        :return:
        :rtype:
        """
        i = self.Index
        if forward: i += amount
        else: i -= amount

        if i > self.Count:
            if extend:
                for _ in range(amount): self.Append('')
            else: i = self.Count
        elif i < 0: i = 0

        self.Index = i

    def SetList(self, temp_list: list or tuple):
        """        clear the listbox and set the new items.        """
        self.Clear()
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def AddList(self, temp_list: list or tuple):
        """        Append items from the list into the listbox.        """
        for item in temp_list:
            self.Append(item)
    def SortList(self, key: callable = str.lower):
        """        function to sort listbox items case insensitive by default.        """
        temp_list = self.Items
        temp_list.sort(key=key)
        # delete contents of present listbox
        self.delete(0, Tags.End.value)
        # load listbox with sorted data
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def Append(self, value: str): self.insert(Tags.End.value, value)


    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ListboxSelect, self._cmd, add=add)
        return self
    def ResetColors(self, color: str):
        for i in range(self.size()):
            self.itemconfig(i, background=color)

    @property
    def Items(self) -> list:
        """ returns the current listbox contents """
        return list(self.get(0, Tags.End.value))


    def IsAllValidItems(self) -> bool: return all(self.Items)
    def ValidCount(self) -> int:
        count = 0
        for item in self.Items:
            if item: count += 1

        return count

    @property
    def Count(self) -> int: return self.size()

    @property
    def Index(self) -> int or None: return self._Current_ListBox_Index
    @Index.setter
    def Index(self, value: int or None):
        self._Current_ListBox_Index = value
        if value is not None: self.SelectRow(value)

    @property
    def txt(self) -> str: return self.GetAtIndex(self._Current_ListBox_Index)
    @txt.setter
    def txt(self, value: str): self.ReplaceAtIndex(self._Current_ListBox_Index, value)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




class Canvas(tk.Canvas, BaseTkinterWidget):
    def __init__(self, master, *args, Color: dict = None, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self._setupBindings()
        BaseTkinterWidget.__init__(self, Color)
    def _setupBindings(self):
        self.bind(Bindings.ButtonPress.value, func=self.HandleRelease)
        self.bind(Bindings.ButtonRelease.value, func=self.HandlePress)

        self.bind(Bindings.FocusIn.value, func=self.HandleFocusIn)
        self.bind(Bindings.FocusOut.value, func=self.HandleFocusOut)

    def SetImage(self, x: int, y: int, path: str = None, data: str = None, url: str = None) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        if url: return self.DownloadImage(url, x, y)
        elif data and path: raise KeyError('Cannot use both ImageData and ImageName')
        elif data: return self.SetImageFromBytes(base64.b64decode(data), x, y)
        elif path: return self.OpenImage(path, x=x, y=y)
    def DownloadImage(self, url: str, x: int, y: int): return self.SetImageFromBytes(urlopen(url).read(), x, y)
    def OpenImage(self, path: str, x: int, y: int) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        assert (os.path.isfile(path))
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                return self.CreateImage(image=img, x=x, y=y)
    def SetImageFromBytes(self, data: bytes, x: int, y: int) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        assert (isinstance(data, bytes))
        with io.BytesIO(data) as buf:
            with Image.open(buf) as tempImg:
                return self.CreateImage(image=tempImg, x=x, y=y)
    def CreateImage(self, image: Image.Image, x: int, y: int, anchor: str or AnchorAndSticky = tk.NW) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        img_tk = ImageTk.PhotoImage(image)
        return img_tk, image.size, self.create_image(x, y, anchor=anchor, image=img_tk)



    def HandlePress(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandlePress(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass
    def HandleRelease(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleRelease(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass

    def HandleFocusIn(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleFocusIn(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass
    def HandleFocusOut(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleFocusOut(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))


class Scrollbar(tk.Scrollbar, BaseTkinterWidget, CommandMixin):
    def __init__(self, master, **kwargs):
        tk.Scrollbar.__init__(self, master, **kwargs)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



class Text(tk.Text, BaseTextTkinterWidget, CommandMixin):
    def __init__(self, master, **kwargs):
        tk.Text.__init__(self, master, **kwargs)

    def Clear(self): self.delete(self.GetIndex(1, 0), tk.END)

    @staticmethod
    def GetIndex(line: int, char: int): return f'{line}.{char}'

    @property
    def txt(self) -> str: return self.get(self.GetIndex(1, 0), tk.END)
    @txt.setter
    def txt(self, value: str): self.insert(self.GetIndex(1, 0), value)


    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



class ScrolledText(BaseTextTkinterWidget, CommandMixin):
    tb: Text
    vbar: Scrollbar
    # noinspection PyMissingConstructor
    def __init__(self, master, *, text: str, **kw):
        # super().__init__(text=text)
        self.frame = Frame(master, text=text, **kw)
        self.tb = Text(master=self.frame).Pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vbar = Scrollbar(self.frame)
        self.vbar.Pack(side=tk.RIGHT, fill=Fill.y)
        self.vbar.SetCommand(self.tb.yview)
        self.tb.configure(yscrollcommand=self.vbar.set)


    @property
    def txt(self) -> str: return self.tb.txt
    @txt.setter
    def txt(self, value: str): self.tb.txt = value



    def _setCommand(self, add: bool):
        self.command_cb = self.tb.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



class Scale(tk.Scale, BaseTkinterWidget):
    def __init__(self, master, **kwargs):
        tk.Scale.__init__(self, master, **kwargs)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

