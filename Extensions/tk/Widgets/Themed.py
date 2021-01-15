# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
import random
from typing import Any, Dict, Iterable, List, Tuple, Union

from .BaseWidgets import *
from .Frames import *
from .base import *
from ..Events import *
from ..Enumerations import *




__all__ = [
        'TreeViewThemed', 'TreeViewHolderThemed', 'ListItem', 'ItemCollection', 'DelimiterError',
        'ComboBoxThemed', 'ButtonThemed', 'EntryThemed', 'LabelThemed', 'NotebookThemed', 'SeparatorThemed', 'ScrollbarThemed',
        ]

TODO = """
--Button
CheckButton
--ComoboBox
--Entry
--Frame
--LabelFrame
--Label
--Notebook
PanedWidnow
ProgressBar
RadioButton
Scale
Separator
SizeGrip
Scrollbar
--ThemedTreeView
"""

class ComboBoxThemed(ttk.Combobox, BaseTextTkinterWidget, CommandMixin):
    """Construct a Ttk Combobox _widget with the master master.

    STANDARD OPTIONS

        class, cursor, style, takefocus

    WIDGET-SPECIFIC OPTIONS

        exportselection
        postcommand

        textvariable

        values

        justify
        state
        height
        width
    """
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        ttk.Combobox.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    @property
    def value(self) -> bool: return self._txt.get()
    @value.setter
    def value(self, v: str): self._txt.set(v)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ComboboxSelected, self._cmd, add=add)
        return self

    def SetValues(self, values: list or tuple):
        self.configure(values=values)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




class ScrollbarThemed(ttk.Scrollbar, BaseTkinterWidget):
    def __init__(self, master, orientation: Orient, **kwargs):
        ttk.Scrollbar.__init__(self, master, orient=orientation.value, **kwargs)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




class DelimiterError(Exception): pass
class ListItem(dict):
    @property
    def ID(self) -> str: return self.get("ID", None)
    @property
    def Name(self) -> str: return self.get("Name", None)
    @property
    def Children(self):
        """
        :return:
        :rtype: ItemCollection or None
        """
        return self.get("Children", None)

    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            if "Children" in d:
                if not isinstance(d["Children"], list): raise TypeError(f"""Expecting {list} got type {type(d["Children"])}""")
                d["Children"] = ItemCollection.Parse(d["Children"])

            return ListItem(d)

        raise TypeError(f"""Expecting {dict} got type {type(d)}""")

    @staticmethod
    def Create(ID: str, Name: str, Children: List = None):
        """
        :param ID: Unique Identifier
        :type ID: str
        :param Name: Display Name
        :type Name: str
        :param Children: Nested ListItems
        :type Children: List[ListItem]
        :return:
        :rtype: ListItem
        """
        return ListItem.Parse(dict(ID=ID, Name=Name, Children=Children))
class ItemCollection(list):
    def __init__(self, d: Union[List[ListItem], Iterable[ListItem]]):
        list.__init__(self, d)

    def __setitem__(self, key: int, value: ListItem): return super().__setitem__(key, value)
    def __getitem__(self, key: int) -> ListItem: return super().__getitem__(key)
    def Slice(self, key: slice): return ItemCollection(super().__getitem__(key))

    def __iter__(self) -> Iterable[ListItem]: return super().__iter__()
    def enumerate(self) -> Iterable[Tuple[int, ListItem]]: return enumerate(self)
    def Iter(self) -> Iterable[int]: return range(len(self))

    def Names(self) -> Iterable[str]: return map(lambda o: getattr(o, 'Name'), self)
    def IDs(self) -> Iterable[str]: return map(lambda o: getattr(o, 'ID'), self)



    @classmethod
    def Parse(cls, d):
        if isinstance(d, list):
            return cls(map(ListItem.Parse, d))

        raise TypeError(f"""Expecting {list} got type {type(d)}""")
class TreeViewThemed(ttk.Treeview, BaseTkinterWidget, CommandMixin):
    """Construct a Ttk Treeview with parent master.

    STANDARD OPTIONS

        class, cursor, style, takefocus, xscrollcommand,
        yscrollcommand

    WIDGET-SPECIFIC OPTIONS

        columns, displaycolumns, height, padding, selectmode, show

    ITEM OPTIONS

        text, image, values, open, tags

    TAG OPTIONS

        foreground, background, font, image
    """
    last_focus: int or str
    focus_tags: List[str] = []
    SelectedItems: List = []
    items: Union[ListItem, ItemCollection] = None

    def __init__(self, master: FrameTypes, Color: dict = None, selectmode: SelectionMode = SelectionMode.Extended, **kwargs):
        ttk.Treeview.__init__(self, master=master, selectmode=selectmode.value, **kwargs)
        BaseTkinterWidget.__init__(self, Color)
        self.SetCommand(self.OnSelectRow)

        self.foreground = self.CreateForegroundColorTags()
        self.background = self.CreateBackgroundColorTags()
        for color, kw in self.foreground.items(): self.tag_configure(color, **kw)
        for color, kw in self.background.items(): self.tag_configure(color, **kw)

    @staticmethod
    def CreateForegroundColorTags(*colors) -> dict: return TreeViewThemed.CreateColorTags(*colors, kw='foreground')
    @staticmethod
    def CreateBackgroundColorTags(*colors) -> dict: return TreeViewThemed.CreateColorTags(*colors, kw='background')
    @staticmethod
    def CreateColorTags(*colors, kw: str) -> dict:
        """
            https://stackoverflow.com/questions/48358084/how-to-change-the-foreground-or-background-colour-of-a-selected-cell-in-tkinter/48361639

        :param colors: a list of strings passed as arguments to be converted into tag dictionaries
        :type colors: str
        :param kw: the keyword to change in the tag dictionary
        :type kw: str
        :return: tag dictionary
        :rtype: dict
        """
        if not colors: colors = ("red", "green", "black", "blue", "white", "yellow", "orange", "pink", "grey", "purple", "brown")
        return { f'{kw}_{c}': { kw: c } for c in colors }

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.TreeViewSelect, self._cmd, add=add)
        return self

    def SetTags(self, **tags: Dict[str, Dict[str, Any]]):
        for _ in self.SetTagsIter(**tags): pass
    def SetTagsIter(self, **tags: Dict[str, Dict[str, Any]]) -> Iterable[Tuple[str, Union[Dict[str, Any], str]]]:
        if tags:
            for tag, kwargs in tags.items():
                yield tag, self.tag_configure(tag, **kwargs)

    def Clear(self): self.delete(*self.get_children())

    def SetItems(self, items: Union[ListItem, ItemCollection], *, clear: bool = True, Open: bool = True):
        if clear: self.Clear()
        self.items = items
        self._json_tree(self.items, Open=Open)
    def _json_tree(self, d: Union[ListItem, ItemCollection], *, parent: str = '', Open: bool):
        if not d: return
        if not isinstance(parent, str): raise TypeError(type(parent), (str,))

        if isinstance(d, ListItem):
            self.insert(parent, index=tk.END, iid=d.ID, text=d.Name, open=Open)
            self._json_tree(d.Children, parent=d.ID, Open=Open)

        elif isinstance(d, ItemCollection):
            for item in d:
                if not isinstance(item, ListItem): raise TypeError(type(item), (ListItem,))
                self.insert(parent, index=tk.END, iid=item.ID, text=item.Name, open=Open)
                self._json_tree(item.Children, parent=item.ID, Open=Open)

        else: raise TypeError(type(d), (ListItem, ItemCollection))


    def column(self, column, option=None, **kw):
        return super(TreeViewThemed, self).column(column, option, **self.convert_kwargs(kw))
    def heading(self, column, option=None, **kw):
        return super(TreeViewThemed, self).heading(column, option, **self.convert_kwargs(kw))

    def selection(self) -> Tuple[str]: return super(TreeViewThemed, self).selection()

    # noinspection PyUnusedLocal
    def OnSelect(self, event: tkEvent = None):
        if not isinstance(event, TkinterEvent):
            event = TkinterEvent(event)
        _iid = self.identify_row(event.y)
        if _iid != self.last_focus:
            if self.last_focus:
                self.item(self.last_focus, tags=[])
            self.item(_iid, tags=self.focus_tags)
            self.last_focus = _iid
    # noinspection PyUnusedLocal
    def OnSelectRow(self, event: tkEvent = None):
        for _id in self.selection():
            fg = random.choice(tuple(self.foreground.values()))
            bg = random.choice(tuple(self.background.values()))
            if self.tag_has('sel', _id): self.item(_id, tags=[''])
            else: self.item(_id, tags=['sel', fg, bg])

        self.SelectedItems = self.tag_has('sel')

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))
class TreeViewHolderThemed(Frame):
    """Construct a Ttk Treeview with master scale.

    STANDARD OPTIONS
        class, cursor, style, takefocus, xscrollcommand,
        yscrollcommand

    WIDGET-SPECIFIC OPTIONS
        columns, displaycolumns, height, padding, selectmode, show

    ITEM OPTIONS
        text, image, values, open, tags

    TAG OPTIONS
        foreground, background, font, image

    --------------------------------------------------------------
    Also creates ttk.scrollbar and the _root_frame that conatins
    both ThemedTreeView and ScrollBar objects
    """
    TreeView: TreeViewThemed
    vsb: ScrollbarThemed
    hsb: ScrollbarThemed
    def __init__(self, master, backgroundColor: str, showScrollBars: ShowScrollBars = ShowScrollBars.Always, **kwargs):
        Frame.__init__(self, master=master, bg=backgroundColor, **kwargs)

        for i in range(1): self.Grid_RowConfigure(i, weight=1)
        for i in range(1): self.Grid_ColumnConfigure(i, weight=1)

        self.TreeView = TreeViewThemed(master=self, **kwargs).Grid(row=0, column=0)

        self.vsb = ScrollbarThemed(master=self, orientation=Orient.Vertical, command=self.TreeView.yview).Grid(row=0, column=1, rowspan=2)
        self.hsb = ScrollbarThemed(master=self, orientation=Orient.Horizonal, command=self.TreeView.xview).Grid(row=1, column=0)

        self.TreeView.configure(yscrollcommand=self.vsb.set)
        self.TreeView.configure(xscrollcommand=self.hsb.set)

        if showScrollBars == ShowScrollBars.Never:
            self.vsb.hide()
            self.hsb.hide()

        elif showScrollBars == ShowScrollBars.Always:
            self.vsb.show()
            self.hsb.show()

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




# noinspection DuplicatedCode
class ButtonThemed(ttk.Button, BaseTextTkinterWidget, ImageMixin, CommandMixin):
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
        ttk.Button.__init__(self, master=master, **kwargs)
        cmd = kwargs.pop('command', None)
        if cmd: self.SetCommand(cmd)

        if Command: self.SetCommand(Command)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)


    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



# noinspection DuplicatedCode
class LabelThemed(ttk.Label, BaseTextTkinterWidget, ImageMixin):
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
        ttk.Label.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




# noinspection DuplicatedCode
class EntryThemed(ttk.Entry, BaseTextTkinterWidget, CommandMixin):
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
        ttk.Entry.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    def Clear(self): self.delete(0, Tags.End.value)

    def _setCommand(self, add: bool):
        self.command_cb = self.Bind(Bindings.ButtonPress, self._cmd, add=add)
        return self

    @property
    def txt(self) -> str: return self.get()
    @txt.setter
    def txt(self, value: str):
        self.Clear()
        self.insert(Tags.End.value, value)

    def Append(self, value: str):
        self.insert(Tags.End.value, value)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))




class NotebookThemed(BaseTextTkinterWidget, ttk.Notebook):
    def __init__(self, master, Color: dict = None, **kwargs):
        ttk.Notebook.__init__(self, master=master, **kwargs)
        BaseTkinterWidget.__init__(self, Color=Color)

    def Add(self, w: BaseTkinterWidget, add: dict = dict(padding=2), *, title: str, **kwargs) -> int:
        """Adds a new tab to the notebook.

        If window is currently managed by the notebook but hidden, it is restored to its previous position."""
        index = self.add(w, **add)
        self.tab(index, text=title, **kwargs)
        return index
    def add(self, child: BaseTkinterWidget, **kw) -> int:
        """Adds a new tab to the notebook.

        If window is currently managed by the notebook but hidden, it is restored to its previous position.

        Returns the index of the child. """
        ttk.Notebook.add(self, child, **kw)
        return self.index_of(child)

    def hide_tab(self, tab_id: Union[int, str]):
        """Hides the tab specified by tab_id.

        The tab will not be displayed, but the associated window remains managed by the notebook and its configuration remembered.
        Hidden tabs may be restored with the add command."""
        return ttk.Notebook.hide(self, tab_id)
    def forget(self, tab_id: Union[int, str]):
        """Removes the tab specified by tab_id, unmaps and unmanages the associated window."""
        return ttk.Notebook.forget(self, tab_id)
    def identify(self, x: int, y: int) -> Union[int, str]:
        """Returns the name of the tab element at position x, y, or the empty string if none."""
        return ttk.Notebook.identify(self, x, y)

    def index_of(self, widget: Union[BaseTkinterWidget, str]) -> int:
        if not isinstance(widget, str): _w = str(widget)
        else: _w = widget

        for i, w in enumerate(self.tabs()):
            if w == _w: return i

        raise ValueError(f'widget {widget} is not found in the tabs.')
    def index(self, tab_id: Union[int, str]):
        """Returns the numeric index of the tab specified by tab_id, or the total number of tabs if tab_id is the string "end"."""
        return ttk.Notebook.index(self, tab_id)

    def insert(self, pos: int, child: BaseTkinterWidget, **kw):
        """Inserts a pane at the specified position.

        pos is either the string end, an integer index, or the name of a managed child.
        If child is already managed by the notebook, moves it to the specified position."""
        return ttk.Notebook.insert(self, pos, child, **kw)

    def select(self, tab_id: Union[int, str] = None) -> Union[int, str]:
        """Selects the specified tab.

        The associated child window will be displayed, and the previously-selected window (if different) is unmapped.
        If tab_id is omitted, returns the widget name of the currently selected pane."""
        return ttk.Notebook.select(self, tab_id)

    def tab(self, tab_id: Union[int, str], option: str = None, **kw) -> Union[dict, Union[int, str]]:
        """Query or modify the options of the specific tab_id.

        If kw is not given, returns a dict of the tab option values.

        If option is specified, returns the value of that option.

        Otherwise, sets the options to the corresponding values."""
        return ttk.Notebook.tab(self, tab_id, option, **kw)
    def tabs(self) -> List[BaseTkinterWidget]:
        """Returns a list of windows managed by the notebook."""
        return ttk.Notebook.tabs(self)

    def enable_traversal(self):
        """Enable keyboard traversal for a toplevel window containing this notebook.

        This will extend the bindings for the toplevel window containing this notebook as follows:

            Control-Tab: selects the tab following the currently selected one

            Shift-Control-Tab: selects the tab preceding the currently selected one

            Alt-K: where K is the mnemonic (underlined) character of any tab, will select that tab.


        Multiple notebooks in a single toplevel may be enabled for traversal, including nested notebooks.
        However, notebook traversal only works properly if all panes are direct children of the notebook.


        The only, and good, difference I see is about mnemonics, which works after calling this method.
        Control-Tab and Shift-Control-Tab always works (here at least).
        """
        return ttk.Notebook.enable_traversal(self)


    @property
    def ActiveTab(self) -> Union[int, str]: return self.select()
    @ActiveTab.setter
    def ActiveTab(self, tab_id: Union[int, str]): self.select(tab_id)


    @property
    def txt(self) -> str: return self.tab(self.ActiveTab, option='text')
    @txt.setter
    def txt(self, value: str): self.tab(self.ActiveTab, text=value)


    @property
    def wrap(self) -> int: return self.tab(self.ActiveTab, option='wraplength')
    @wrap.setter
    def wrap(self, value: int):
        assert (isinstance(value, int))
        self.tab(self.ActiveTab, wraplength=self._wrap)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))


class SeparatorThemed(ttk.Separator, BaseTkinterWidget):
    def __init__(self, master, orientation: Orient = Orient.Horizonal):
        ttk.Separator.__init__(self, master, orient=orientation.value)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))


class CheckButtonThemed(ttk.Checkbutton, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Ttk Checkbutton widget which is either in on- or off-state.

    Construct a Ttk Checkbutton widget with the parent master.

    STANDARD OPTIONS

        class, compound, cursor, image, state, style, takefocus,
        text, textvariable, underline, width

    WIDGET-SPECIFIC OPTIONS

        command, offvalue, onvalue, variable
    """
    _value: tk.BooleanVar
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        ttk.Checkbutton.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)
        self._value = tk.BooleanVar(master=self, value=False)
        self.configure(variable=self._value)


    @property
    def value(self) -> bool: return self._value.get()
    @value.setter
    def value(self, b: bool):  # FIXME: ignores value passed. only toggles true/false.
        self._value.set(b)

        self.invoke()

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))
