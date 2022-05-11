# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
from asyncio import AbstractEventLoop
from io import BytesIO
from os import PathLike
from os.path import *
from typing import *

from PIL.Image import Image
from PIL.ImageTk import PhotoImage
from PythonExtensions.Names import typeof
from aiohttp import ClientResponse, ClientSession
from requests import get

from .Base import *
from .Enumerations import *
from .Events import *




# from aiofiles import open as async_file_open


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

        command, compound, default, Height,
        overrelief, state, Width
    """
    __slots__ = ['_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 Command: callable = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)
        cmd = kwargs.pop('command', None)
        if cmd: self.SetCommand(cmd)

        if Command: self.SetCommand(Command)

    def _options(self, cnf, kwargs=None) -> dict:
        return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

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

        Height, state, Width

    """
    __slots__ = ['_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)



    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Message(tk.Message, BaseTextTkinterWidget, CommandMixin):
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 loop: Optional[AbstractEventLoop] = None,
                 Color: Optional[Dict[str, str]] = None,
                 **kwargs):
        tk.Message.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Entry(tk.Entry, BaseTextTkinterWidget, CommandMixin):
    __doc__ = """Construct an entry _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, Width,
    xscrollcommand.
    """
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)

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

# ------------------------------------------------------------------------------------------

class CheckButton(tk.Checkbutton, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a checkbutton _widget with the master MASTER.

        Valid resource names:

                Width
                Height

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
    __slots__ = ['_value', '_cmd', 'command_cb', '_IMG', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    _value: tk.BooleanVar
    def __init__(self, master,
                 text: str = '',
                 Override_var: tk.StringVar = None,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Checkbutton.__init__(self, master, **kwargs)
        BaseTextTkinterWidget.__init__(self, text, Override_var, Color, loop)
        ImageMixin.__init__(self)
        self._value = tk.BooleanVar(master=self, value=False)
        self.configure(variable=self._value)


    @property
    def value(self) -> bool:
        return self._value.get()
    @value.setter
    def value(self, b: bool):
        self._value.set(b)
        if b:
            self.select()
        else:
            self.deselect()

    def _options(self, cnf, kwargs=None) -> dict:
        return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Listbox(tk.Listbox, BaseTextTkinterWidget, CommandMixin):
    """Construct a listbox _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, Height, highlightbackground,
    highlightcolor, highlightthickness, relief, selectbackground,
    selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
    Width, xscrollcommand, yscrollcommand, listvariable.

    Allowed WordWrap modes are ('word', 'none', 'char')
    """
    __slots__ = ['_Current_ListBox_Index', '_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    _Current_ListBox_Index: Optional[int]
    def __init__(self, master,
                 *,
                 Command: callable = None,
                 z=None,
                 selectMode: Union[str, SelectionMode] = tk.SINGLE,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Listbox.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self.SetSelectMode(selectMode)
        if Command is not None: self.SetCommand(Command, z=z)
        self._Current_ListBox_Index = None
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
    def Current_Index(self, event: TkinterEvent = None) -> Optional[int]:
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
    def GetAtIndex(self, index: int) -> str:
        return self.get(index)
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
        if forward:
            i += amount
        else:
            i -= amount

        if i > self.Count:
            if extend:
                for _ in range(amount): self.Append('')
            else:
                i = self.Count
        elif i < 0:
            i = 0

        self.Index = i

    def SetList(self, temp_list: Iterable):
        """        clear the listbox and set the new items.        """
        self.Clear()
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def AddList(self, temp_list: Iterable):
        """        Append items from the list into the listbox.        """
        for item in temp_list:
            self.Append(item)
    def SortList(self, key: Callable = str.lower):
        """        function to sort listbox items case insensitive by default.        """
        temp_list = self.Items
        temp_list.sort(key=key)
        # delete contents of present listbox
        self.delete(0, Tags.End.value)
        # load listbox with sorted data
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def Append(self, value: str):
        self.insert(Tags.End.value, value)


    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ListboxSelect, self._cmd, add=add)
        return self
    def ResetColors(self, color: str):
        for i in range(self.Count):
            self.itemconfig(i, background=color)

    @property
    def Items(self) -> list:
        """ returns the current listbox contents """
        return list(self.get(0, Tags.End.value))


    def IsAllValidItems(self) -> bool:
        return all(self.Items)
    def ValidCount(self) -> int:
        count = 0
        for item in self.Items:
            if item: count += 1

        return count

    @property
    def Count(self) -> int:
        return tk.Listbox.size(self)

    @property
    def Index(self) -> int or None:
        return self._Current_ListBox_Index
    @Index.setter
    def Index(self, value: int or None):
        self._Current_ListBox_Index = value
        if value is not None: self.SelectRow(value)

    @property
    def txt(self) -> str:
        return self.GetAtIndex(self._Current_ListBox_Index)
    @txt.setter
    def txt(self, value: str):
        self.ReplaceAtIndex(self._Current_ListBox_Index, value)

    def _options(self, cnf, kwargs=None) -> dict:
        return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Canvas(tk.Canvas, BaseTkinterWidget):
    __slots__ = ['_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 Color: Dict[str, str] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self._setupBindings()


    def DownloadImage(self, url: Union[URL, str], x: int, y: int, *formats: str, width: int = None, height: int = None, **kwargs):
        if isinstance(url, URL) or isinstance(url, str) and url.lower().strip().startswith('http'):
            reply = get(url, **kwargs)
            return self.SetImageFromBytes(reply.content, x, y, *formats, width=width, height=height)

        raise TypeError(typeof(url), (str, URL))
    async def DownloadImageAsync(self, url: Union[URL, str], x: int, y: int, *formats: str, width: int = None, height: int = None, **kwargs):
        if isinstance(url, URL) or isinstance(url, str) and url.lower().strip().startswith('http'):
            async with ClientSession() as session:
                reply: ClientResponse = await session.get(url, **kwargs)
                content = await reply.read()
                return self.SetImageFromBytes(content, x, y, *formats, width=width, height=height)

        raise TypeError(typeof(url), (str, URL))


    def OpenImage(self, path: PathLike, x: int, y: int, *formats: str, width: int = None, height: int = None) -> Tuple[PhotoImage, int]:
        assert (isfile(path))

        with open(path, 'rb') as f:
            img = ImageMixin.open(self, f, width, height, *formats)
            return self.CreateImage(image=img, x=x, y=y)
    async def OpenImageAsync(self, path: PathLike, x: int, y: int, *formats: str, width: int = None, height: int = None) -> Tuple[PhotoImage, int]:
        assert (isfile(path))

        async with async_file_open(path, 'rb') as f:
            img = ImageMixin.open(self, f, width, height, *formats)
            return self.CreateImage(image=img, x=x, y=y)


    def SetImageFromBytes(self, data: bytes, x: int, y: int, *formats: str, width: int = None, height: int = None) -> Tuple[PhotoImage, int]:
        assert (isinstance(data, bytes))

        with BytesIO(data) as buf:
            img = ImageMixin.open(self, buf, width, height, *formats)
            return self.CreateImage(image=img, x=x, y=y)


    def CreateImage(self, image: Union[Image, tkPhotoImage], x: int, y: int, anchor: Union[str, AnchorAndSticky] = tk.NW) -> Tuple[tkPhotoImage, int]:
        if not isinstance(image, tkPhotoImage): image = tkPhotoImage(image, size=image.size)

        return image, self.create_image(x, y, anchor=anchor, image=image)


    def GetItemPosition(self, _id) -> Optional[Tuple[int, int]]:
        try:
            return self.coords(_id)
        except tk.TclError:
            return None


    def _setupBindings(self):
        self.bind(Bindings.ButtonPress.value, func=self.HandleRelease)
        self.bind(Bindings.ButtonRelease.value, func=self.HandlePress)

        self.bind(Bindings.FocusIn.value, func=self.HandleFocusIn)
        self.bind(Bindings.FocusOut.value, func=self.HandleFocusOut)

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

    def _options(self, cnf, kwargs=None) -> dict:
        return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Scrollbar(tk.Scrollbar, BaseTkinterWidget, CommandMixin):
    """Construct a scrollbar widget with the parent MASTER.

    Valid resource names: activebackground, activerelief,
    background, bd, bg, borderwidth, command, cursor,
    elementborderwidth, highlightbackground,
    highlightcolor, highlightthickness, jump, orient,
    relief, repeatdelay, repeatinterval, takefocus,
    troughcolor, Width."""
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master,
                 orientation: Orient,
                 Color: Optional[Dict[str, str]] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Scrollbar.__init__(self, master, orient=orientation.value, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Text(tk.Text, BaseTextTkinterWidget, CommandMixin):
    class Index(str):
        @classmethod
        def Create(cls, line: int, char: int): return cls(f'{line}.{char}')
        @classmethod
        def End(cls): return cls(tk.END)



    __doc__ = """Construct a text widget with the parent MASTER.

    STANDARD OPTIONS

        background, borderwidth, cursor,
        exportselection, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, insertbackground,
        insertborderwidth, insertofftime,
        insertontime, insertwidth, padx, pady,
        relief, selectbackground,
        selectborderwidth, selectforeground,
        setgrid, takefocus,
        xscrollcommand, yscrollcommand,

    WIDGET-SPECIFIC OPTIONS

        autoseparators, Height, maxundo,
        spacing1, spacing2, spacing3,
        state, tabs, undo, Width, wrap,

    """
    __slots__ = ['_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']

    def __init__(self, master,
                 text: str = '',
                 Color: Optional[Dict[str, str]] = None,
                 loop: Optional[AbstractEventLoop] = None,
                 **kwargs):
        tk.Text.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self.txt = text


    def Clear(self): self.delete(self.Index.Create(1, 0), self.Index.End())
    def ClearTags(self): return self.tag_delete(*self.Tags())
    def Tags(self, index: int = None) -> List[str]: return self.tag_names(index)

    def Replace(self, new_text: str, start: Index, end: Index):
        self.delete(start, end)
        return self.insert(start, new_text)

    @property
    def txt(self) -> str: return self.get(self.Index.Create(1, 0), self.Index.End())
    @txt.setter
    def txt(self, value: str): self.insert(self.Index.Create(1, 0), value)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class ScrolledText(Frame, BaseTextTkinterWidget, CommandMixin):
    tb: Text
    vbar: Scrollbar
    hbar: Scrollbar
    __slots__ = ['tb', 'vbar', 'hbar', '_cmd', 'command_cb', '_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, text: str = '', Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **frame_kwargs):
        Frame.__init__(self, master, **frame_kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)
        self.Grid_RowConfigure(0, weight=10)
        self.Grid_RowConfigure(1, weight=1)
        self.Grid_ColumnConfigure(0, weight=10)
        self.Grid_ColumnConfigure(1, weight=1)
        self.tb = Text(master=self).Grid(0, 0)
        self.tb.txt = text

        self.vbar = Scrollbar(self, orientation=Orient.Vertical)
        self.vbar.Grid(0, 1)
        self.vbar.SetCommand(self.tb.yview)
        self.tb.configure(yscrollcommand=self.vbar.set)

        self.hbar = Scrollbar(self, orientation=Orient.Horizonal)
        self.hbar.Grid(1, 0, columnspan=2)
        self.hbar.SetCommand(self.tb.xview)
        self.tb.configure(xscrollcommand=self.hbar.set)


    @property
    def txt(self) -> str: return self.tb.txt
    @txt.setter
    def txt(self, value: str): self.tb.txt = value



    def _setCommand(self, add: bool):
        self.command_cb = self.tb.Bind(Bindings.ButtonPress, func=self._cmd, add=add)
        return self

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

# ------------------------------------------------------------------------------------------

class Scale(tk.Scale, BaseTkinterWidget):
    __slots__ = ['_state_', '__bindings__', '_pi', '_manager_', '_wrap', '_cb', '_loop', '_txt']
    def __init__(self, master, Color: Optional[Dict[str, str]] = None, loop: Optional[AbstractEventLoop] = None, **kwargs):
        tk.Scale.__init__(self, master, **kwargs)
        BaseTkinterWidget.__init__(self, Color, loop)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))
