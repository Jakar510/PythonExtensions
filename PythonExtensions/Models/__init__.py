from enum import Enum
from typing import *




__all__ = ['InternalRequest']

_TAction = TypeVar('_TAction', Enum, str, int)
class InternalRequest(Generic[_TAction]):
    def __init__(self, action: _TAction, *args, **kwargs):
        self.Action: Final[_TAction] = action
        self.args: Final[Tuple] = args
        self.kwargs: Final[Dict[str, Any]] = kwargs

    def __hash__(self): return hash((self.Action, self.args, self.kwargs))
