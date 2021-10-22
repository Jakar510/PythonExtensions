from json import loads as _loads
from typing import *

from Json import *




__all__ = ['BaseMultiDictModel', 'KeyCollection']

_Default = TypeVar("_Default")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class KeyCollection(BaseListModel[Hashable]):
    def __hash__(self): return hash(tuple(self))
    def __contains__(self, item: Hashable): return super().__contains__(item)

    @classmethod
    def FromString(cls, s: str):
        if isinstance(s, str):
            return cls.FromJson(s)

        throw(s, str)



class BaseMultiDictModel(dict, BaseObjectModel, Dict[KeyCollection, _VT]):
    def __init__(self, source: Dict[KeyCollection, _VT] = None, **kwargs: _VT):
        if source is not None: super().__init__(source, **kwargs)
        else: super().__init__(**kwargs)

    # def __deepcopy__(self): return super().__deepcopy__()
    def __delitem__(self, item: Union[Hashable, KeyCollection]):
        if isinstance(item, KeyCollection): return super().__delitem__(item)

        for x in self.keys():
            if item in x: return True

        return False
    def __contains__(self, item: Union[Hashable, KeyCollection]) -> bool:
        if isinstance(item, KeyCollection): return super().__contains__(item)

        return any(item in x for x in self.keys())

    def __setitem__(self, key: Union[Hashable, KeyCollection], value: _VT):
        if key in self:
            if isinstance(key, KeyCollection): return super().__setitem__(key, value)

        for k, v in self.items():
            if value == v:

                return

    def __getitem__(self, item: Hashable):
        pass

    def enumerate(self) -> Iterable[Tuple[int, KeyCollection]]: return enumerate(self)


    @property
    def Count(self) -> int: return len(self)
    @property
    def Empty(self) -> bool: return self.Count == 0
    def __bool__(self): return not self.Empty


    def Filter(self, func: callable) -> List[KeyCollection]: return list(filter(func, self.values()))


    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            return cls({ KeyCollection.FromString(k): v for k, v in d.items() })

        throw(d, dict)

    @classmethod
    def FromJson(cls, string: Union[str, bytes, bytearray], **kwargs): return cls.Parse(_loads(string, **kwargs))
