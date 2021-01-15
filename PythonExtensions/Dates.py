from datetime import date, datetime, time
from typing import *




__all__ = [
        'DateTime_ToString', 'ToIsoFormat', 'FromIsoFormat', 'now'
        ]

def DateTime_ToString(dt: Optional[Union[datetime, date, time]], _format: str) -> str or None:
    return dt.strftime(_format) if dt is not None else None
def ToIsoFormat(dt: Optional[Union[datetime, date, time]]) -> str:
    return dt.isoformat() if isinstance(dt, (datetime, date, time)) else None
def FromIsoFormat(dt: Type[Union[datetime, date, time]], value: str) -> Optional[Union[datetime, date, time]]:
    return dt.fromisoformat(value) if isinstance(value, str) else None
def now() -> str: return datetime.now().isoformat()
