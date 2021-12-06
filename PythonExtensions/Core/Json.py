import copy as _copy
import re
from datetime import datetime, time, timedelta
from enum import Enum
from json import dumps as _dumps, loads as _loads
from typing import *

from dateutil import parser

from .Names import nameof, typeof




__all__ = ['BaseObjectModel',
           'BaseDictModel',
           'BaseSetModel',
           'BaseListModel',
           'Assert',
           'throw',
           'AssertKeys',
           'AssertType',
           'ConvertBool',
           'RaiseKeyError',
           ]


@overload
def Assert(d: Any, t: Type): ...
@overload
def Assert(d: Any, *types: Type): ...
def Assert(d: Any, *t: type):
    if not isinstance(d, t): throw(d, *t)



@overload
def throw(d: Any, t: Type): ...
@overload
def throw(d: Any, *types: Type): ...
def throw(d: Any, *types: Type):
    if not types:
        raise ValueError('expected types must be provided')

    if len(types) == 1:
        raise TypeError(f'Expecting {types[0]}   got type {typeof(d)}')

    raise TypeError(f'Expecting one of {types}   got type {typeof(d)}')



def AssertKeys(d: Dict, *args):
    for key in args:
        if key not in d: RaiseKeyError(key, d)


def AssertType(cls: Type, *args: Type):
    if not (issubclass(cls, args)): raise TypeError(type(cls), args)

def ConvertBool(o: Union[bool, str]) -> bool:
    if isinstance(o, bool): return o
    if isinstance(o, str): return o.strip().lower() == 'true'

    throw(o, bool, str)



def RaiseKeyError(key, d: Dict): raise KeyError(f'{key} not in {d.keys()}')



_regex = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

class BaseObjectModel(object):
    def Clone(self):
        return _copy.deepcopy(self)

    @property
    def __class_name__(self) -> str:
        return nameof(self)

    def ToString(self) -> str:
        return f'<{self.__class_name__} Object() {self.ToJsonString()}>'
    def ToJsonString(self, indent: int = 4) -> str:
        return _dumps(self, indent=indent, default=self._serialize)

    def __str__(self):
        return self.ToJsonString()


    @staticmethod
    def _ToDict(o: Dict) -> Dict[_KT, Union[_VT, Dict, str]]:
        d = { }
        for key, value in o.items():
            if isinstance(value, Enum):
                d[key] = value.value

            elif isinstance(value, BaseListModel):
                d[key] = value

            elif isinstance(value, BaseSetModel):
                d[key] = value.ToList()

            elif isinstance(value, BaseDictModel):
                d[key] = value.ToDict()

            elif hasattr(value, 'ToList') and callable(value.ToList):
                d[key] = value.ToList()

            elif hasattr(value, 'ToTuple') and callable(value.ToTuple):
                d[key] = value.ToTuple()

            elif hasattr(value, 'ToDict') and callable(value.ToDict):
                d[key] = value.ToDict()

            elif hasattr(value, 'ToString') and callable(value.ToString):
                d[key] = value.ToString()

            else:
                d[key] = value
        return d


    def Filter(self, func: callable):
        raise NotImplementedError()
    def enumerate(self):
        raise NotImplementedError()
    def __iter__(self):
        raise NotImplementedError()
    def __len__(self) -> int:
        raise NotImplementedError()


    @property
    def Count(self) -> int:
        return len(self)
    @property
    def Empty(self) -> bool:
        return self.Count == 0
    def __bool__(self):
        return not self.Empty


    @classmethod
    def Parse(cls, d):
        raise NotImplementedError()

    @classmethod
    def FromJson(cls, string: Union[str, bytes, bytearray], **kwargs):
        raise NotImplementedError()



    @staticmethod
    def _serialize(obj):
        if isinstance(obj, Enum): return obj.value

        if isinstance(obj, time): return obj.isoformat()

        if isinstance(obj, datetime): return obj.isoformat()

        if isinstance(obj, timedelta): return obj.total_seconds()

        if isinstance(obj, BaseSetModel): return obj.ToList()

        if isinstance(obj, BaseListModel): return obj

        if isinstance(obj, BaseDictModel): return obj.ToDict()

        if hasattr(obj, 'ToList') and callable(obj.ToList): return obj.ToList()

        if hasattr(obj, 'ToTuple') and callable(obj.ToTuple): return obj.ToTuple()

        if hasattr(obj, 'ToDict') and callable(obj.ToDict): return obj.ToDict()

        return obj


    @staticmethod
    def convert_time(value: Union[int, float, timedelta, str], default: Union[time, Type[Exception]] = None) -> Optional[time]:
        if isinstance(value, str): return BaseObjectModel.parse_time(value)

        if isinstance(value, time): return value

        if isinstance(value, int): return time(hour=value)

        if isinstance(value, float):
            hours = int(value)
            return time(hour=hours % 24, minute=int((value - hours) * 60))

        if issubclass(default, TypeError):
            raise default(typeof(value), (int, float, time, str))

        if issubclass(default, Exception):
            raise default

        return default

    @staticmethod
    def convert_date_time(value: Union[datetime, str], default: Union[datetime, Type[Exception]] = None) -> Optional[datetime]:
        if isinstance(value, str): return BaseObjectModel.parse_date_time(value)

        if isinstance(value, datetime): return value

        if issubclass(default, TypeError):
            raise default(typeof(value), (datetime, str))

        if issubclass(default, Exception):
            raise default

        return default


    @staticmethod
    def convert_time_delta(value: Union[int, float, timedelta, str], default: Union[timedelta, Type[Exception]] = None) -> Optional[timedelta]:
        if isinstance(value, str): return BaseObjectModel.parse_time_delta(value)

        if isinstance(value, timedelta): return value

        if isinstance(value, int): return timedelta(seconds=value)

        if isinstance(value, float):
            seconds = int(value)
            return timedelta(seconds=seconds, microseconds=value - seconds)

        if issubclass(default, TypeError):
            raise default(typeof(value), (int, float, timedelta, str))

        if issubclass(default, Exception):
            raise default

        return default


    @staticmethod
    def parse_time_delta(value: str) -> Optional[timedelta]:
        if value == str(None):
            return None

        try:
            seconds = int(value)
            return timedelta(seconds=seconds)
        except ValueError:
            parts = _regex.match(value)
            if not parts:
                return None

            parts = parts.groupdict()
            time_params = { }
            for name, param in parts.items():
                if param:
                    time_params[name] = int(param)
            return timedelta(**time_params)

    @staticmethod
    def parse_time(value: str) -> Optional[time]:
        if value == str(None):
            return None

        try:
            return time.fromisoformat(value)
        except ValueError:
            return parser.parse(value).time()

    @staticmethod
    def parse_date_time(value: str) -> Optional[datetime]:
        if value == str(None):
            return None

        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return parser.parse(value)



class BaseListModel(list, BaseObjectModel, List[_T]):
    def __init__(self, source: Union[List, Iterable] = None):
        super().__init__(source or [])

    # def __iter__(self) -> Iterable[_T]: return super().__iter__()
    # def __contains__(self, item: _T): return super().__contains__(item)
    # def __setitem__(self, key: int, value: _T): return super().__setitem__(key, value)
    def __getitem__(self, key: int) -> Optional[_T]:
        try:
            return super().__getitem__(key)
        except KeyError:
            return None

    def enumerate(self) -> Iterable[Tuple[int, _T]]:
        return enumerate(self)
    def Iter(self) -> Iterable[int]:
        return range(len(self))


    def Filter(self, func: callable) -> List[_T]:
        return list(filter(func, self))
    def ToDict(self) -> Dict[int, _T]:
        return dict(self.enumerate())


    @classmethod
    def Parse(cls, d):
        if isinstance(d, list):
            return cls(d)

        throw(d, list)

    @classmethod
    def Create(cls, *args: _T):
        return cls(args)

    @classmethod
    def FromJson(cls, string: Union[str, bytes, bytearray], **kwargs):
        return cls.Parse(_loads(string, **kwargs))



class BaseSetModel(set, BaseObjectModel, Set[_T]):
    # def __contains__(self, item: _T): return super().__contains__(item)
    # def __delitem__(self, item: _T): return self.discard(item)
    # def __isub__(self, item: _T): return self.discard(item)
    # def __iadd__(self, item: _T): return self.add(item)
    # def __iter__(self) -> Iterable[_T]: return super().__iter__()

    def enumerate(self) -> Iterable[Tuple[int, _T]]: return enumerate(self)
    def ToDict(self) -> Dict[int, _T]: return dict(self.enumerate())
    def ToList(self) -> List[_T]: return list(self)

    def Filter(self, func: callable): return filter(func, self)
    def extend(self, items: Union[List[_T], Set[_T]]): return self.update(items)




    @staticmethod
    def FromArgs(*items: _T): return BaseSetModel.Parse(items)

    @classmethod
    def Parse(cls, d):
        if isinstance(d, list):
            return cls(d)

        throw(d, list)

    @classmethod
    def Create(cls, *args: _T): return cls(args)

    @classmethod
    def FromJson(cls, string: Union[str, bytes, bytearray], **kwargs): return cls.Parse(_loads(string, **kwargs))



class BaseDictModel(dict, BaseObjectModel, Dict[_KT, _VT]):
    def __init__(self, source: dict = None, **kwargs):
        if source is not None:
            super().__init__(source, **kwargs)
        else:
            super().__init__(**kwargs)


    # def __deepcopy__(self): return super(BaseDictModel, self).__deepcopy__()
    # def __delitem__(self, item: Union[_KT, _VT]): return super().__delitem__(item)
    # def __contains__(self, item: Union[_KT, _VT]): return super().__contains__(item)
    # def __setitem__(self, key: _KT, value: _VT): return super().__setitem__(key, value)
    # def __getitem__(self, key: _KT) -> _VT: return super().__getitem__(key)
    # def __iter__(self) -> Iterable[_KT]: return super().__iter__()
    # def values(self) -> Iterable[_VT]: return super().values()
    # def items(self) -> Iterable[Tuple[_KT, _VT]]: return super().items()
    # def keys(self) -> Iterable[_KT]: return super().keys()

    def enumerate(self) -> Iterable[Tuple[int, _KT]]:
        return enumerate(self)


    def Filter(self, func: callable) -> List[_VT]:
        return list(filter(func, self.values()))

    def ToList(self) -> List[Tuple[_KT, _VT]]:
        return list(self.items())
    def ToDict(self) -> Dict[_KT, Union[_VT, Dict, str]]:
        return self._ToDict(self)


    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            return cls(d)

        throw(d, dict)

    @classmethod
    def Create(cls, **kwargs: _VT):
        return cls(kwargs)

    @classmethod
    def FromJson(cls, string: Union[str, bytes, bytearray], **kwargs):
        return cls.Parse(_loads(string, **kwargs))
