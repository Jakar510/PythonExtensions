# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from .Widgets.base import tk
from .Widgets.BaseWidgets import BaseTkinterWidget




__all__ = ['DebugWidget', 'DebugWidgetRecursively']

def _rootLevelDataRecurive(w) -> dict:
    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    return _WidgetDataRecurive(w)
def _WidgetDataRecurive(w) -> dict:
    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    return {
            'Type':                     w.__class__,
            'str(w)':                   str(w),
            'repr(w)':                  repr(w),
            'PI (position info)':       w.pi,
            # 'master.children':            w.master.children,
            'children':                 w.children,
            'winfo_id':                 w.winfo_id(),
            'winfo_name':               w.winfo_name(),
            'winfo_parent':             w.winfo_parent(),
            'winfo_manager':            w.winfo_manager(),
            'winfo_ismapped':           w.winfo_ismapped(),
            'winfo_pathname(winfo_id)': w.winfo_pathname(w.winfo_id()),
            'winfo_children':           _childData(w.winfo_children()),
            }

def _childData(obj):
    if isinstance(obj, dict):
        r = { }
        for key, w in obj:
            print('type(w)', type(w))
            print('type(key)', type(key))
            r[key] = _WidgetDataRecurive(w)
        return r

    if isinstance(obj, list):
        r = []
        for w in obj:
            print('type(w)', type(w))
            r.append((w.winfo_id(), _WidgetDataRecurive(w)))
        return dict(r)

    return obj
def DebugWidgetRecursively(w, *, Message: str):
    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    print(f'---------------- {Message} < {w.__class__.__name__} > ----------------')
    pp.pprint(_rootLevelDataRecurive(w))
    print()
    print()


def _rootLevelData(w, root: tk.Tk or tk.Toplevel) -> dict:
    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    return {
            'root.children': root.children,
            # f'Widget: {w.__class__.__name__}':        _WidgetData(w)
            'Widget':        _WidgetData(w)
            }
def _WidgetData(w) -> dict:
    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    return {
            'Type':                     w.__class__,
            'str(w)':                   str(w),
            'repr(w)':                  repr(w),
            'PI (position info)':       w.pi,
            'master.children':          w.root.children,
            'children':                 w.children,
            'winfo_id':                 w.winfo_id(),
            'winfo_name':               w.winfo_name(),
            'winfo_parent':             w.winfo_parent(),
            'winfo_manager':            w.winfo_manager(),
            'winfo_ismapped':           w.winfo_ismapped(),
            'winfo_pathname(winfo_id)': w.winfo_pathname(w.winfo_id()),
            'winfo_children':           w.winfo_children(),
            }
def DebugWidget(w, *, root: tk.Tk or tk.Toplevel, Message: str):
    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    print(f'---------------- {Message} < {w.__class__.__name__} > ----------------')
    pp.pprint(_rootLevelData(w, root))
    print()
    print()
