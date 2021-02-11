import re
from typing import *

from ..Exceptions import *
from ..Names import *




__all__ = [
    'BreakCase',
    'CallBackException',
    'ActiveSessionError',
    'InvalidRegexObject',
    'InactiveSessionError',

    '_BaseSwitchCase',
    'SwitchRegex',
    'SwitchVariable',
    'SwitchCallback',
    'SwitchInstance',
    'SwitchSubClass',
    ]




class Equalable(Protocol):
    def __eq__(self, *args, **kwargs) -> bool: ...



_TCase = TypeVar('_TCase')
class _BaseSwitchCase(Generic[_TCase]):
    """
     variable: the instance to check against.
     regex: the instance to check against.
     regex_pattern: the instance to check against.
     Check_Address: Checks the addresses between variable and the value_to_check, using "is".
     catch_value_to_check: If match is True, added the value_to_check to on_true_args at the start.
     no_match_callback: Optional Method that is called if no match is found or Exception that is raised if no match is found.
     no_match_handler_args (args): _no_match_handler's args
     no_match_handler_kwargs (kwargs): _no_match_handler's kwargs
    """
    __slots__ = ['_variable', '_break', 'no_match_handler']
    _active: bool = False
    _break: Optional[BreakCase]
    _no_match_handler: Optional[Union[Callable[[], None], Type[Exception]]]
    def __init__(self, variable: _TCase, no_match_handler: Optional[Union[Callable[[], None], Type[Exception]]] = None):
        """
        :param variable: the instance to check against.
        :param no_match_handler_args (args): _no_match_handler's args
        :param no_match_handler_kwargs (kwargs): _no_match_handler's kwargs
        """
        if not hasattr(variable, '__eq__'):
            raise AttributeError(f'variable is not a comparable type. {type(variable)}')

        self._variable: Final[_TCase] = variable
        self._no_match_handler = no_match_handler
        self._break = None
        self._active = False

    def __enter__(self):
        self._break = None
        self._active = True
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        if isinstance(exc_val, BreakCase): return True
        if self._no_match_handler is None: return
        if issubclass(self._no_match_handler, Exception): raise self._no_match_handler() from exc_val
        if callable(self._no_match_handler): return self._no_match_handler()
    def _exit(self) -> True:
        if isinstance(self._break, BreakCase):
            raise self._break

        elif self._break is None:
            self._break = BreakCase()

        else:
            raise TypeError(type(self._break), (BreakCase, type(None)))

        return True

    def _checkActive(self):
        if not self._active:
            raise InactiveSessionError(""" Context Manager Must be Used!

    For example:

    # value_to_check = one of [ variable OR instance OR type OR tuple of types ]
    with SwitchVariable(value_to_check) as sc:
        if sc(value_to_search_for):
            ...
        if sc(value_to_search_for): 
            ...
        ...
""")
    def __setattr__(self, key, value):
        if key not in ('_active', '_break') and self._active:
            raise ActiveSessionError(f"Attributes cannot be changed while the context manager is active.")

        super().__setattr__(key, value)

    def _check(self, value_to_check: _TCase): return self._variable == value_to_check



class SwitchRegex(_BaseSwitchCase[_TCase]):
    # noinspection PyMissingConstructor
    def __init__(self, regex: re.Pattern, method: str):
        """
        :param regex: the instance to check against.
        """
        if not hasattr(regex, method): raise AttributeError('method must be a callable function of the regex object.')
        self._re = regex
        self._regex: Final[Callable[[str], Any]] = getattr(regex, method)
        if not callable(self._regex): raise TypeError(f'regex.{method} is not callable')

    # noinspection PyMethodOverriding
    def __call__(self, value_to_check: _TCase) -> bool:
        self._checkActive()
        if self._check(value_to_check):
            return self._exit()

        return False
    def _check(self, value_to_check: str) -> bool:  # TODO: implement regex parsing for the value_to_check
        if not isinstance(value_to_check, str): return False

        return self._regex(value_to_check) is not None



class SwitchVariable(_BaseSwitchCase[_TCase]):
    def __call__(self, value_to_check: _TCase, *args, **kwargs) -> bool:
        self._checkActive()
        if self._check(value_to_check):
            return self._exit()

        return False



class SwitchCallback(_BaseSwitchCase[_TCase]):
    # noinspection PyMethodOverriding
    def __call__(self, value_to_check: _TCase, callback: Callable[[_TCase], None]) -> bool:
        self._checkActive()
        if self._check(value_to_check):
            callback(value_to_check)
            return self._exit()

        return False



class SwitchInstance(_BaseSwitchCase[_TCase]):
    def __call__(self, *types: Union[Type, Any]) -> bool:
        self._checkActive()
        if self._check(*types):
            return self._exit()

        return False

    def _check(self, *types):

        return isinstance(self._variable, convert_to_types(types))



class SwitchSubClass(_BaseSwitchCase):
    def __init__(self, variable: Type):
        super().__init__(variable)
    def __call__(self, *types: Type) -> bool:
        self._checkActive()
        if self._check(*types):
            return self._exit()

        return False

    def _check(self, *types: Type): return issubclass(self._variable, convert_to_types(types))
