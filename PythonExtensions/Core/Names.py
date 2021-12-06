from typing import *




__all__ = ['class_name', 'nameof', 'typeof', 'convert_to_types']

def class_name(obj) -> str:
    if isinstance(obj, type):
        return obj.__name__

    return obj.__class__.__name__

def nameof(obj: Union[Callable, property, object]) -> str:
    if not hasattr(obj, '__module__'):
        if hasattr(obj, '__qualname__'):
            mod = obj.__qualname__
        elif hasattr(obj, '__name__'):
            mod = obj.__name__
        else:
            mod = class_name(obj)
    else:
        mod = obj.__module__

    try:
        name = obj.__qualname__
    except AttributeError:
        try:
            name = obj.__name__
        except AttributeError:
            name = class_name(obj)

    return f'{mod}.{name}'


def typeof(obj) -> Type:
    if isinstance(obj, type):
        return obj

    return type(obj)

def convert_to_types(value_to_check) -> Union[Tuple[Type, ...], Type]:
    if isinstance(value_to_check, (list, tuple)):
        return tuple(map(typeof, value_to_check))

    return typeof(value_to_check)
