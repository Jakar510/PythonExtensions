from enum import IntEnum, StrEnum




# import cython
#
# from cython.view cimport array as cvarray
# from cython.operator cimport dereference as deref
#
# try:
#     from itertools import izip_longest
# except ImportError:
#     from itertools import zip_longest as izip_longest
#
# from libc.stdlib cimport malloc
# from libc.stdint cimport uintptr_t
# from libc.string cimport strdup
# from libc.string cimport strncpy
# from libc.float  cimport FLT_MAX
# from libcpp cimport bool
#
# # cimport enums
# # cimport ansifeed
# # from cpython.version cimport PY_MAJOR_VERSION


cpdef class ShowScrollBars(IntEnum):
    Never = 0
    Always = 1
    Auto = 2

cpdef class Layout(IntEnum):
    place = 1
    grid = 2
    pack = 3

cpdef class ViewState(StrEnum):
    # v _widget and button states
    Normal = 'NORMAL'
    Disabled = 'DISABLED'
    Active = 'ACTIVE'
    Hidden = 'HIDDEN'  # Canvas state

cpdef class AnchorAndSticky(StrEnum):
    North = 'N'
    South = 'S'
    West = 'W'
    East = 'E'
    NorthEast = 'NE'
    SouthEast = 'SE'
    NorthWest = 'NW'
    SouthWest = 'SW'
    NorthSouth = 'NS'
    EastWest = 'EW'
    All = 'NSEW'
    Center = 'CENTER'

cpdef class Fill(StrEnum):
    none = 'NONE'
    x = 'X'
    y = 'Y'
    both = 'BOTH'

cpdef class Side(StrEnum):
    left = 'LEFT'
    top = 'TOP'
    right = 'RIGHT'
    bottom = 'BOTTOM'

cpdef class Relief(StrEnum):
    Raised = 'RAISED'
    Sunken = 'SUNKEN'
    Flat = 'FLAT'
    Ridge = 'RIDGE'
    Groove = 'GROOVE'
    Solid = 'SOLID'

cpdef class Orient(StrEnum):
    Horizontal = 'HORIZONTAL'
    Vertical = 'VERTICAL'

cpdef class Wrap(StrEnum):
    Char = 'CHAR'
    Word = 'WORD'

cpdef class BorderMode(StrEnum):
    Inside = 'INSIDE'
    Outside = 'OUTSIDE'

cpdef class Tags(StrEnum):  # Special tags marks and insert positions
    Select = 'SEL'
    SelectFirst = 'SEL_FIRST'
    SelectLast = 'SEL_LAST'
    End = 'END'
    Insert = 'INSERT'
    Current = 'CURRENT'
    Anchor = 'ANCHOR'
    First = 'FIRST'
    All = 'all'  # e.g. Canvas.delete(ALL)

cpdef class MenuItemTypes(StrEnum):  # Menu item types
    Cascade = 'cascade'
    CheckButton = 'checkbutton'
    Command = 'command'
    RadioButton = 'radiobutton'
    Separator = 'separator'

cpdef class SelectionMode(StrEnum):  # Selection modes for list boxes
    Single = 'single'
    Browse = 'browse'
    Multiple = 'multiple'
    Extended = 'extended'

cpdef class ActiveStyle(StrEnum):  # Activestyle for list boxes
    DotBox = 'dotbox'
    Underlined = 'underlined'
    none = 'none'

# Various canvas styles
cpdef class CanvasStyles(StrEnum):
    PieSlice = 'pieslice'
    Chord = 'chord'
    Arc = 'arc'
    First = 'first'
    Last = 'last'
    Butt = 'butt'
    Projecting = 'projecting'
    Round = 'round'
    Bevel = 'bevel'
    Miter = 'miter'

cpdef class ViewArguments(StrEnum):  # Arguments to xview/yview
    MoveTo = 'moveto'
    Scroll = 'scroll'
    Units = 'units'
    Pages = 'pages'

cpdef class Orientation(IntEnum):
    Landscape = 0
    Portrait = 1

cpdef class RotationAngle(IntEnum):
    none = 0
    right = 90
    upside_down = 180
    left = 270
cpdef RotationAngle Rotate(RotationAngle self, int angle = -90): return RotationAngle((&self + angle) % 360)