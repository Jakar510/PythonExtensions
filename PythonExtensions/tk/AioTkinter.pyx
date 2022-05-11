from enum import IntEnum, Enum

import cython
from cython.view cimport array as cvarray
from cython.operator cimport dereference as deref

try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest

from libc.stdlib cimport malloc
from libc.stdint cimport uintptr_t
from libc.string cimport strdup
from libc.string cimport strncpy
from libc.float  cimport FLT_MAX
from libcpp cimport bool

cimport cimgui
cimport enums
cimport ansifeed

from cpython.version cimport PY_MAJOR_VERSION

from tkinter.constants import *



#region Enums
cpdef class ShowScrollBars(IntEnum):
    Never = 0
    Always = 1
    Auto = 2

cpdef class Layout(IntEnum):
    place = 1
    grid = 2
    pack = 3

cpdef class ViewState(Enum):
    # v _widget and button states
    Normal = NORMAL
    Disabled = DISABLED
    Active = ACTIVE
    Hidden = HIDDEN  # Canvas state

cpdef class AnchorAndSticky(Enum):
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

cpdef class Fill(Enum):
    none = NONE
    x = X
    y = Y
    both = BOTH

cpdef class Side(Enum):
    left = LEFT
    top = TOP
    right = RIGHT
    bottom = BOTTOM

cpdef class Relief(Enum):
    Raised = RAISED
    Sunken = SUNKEN
    Flat = FLAT
    Ridge = RIDGE
    Groove = GROOVE
    Solid = SOLID

cpdef class Orient(Enum):
    Horizontal = HORIZONTAL
    Vertical = VERTICAL

cpdef class Wrap(Enum):
    Char = CHAR
    Word = WORD

cpdef class BorderMode(Enum):
    Inside = INSIDE
    Outside = OUTSIDE

cpdef class Tags(Enum):  # Special tags marks and insert positions
    Select = SEL
    SelectFirst = SEL_FIRST
    SelectLast = SEL_LAST
    End = END
    Insert = INSERT
    Current = CURRENT
    Anchor = ANCHOR
    First = FIRST
    All = ALL  # e.g. Canvas.delete(ALL)

cpdef class MenuItemTypes(Enum):  # Menu item types
    Cascade = CASCADE
    CheckButton = CHECKBUTTON
    Command = COMMAND
    RadioButton = RADIOBUTTON
    Separator = SEPARATOR

cpdef class SelectionMode(Enum):  # Selection modes for list boxes
    Single = SINGLE
    Browse = BROWSE
    Multiple = MULTIPLE
    Extended = EXTENDED

cpdef class ActiveStyle(Enum):  # Activestyle for list boxes
    DotBox = DOTBOX
    Underlined = UNDERLINE
    none = NONE

# Various canvas styles
cpdef class CanvasStyles(Enum):
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

cpdef class ViewArguments(Enum):  # Arguments to xview/yview
    MoveTo = MOVETO
    Scroll = SCROLL
    Units = UNITS
    Pages = PAGES

cpdef class RotationAngle(IntEnum):
    none = 0
    right = 90
    upside_down = 180
    left = 270

cpdef class Orientation(IntEnum):
    Landscape = 0
    Portrait = 1

cpdef RotationAngle Rotate(RotationAngle self, int angle = -90): return RotationAngle((&self + angle) % 360)
#endregion
