import re

__all__ = ['IsAttributePrivate', 'ObjectToDict']


private_or_special_function_searcher = re.compile(r"(^__\w+$)|(^_\w+$)|(^__\w+__$)")
def IsAttributePrivate(attr_name: str) -> bool:
    return private_or_special_function_searcher.search(attr_name) is not None


def ObjectToDict(Object: any, Skip: list or tuple = (), *, ShowAll: bool = False, IncludeCallable: bool = False) -> dict:
    """
        Returns a dictionary of the public attributes of the given object provided;
        Filter out private or special functions (_private, __SuperPrivate, __special__).

    :param IncludeCallable: doesn't include functions by default.
    :param ShowAll: remove all filters and show entire object.
    :param Skip:  list of names to skip. i.e. certain method names when IncludeCallable is True.
    :param Object: the thing being inspected.
    :return:
    """
    temp = {}
    for key in dir(Object):
        if key in Skip: continue
        if ShowAll or IsAttributePrivate(key):
            temp[key] = getattr(Object, key)
            if IncludeCallable and callable(temp[key]):
                del temp[key]
    return temp

