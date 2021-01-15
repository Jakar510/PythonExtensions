# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from typing import List, Tuple

from ..Widgets.base import *




__all__ = ['Style']

class Style(ttk.Style):
    def Configure_Root(self, background: str, foreground: str, selected: str, active: str, font: str):
        self.configure('.', background=background, foreground=foreground, font=font)
        self.map('.', background=[('selected', selected), ('active', active)])

    def Configure_NotebookTab(self, background: str, foreground: str, selected: str, active: str, font: str, padding: Tuple[int, int]):
        self.configure('TNotebook.Tab', background=background, foreground=foreground)
        self.map('TNotebook.Tab', background=[('selected', selected), ('active', active)])
        self.theme_settings(self.CurrentTheme, { "TNotebook.Tab": { "configure": { "padding": padding, 'font': font } } })


    @property
    def Themes(self) -> List[str]: return self.theme_names()


    @property
    def CurrentTheme(self): return self.theme_use()
    @CurrentTheme.setter
    def CurrentTheme(self, theme: str): self.theme_use(theme)
