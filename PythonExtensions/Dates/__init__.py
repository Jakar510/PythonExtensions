from datetime import date as Date, datetime as DateTime, time as Time, tzinfo
from time import time
from typing import *

from attr import attrib, attrs, validators





__all__ = [
    'IsoFormat',
    'time',
    'DateTime', 'Date', 'Time', 'tzinfo',
    ]


@attrs(slots=True, hash=True, order=True, eq=True, auto_attribs=True)
class IsoFormat(object):
    Value: Union[DateTime, Date, Time] = attrib(default=None, validator=validators.instance_of((DateTime, Date, Time)))
    Format: str = attrib(default=None, validator=validators.instance_of(str))
    TimeZoneData: Optional[tzinfo] = attrib(default=None, validator=validators.instance_of(tzinfo))


    def __format__(self, format_spec: Optional[str] = None):
        fmt = format_spec or self.Format
        if not fmt: return str(self)

        return self.Value.strftime(fmt)
    def __str__(self) -> str: return self.Value.isoformat(self.Format)


    @staticmethod
    def ToIsoFormat(dt: Optional[Union[DateTime, Date, Time]]) -> str: return dt.isoformat() if isinstance(dt, (DateTime, Date, Time)) else None


    @staticmethod
    def NowString() -> str: return DateTime.now().isoformat()

    @classmethod
    def Now(cls, tz: tzinfo = None): return cls(DateTime.now(tz))

    @classmethod
    def FromString(cls, _type: Type[Union[DateTime, Date, Time]], obj: str, tz: tzinfo = None): return cls(_type.fromisoformat(obj), TimeZoneData=tz)


    @classmethod
    def FromDateTime(cls, obj: Optional[DateTime], _format: Optional[str], tz: tzinfo = None):
        if obj is None: return None
        return cls(obj, _format, tz)

    @classmethod
    def FromDate(cls, obj: Optional[Date], _format: Optional[str], tz: tzinfo = None):
        if obj is None: return None
        return cls(obj, _format, tz)

    @classmethod
    def FromTime(cls, obj: Optional[Time], _format: Optional[str], tz: tzinfo = None):
        if obj is None: return None
        return cls(obj, _format, tz)
