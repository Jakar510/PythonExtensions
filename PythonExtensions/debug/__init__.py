from .chains import *
from .console import *
from .converters import *
from .decorators import *
from .debug_tk import *



def nameof(obj) -> str:
    if not hasattr(obj, '__module__'):
        if hasattr(obj, '__qualname__'):
            obj = obj.__qualname__
        elif hasattr(obj, '__name__'):
            obj = obj.__name__
        else:
            obj = obj.__class__

    mod = obj.__module__
    try:
        return f'{mod}.{obj.__qualname__}'
    except AttributeError:
        try:
            return f'{mod}.{obj.__name__}'
        except AttributeError:
            return f'{mod}.{obj.__class__.__name__}'
