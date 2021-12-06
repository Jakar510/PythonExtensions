# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------

from tkinter.messagebox import *

from ..Base import *
from ..Roots import *




__all__ = ['tkMessageBox']

class tkMessageBox(tkTopLevel, BaseTkinterWidget):
    """
    Not Implemented Yet.

    https://www.tutorialspoint.com/python3/tk_messagebox.htm
    """
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
