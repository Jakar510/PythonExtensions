from json import loads as _loads
from typing import *

from .Base import *
from .Common import *




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

    # def __deepcopy__(self): return super(BaseDictModel, self).__deepcopy__()
    def __delitem__(self, item: KeyCollection): return super().__delitem__(item)
    def __contains__(self, item: KeyCollection): return super().__contains__(item)
    def __setitem__(self, key: KeyCollection, value: _VT): return super().__setitem__(key, value)
    def __getitem__(self, key: KeyCollection) -> _VT: return super().__getitem__(key)
    def __iter__(self) -> Iterable[KeyCollection]: return super().__iter__()
    def enumerate(self) -> Iterable[Tuple[int, KeyCollection]]: return enumerate(self)
    

    @property
    def Count(self) -> int: return len(self)
    @property
    def Empty(self) -> bool: return self.Count == 0
    def __bool__(self): return not self.Empty

    def _Filter(self, func: callable) -> List[KeyCollection]: return list(filter(func, self.values()))

    def items(self) -> Iterable[Tuple[KeyCollection, _VT]]: return list(self.items())
    def ToList(self) -> List[Tuple[KeyCollection, _VT]]: return list(self.items())
    def ToDict(self) -> Dict[KeyCollection, Union[KeyCollection, Dict, str]]: return self._ToDict({ k.ToJsonString(): v for k, v in self.items() })

    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            return cls({ KeyCollection.FromString(k): v for k, v in d.items() })

        throw(d, dict)

    @classmethod
    def FromJson(cls, string: Union[str, bytes, bytearray], **kwargs): return cls.Parse(_loads(string, **kwargs))
