# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from abc import ABC
from typing import Any, Dict

from .Frames import *
from .Widgets import *




__all__ = [
        'ButtonGrid',
        ]

class ButtonGrid(Frame, ABC):
    _buttons: Dict[int, Button] = { }
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
        Frame.__init__(self, master=master)
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
    def _Count(self) -> int: return self._rows * self._cols

    @property
    def ButtonTitles(self) -> Dict[int, str]: raise NotImplementedError()
    @property
    def ButtonCommands(self) -> Dict[int, callable]: raise NotImplementedError()


