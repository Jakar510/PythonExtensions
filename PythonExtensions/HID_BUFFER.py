# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------


import time
from typing import *

from .Names import nameof




__all__ = ['HID_BUFFER', 'TimeKeeperMixin']

class TimeKeeperMixin:
    __slots__ = ['_LastTime']
    _LastTime: float
    def __init__(self):
        self._LastTime = time.time()

    def UpdateTime(self): self._LastTime = time.time()

    @property
    def ElapsedTime(self) -> float: return abs(self.CurrentTime - self._LastTime)

    @property
    def CurrentTime(self) -> float: return time.time()



class HID_BUFFER(TimeKeeperMixin):
    __slots__ = ['_text']
    _text: str
    def __init__(self, text: str = ''):
        self._text = text
        super().__init__()


    def Clear(self, s: str = '') -> str:
        if not isinstance(s, str): s = str(s)
        self._text = s
        self.UpdateTime()
        return self._text
    def Add(self, s: str):
        if not isinstance(s, str): s = str(s)
        self._text += s
        self.UpdateTime()
        return self
    def Sub(self, s: str):
        if not isinstance(s, str): s = str(s)
        self._text -= s
        self.UpdateTime()
        return self
    def Backspace(self):
        self._text = self._text[:-1]
        self.UpdateTime()
        return self
    def Backspace_Number(self):
        self.UpdateTime()
        self._text = self._text[:-1]
        if len(self._text) == 0: return self
        if self._text[-1] == '.' or self._text[-1] == ',':
            self._text = self._text[:-2]

        return self


    @property
    def Value(self) -> str: return self._text
    @Value.setter
    def Value(self, v: int or float or str): self._text = str(v)



    def TryReturnAsNumber(self) -> Optional[float]:
        """
            tries to convert to number, if fails returns None.

        :return: Optional[float]
        """
        try: return self.ReturnAsNumber()
        except (ValueError, TypeError): return None
    def ReturnAsNumber(self) -> float:
        """
            Throws ValueError if text is empty.

        :return: float
        """
        self.UpdateTime()
        if not self._text: raise ValueError(f'{nameof(self)}.Value is empty')
        return float(self._text)
    def MultiplyByFactor(self, factor: Union[int, float] = -1) -> float:
        """

            Throws ValueError if text is empty.

        :param factor: the factor the multiply by
        :type factor: Union[int, float]
        :return: float times a factor (default of -1).
        :rtype: float
        """
        return self.ReturnAsNumber() * factor
    def __mul__(self, other: Union[float, int]) -> float: return self.MultiplyByFactor(other)



    def format(self, *args, **kwargs) -> str: return self._text.format(*args, **kwargs)
    def __format__(self, format_spec) -> str: return self._text.__format__(format_spec)
    def __contains__(self, item: str) -> bool: return item in self._text
    def __repr__(self) -> str: return f'<{nameof(self)} Object: "{self._text}">'
    def __str__(self) -> str: return self._text


    def __iadd__(self, char: str): return self.Add(char)
    def __add__(self, char: str): return self.Add(char)

    def __isub__(self, char: str): return self.Sub(char)
    def __sub__(self, char: str): return self.Sub(char)

    def __len__(self) -> int: return len(self._text)


    def __delitem__(self, key: int):
        """ https://www.geeksforgeeks.org/ways-to-remove-ith-character-from-string-in-python/ """
        # if key != len(self):
        #     print('before __delitem__', self)
        #     b = self._text[:key]
        #     a = self._text[key + 1:]
        #     self._text = b + a
        #     PRINT('__delitem__', b=b, a=a, index=key, length=len(self))
        #     print('after __delitem__', self)
        #     return

        try:
            _ = float(self._text)
            self.Backspace_Number()
        except (ValueError, TypeError):
            self.Backspace()

    def __setitem__(self, key: int, value: str):
        """ https://stackoverflow.com/a/41753022/9530917 """
        l = list(self._text)
        l[key] = value
        self._text = ''.join(l)
    def __getitem__(self, key: Union[int, slice]) -> str:
        return self._text.__getitem__(key)
