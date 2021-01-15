import re
from abc import ABC
from typing import Callable, Dict, Tuple

from ..Exceptions import *




__all__ = [
        'SwitchCase', 'CallbackSwitchCase', 'RegexSwitchCase', 'TypeSwitchCase', 'BaseSwitchCase',
        'BreakCase', 'CallBackException', 'ActiveSessionError', 'InvalidRegexObject', 'InactiveSessionError'
        ]


def _to_type(obj: any): return type(obj) if obj.__class__ != type.__class__ else obj
def _convert_to_types(value_to_check: any) -> tuple or type:
    if isinstance(value_to_check, (list, tuple)):
        return tuple(map(BaseSwitchCase._to_type, value_to_check))

    elif value_to_check.__class__ != type.__class__:
        return type(value_to_check)



class CallbackhHandler(object):
    def __init__(self, func: Callable[[Tuple, Dict], bool], *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs) -> bool:
        args = self._args or args
        kwargs = self._kwargs or kwargs
        return self._func(*args, **kwargs)



class BaseSwitchCase(object, ABC):
    """
     variable: the instance to check against.
     regex: the instance to check against.
     regex_pattern: the instance to check against.
     Check_Address: Checks the addresses between variable and the value_to_check, using "is".
     catch_value_to_check: If match is True, added the value_to_check to on_true_args at the start.
     no_match_callback: Optional Method that is called if no match is found or Exception that is raised if no match is found.
     no_match_handler_args (args): no_match_handler's args
     no_match_handler_kwargs (kwargs): no_match_handler's kwargs
    """
    result = None
    _variable: any
    _active: bool = False
    no_match_handler: CallbackhHandler or Exception = None
    def __init__(self, variable: __eq__):
        """
        :param variable: the instance to check against.
        :param no_match_handler_args (args): no_match_handler's args
        :param no_match_handler_kwargs (kwargs): no_match_handler's kwargs
        """
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not a comparable type. {type(variable)}')

        self._variable = variable

    def _get_config(self) -> dict:
        return {
                'variable':          repr(self._variable),
                'no_match_callback': repr(self.no_match_handler),
                }
    def __enter__(self):
        self._active = True
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        if isinstance(exc_val, BreakCase): return True
        if self.no_match_handler is None: return
        if callable(self.no_match_handler): return self.no_match_handler()
        if issubclass(self.no_match_handler, Exception): raise self.no_match_handler() from exc_val
    def _exit(self): raise BreakCase()

    def __setattr__(self, key, value):
        if key not in ['result', '_active'] and self._active: self._raise_active(key, value)
        super().__setattr__(key, value)

    def _raise_inactive(self):
        raise InactiveSessionError(""" Context Manager Must be Used

        For example:

        # value_to_check = one of [ variable OR instance OR type OR tuple of types ]
        with SwitchCase(value_to_check) as sc:
            sc(value_to_search_for)
            ...
        """)
    def _raise_active(self, key, value):
        raise ActiveSessionError(f"""Attributes cannot be changed while context manager is active. 
    key: {key} 
    value: {value} """)

    def _check(self, value_to_check: any, *args, **kwargs) -> bool: raise NotImplementedError()
    def __call__(self, value_to_check: any, *args, **kwargs) -> bool: raise NotImplementedError()



class RegexSwitchCase(BaseSwitchCase):
    _variable: callable
    def __init__(self, regex: re.Pattern, method: str):
        """
        :param regex: the instance to check against.
        """
        if not method in dir(regex): raise ValueError('method must be a callable function of the regex object.')
        self._variable = getattr(regex, method)
        if not callable(self._variable): raise TypeError('regex.method is not callble')

    def __call__(self, value_to_check: any) -> bool:
        if not self._active: self._raise_inactive()
        return self.__regex__(value_to_check)
    def __regex__(self, value_to_check: str) -> bool:  # TODO: implement regex parsing for the value_to_check
        if not isinstance(value_to_check, str): return False

        return self._variable(value_to_check) is not None



class SwitchCase(BaseSwitchCase):
    def __init__(self, variable: __eq__):
        """
        :param variable: the instance to check against.
        """
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not a comparable type. {type(variable)}')

        self._variable = variable

    def __call__(self, value_to_check: any) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(value_to_check): self._exit()
        return False

    def _check(self, value_to_check): return self._variable == value_to_check



class CallbackSwitchCase(BaseSwitchCase):
    def __init__(self, variable: __eq__):
        """
        :param variable: the instance to check against.
        """
        if not hasattr(variable, '__eq__'): raise ValueError(f'variable is not a comparable type. {type(variable)}')

        self._variable = variable

    def __call__(self, value_to_check: any, callback: CallbackhHandler = None) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(value_to_check):
            callback()
            self._exit()

        return False

    def _check(self, value_to_check): return self._variable == value_to_check



class InstanceSwitchCase(BaseSwitchCase):
    def __init__(self, variable: __eq__):
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not comparable type. {type(variable)}')

        self._variable = variable
    def __call__(self, *types: type) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(*types): self._exit()
        return False

    def _check(self, *types): return isinstance(self._variable, types)



class TypeSwitchCase(BaseSwitchCase):
    def __init__(self, variable: type):
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not comparable type. {type(variable)}')

        self._variable = variable
    def __call__(self, *types: type) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(*types): self._exit()
        return False

    def _check(self, *types): return issubclass(self._variable, types)
