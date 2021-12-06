# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
import tkinter as tk
from typing import *

from ..Core.Names import nameof




__all__ = ['DebugWidget', 'DebugWidgetRecursively']

def _rootLevelDataRecursive(w) -> Dict[str, Any]:
    return _WidgetDataRecursive(w)
def _WidgetDataRecursive(w) -> Dict[str, Any]:
    from ..tk.Base import BaseTkinterWidget

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


def _childData(obj: Union[List, Dict]):
    if isinstance(obj, dict):
        r = { }
        for key, w in obj:
            print('type(w)', type(w))
            print('type(key)', type(key))
            r[key] = _WidgetDataRecursive(w)
        return r

    if isinstance(obj, list):
        r = []
        for w in obj:
            print('type(w)', type(w))
            r.append((w.winfo_id(), _WidgetDataRecursive(w)))
        return dict(r)

    return obj
def DebugWidgetRecursively(w, *, Message: str):
    from ..tk.Base import BaseTkinterWidget

    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    from pprint import PrettyPrinter

    pp = PrettyPrinter(indent=4)
    print(f'---------------- {Message} < {nameof(w)} > ----------------')
    pp.pprint(_rootLevelDataRecursive(w))
    print()
    print()


def _rootLevelData(w, root: Union[tk.Tk, tk.Toplevel]) -> Dict[str, Any]:
    return {
        'root.children': root.children,
        # f'Widget: {w.__class__.__name__}':        _WidgetData(w)
        'Widget':        _WidgetData(w)
        }
def _WidgetData(w) -> Dict[str, Any]:
    from ..tk.Base import BaseTkinterWidget

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
def DebugWidget(w, *, root: Union[tk.Tk, tk.Toplevel], Message: str):
    from ..tk.Base import BaseTkinterWidget

    assert (isinstance(w, BaseTkinterWidget) and isinstance(w, tk.BaseWidget))
    from pprint import PrettyPrinter

    pp = PrettyPrinter(indent=4)
    print(f'---------------- {Message} < {w.__class__.__name__} > ----------------')
    pp.pprint(_rootLevelData(w, root))
    print()
    print()
