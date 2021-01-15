# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

from enum import Enum, IntEnum
from tkinter.constants import *




__all__ = [
        'ActiveStyle', 'AnchorAndSticky', 'Fill', 'Side', 'Relief', 'Orient', 'Wrap', 'BorderMode', 'Tags', 'ViewState', 'MenuItemTypes', 'SelectionMode', 'CanvasStyles', 'Layout',
        'ViewArguments', 'ShowScrollBars', 'Bools',
        ]

class ShowScrollBars(IntEnum):
    Never = 0
    Always = 1
    Auto = 2

class Layout(IntEnum):
    place = 1
    grid = 2
    pack = 3

class ViewState(Enum):  # v _widget and button states
    Normal = NORMAL
    Disabled = DISABLED
    Active = ACTIVE
    Hidden = HIDDEN  # Canvas state

class Bools(IntEnum):
    # NO = NO
    # YES = YES

    NO=FALSE=OFF=0
    YES=TRUE=ON=1
class AnchorAndSticky(Enum):
    North = N
    South = S
    West = W
    East = E
    NorthEast = NE
    SouthEast = SE
    NorthWest = NW
    SouthWest = SW
    NorthSouth = NS
    EastWest = EW
    All = NSEW
    Center = CENTER

class Fill(Enum):
    none = NONE
    x = X
    y = Y
    both = BOTH

class Side(Enum):
    left = LEFT
    top = TOP
    right = RIGHT
    bottom = BOTTOM

class Relief(Enum):
    Raised = RAISED
    Sunken = SUNKEN
    Flat = FLAT
    Ridge = RIDGE
    Groove = GROOVE
    Solid = SOLID

class Orient(Enum):
    Horizonal = HORIZONTAL
    Vertical = VERTICAL

class Wrap(Enum):
    Char = CHAR
    Word = WORD

class BorderMode(Enum):
    Inside = INSIDE
    Outside = OUTSIDE

class Tags(Enum):  # Special tags, marks and insert positions
    Select = SEL
    SelectFirst = SEL_FIRST
    SelectLast = SEL_LAST
    End = END
    Insert = INSERT
    Current = CURRENT
    Anchor = ANCHOR
    First = FIRST
    All = ALL  # e.g. Canvas.delete(ALL)

class MenuItemTypes(Enum):  # Menu item types
    Cascade = CASCADE
    CheckButton = CHECKBUTTON
    Command = COMMAND
    RadioButton = RADIOBUTTON
    Separator = SEPARATOR

class SelectionMode(Enum):  # Selection modes for list boxes
    Single = SINGLE
    Browse = BROWSE
    Multiple = MULTIPLE
    Extended = EXTENDED

class ActiveStyle(Enum):  # Activestyle for list boxes
    DotBox = DOTBOX
    Underlind = UNDERLINE
    none = NONE

# Various canvas styles
class CanvasStyles(Enum):
    PieSlice = PIESLICE
    Chord = CHORD
    Arc = ARC
    First = FIRST
    Last = LAST
    Butt = BUTT
    Projecting = PROJECTING
    Round = ROUND
    Bevel = BEVEL
    Miter = MITER

class ViewArguments(Enum):  # Arguments to xview/yview
    MoveTo = MOVETO
    Scroll = SCROLL
    Units = UNITS
    Pages = PAGES
