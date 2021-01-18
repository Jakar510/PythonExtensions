from datetime import date as Date, datetime as DateTime, time as Time, tzinfo
from typing import *




__all__ = [
    'IsoFormat',

    'DateTime', 'Date', 'Time', 'tzinfo',
    ]


class IsoFormat(object):
    _format: str
    _value: Union[DateTime, Date, Time]
    def __init__(self, obj: Union[DateTime, Date, Time], _format: Optional[str] = None, tz: tzinfo = None):
        self.Set(obj)
        self._tz = tz

    def Set(self, obj: Union[DateTime, Date, Time], _format: Optional[str] = None):
        if not isinstance(obj, (DateTime, Date, Time)): raise TypeError(type(obj), (DateTime, Date, Time))
        self._value = obj
        self._format = _format

    def Format(self, fmt: str = None):
        fmt = fmt or self._format
        if not fmt: return self.ToString()

        return self._value.strftime(fmt)
    def ToString(self) -> str: return self._value.isoformat()
    __str__ = ToString

    @staticmethod
    def ToIsoFormat(dt: Optional[Union[DateTime, Date, Time]]) -> str: return dt.isoformat() if isinstance(dt, (DateTime, Date, Time)) else None

    @staticmethod
    def NowString() -> str: return DateTime.now().isoformat()
    @classmethod
    def Now(cls, tz: tzinfo = None): return cls(DateTime.now(tz))
    @classmethod
    def FromString(cls, _type: Type[Union[DateTime, Date, Time]], obj: str, tz: tzinfo = None): return cls(_type.fromisoformat(obj), tz=tz)


    @classmethod
    def FromDateTime(cls, obj: DateTime, _format: Optional[str], tz: tzinfo = None): return cls(obj, _format, tz)
    @classmethod
    def FromDate(cls, obj: Date, _format: Optional[str], tz: tzinfo = None): return cls(obj, _format, tz)
    @classmethod
    def FromTime(cls, obj: Time, _format: Optional[str], tz: tzinfo = None): return cls(obj, _format, tz)


