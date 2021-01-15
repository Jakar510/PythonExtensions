# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------


import time
from typing import *




__all__ = ['HID_BUFFER', 'TimeKeeperMixin']

class TimeKeeperMixin:
    _LastTime = time.time()
    def UpdateTime(self): self._LastTime = time.time()

    @property
    def ElapsedTime(self) -> float: return abs(self.CurrentTime - self._LastTime)

    @property
    def CurrentTime(self) -> float: return time.time()


# class str(object):
#     """
#     str(object='') -> str
#     str(bytes_or_buffer[, encoding[, errors]]) -> str
#
#     Create a new string object from the given object. If encoding or
#     errors is specified, then the object must expose a data buffer
#     that will be decoded using the given encoding and error handler.
#     Otherwise, returns the result of object.__str__() (if defined)
#     or repr(object).
#     encoding defaults to sys.getdefaultencoding().
#     errors defaults to 'strict'.
#     """
#     def capitalize(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a capitalized version of the string.
#
#         More specifically, make the first character have upper case and the rest lower
#         case.
#         """
#         pass
#
#     def casefold(self, *args, **kwargs):  # real signature unknown
#         """ Return a version of the string suitable for caseless comparisons. """
#         pass
#
#     def center(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a centered string of length width.
#
#         Padding is done using the specified fill character (default is a space).
#         """
#         pass
#
#     def count(self, sub, start=None, end=None):  # real signature unknown; restored from __doc__
#         """
#         S.count(sub[, start[, end]]) -> int
#
#         Return the number of non-overlapping occurrences of substring sub in
#         string S[start:end].  Optional arguments start and end are
#         interpreted as in slice notation.
#         """
#         return 0
#
#     def encode(self, *args, **kwargs):  # real signature unknown
#         """
#         Encode the string using the codec registered for encoding.
#
#           encoding
#             The encoding in which to encode the string.
#           errors
#             The error handling scheme to use for encoding errors.
#             The default is 'strict' meaning that encoding errors raise a
#             UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
#             'xmlcharrefreplace' as well as any other name registered with
#             codecs.register_error that can handle UnicodeEncodeErrors.
#         """
#         pass
#
#     def endswith(self, suffix, start=None, end=None):  # real signature unknown; restored from __doc__
#         """
#         S.endswith(suffix[, start[, end]]) -> bool
#
#         Return True if S ends with the specified suffix, False otherwise.
#         With optional start, test S beginning at that position.
#         With optional end, stop comparing S at that position.
#         suffix can also be a tuple of strings to try.
#         """
#         return False
#
#     def expandtabs(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a copy where all tab characters are expanded using spaces.
#
#         If tabsize is not given, a tab size of 8 characters is assumed.
#         """
#         pass
#
#     def find(self, sub, start=None, end=None):  # real signature unknown; restored from __doc__
#         """
#         S.find(sub[, start[, end]]) -> int
#
#         Return the lowest index in S where substring sub is found,
#         such that sub is contained within S[start:end].  Optional
#         arguments start and end are interpreted as in slice notation.
#
#         Return -1 on failure.
#         """
#         return 0
#
#     def format(self, *args, **kwargs):  # known special case of str.format
#         """
#         S.format(*args, **kwargs) -> str
#
#         Return a formatted version of S, using substitutions from args and kwargs.
#         The substitutions are identified by braces ('{' and '}').
#         """
#         pass
#
#     def format_map(self, mapping):  # real signature unknown; restored from __doc__
#         """
#         S.format_map(mapping) -> str
#
#         Return a formatted version of S, using substitutions from mapping.
#         The substitutions are identified by braces ('{' and '}').
#         """
#         return ""
#
#     def index(self, sub, start=None, end=None):  # real signature unknown; restored from __doc__
#         """
#         S.index(sub[, start[, end]]) -> int
#
#         Return the lowest index in S where substring sub is found,
#         such that sub is contained within S[start:end].  Optional
#         arguments start and end are interpreted as in slice notation.
#
#         Raises ValueError when the substring is not found.
#         """
#         return 0
#
#     def isalnum(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is an alpha-numeric string, False otherwise.
#
#         A string is alpha-numeric if all characters in the string are alpha-numeric and
#         there is at least one character in the string.
#         """
#         pass
#
#     def isalpha(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is an alphabetic string, False otherwise.
#
#         A string is alphabetic if all characters in the string are alphabetic and there
#         is at least one character in the string.
#         """
#         pass
#
#     def isascii(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if all characters in the string are ASCII, False otherwise.
#
#         ASCII characters have code points in the range U+0000-U+007F.
#         Empty string is ASCII too.
#         """
#         pass
#
#     def isdecimal(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is a decimal string, False otherwise.
#
#         A string is a decimal string if all characters in the string are decimal and
#         there is at least one character in the string.
#         """
#         pass
#
#     def isdigit(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is a digit string, False otherwise.
#
#         A string is a digit string if all characters in the string are digits and there
#         is at least one character in the string.
#         """
#         pass
#
#     def isidentifier(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is a valid Python identifier, False otherwise.
#
#         Call keyword.iskeyword(s) to test whether string s is a reserved identifier,
#         such as "def" or "class".
#         """
#         pass
#
#     def islower(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is a lowercase string, False otherwise.
#
#         A string is lowercase if all cased characters in the string are lowercase and
#         there is at least one cased character in the string.
#         """
#         pass
#
#     def isnumeric(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is a numeric string, False otherwise.
#
#         A string is numeric if all characters in the string are numeric and there is at
#         least one character in the string.
#         """
#         pass
#
#     def isprintable(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is printable, False otherwise.
#
#         A string is printable if all of its characters are considered printable in
#         repr() or if it is empty.
#         """
#         pass
#
#     def isspace(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is a whitespace string, False otherwise.
#
#         A string is whitespace if all characters in the string are whitespace and there
#         is at least one character in the string.
#         """
#         pass
#
#     def istitle(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is a title-cased string, False otherwise.
#
#         In a title-cased string, upper- and title-case characters may only
#         follow uncased characters and lowercase characters only cased ones.
#         """
#         pass
#
#     def isupper(self, *args, **kwargs):  # real signature unknown
#         """
#         Return True if the string is an uppercase string, False otherwise.
#
#         A string is uppercase if all cased characters in the string are uppercase and
#         there is at least one cased character in the string.
#         """
#         pass
#
#     def join(self, ab=None, pq=None, rs=None):  # real signature unknown; restored from __doc__
#         """
#         Concatenate any number of strings.
#
#         The string whose method is called is inserted in between each given string.
#         The result is returned as a new string.
#
#         Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
#         """
#         pass
#
#     def ljust(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a left-justified string of length width.
#
#         Padding is done using the specified fill character (default is a space).
#         """
#         pass
#
#     def lower(self, *args, **kwargs):  # real signature unknown
#         """ Return a copy of the string converted to lowercase. """
#         pass
#
#     def lstrip(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a copy of the string with leading whitespace removed.
#
#         If chars is given and not None, remove characters in chars instead.
#         """
#         pass
#
#     def maketrans(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a translation table usable for str.translate().
#
#         If there is only one argument, it must be a dictionary mapping Unicode
#         ordinals (integers) or characters to Unicode ordinals, strings or None.
#         Character keys will be then converted to ordinals.
#         If there are two arguments, they must be strings of equal length, and
#         in the resulting dictionary, each character in x will be mapped to the
#         character at the same position in y. If there is a third argument, it
#         must be a string, whose characters will be mapped to None in the result.
#         """
#         pass
#
#     def partition(self, *args, **kwargs):  # real signature unknown
#         """
#         Partition the string into three parts using the given separator.
#
#         This will search for the separator in the string.  If the separator is found,
#         returns a 3-tuple containing the part before the separator, the separator
#         itself, and the part after it.
#
#         If the separator is not found, returns a 3-tuple containing the original string
#         and two empty strings.
#         """
#         pass
#
#     def removeprefix(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a str with the given prefix string removed if present.
#
#         If the string starts with the prefix string, return string[len(prefix):].
#         Otherwise, return a copy of the original string.
#         """
#         pass
#
#     def removesuffix(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a str with the given suffix string removed if present.
#
#         If the string ends with the suffix string and that suffix is not empty,
#         return string[:-len(suffix)]. Otherwise, return a copy of the original
#         string.
#         """
#         pass
#
#     def replace(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a copy with all occurrences of substring old replaced by new.
#
#           count
#             Maximum number of occurrences to replace.
#             -1 (the default value) means replace all occurrences.
#
#         If the optional argument count is given, only the first count occurrences are
#         replaced.
#         """
#         pass
#
#     def rfind(self, sub, start=None, end=None):  # real signature unknown; restored from __doc__
#         """
#         S.rfind(sub[, start[, end]]) -> int
#
#         Return the highest index in S where substring sub is found,
#         such that sub is contained within S[start:end].  Optional
#         arguments start and end are interpreted as in slice notation.
#
#         Return -1 on failure.
#         """
#         return 0
#
#     def rindex(self, sub, start=None, end=None):  # real signature unknown; restored from __doc__
#         """
#         S.rindex(sub[, start[, end]]) -> int
#
#         Return the highest index in S where substring sub is found,
#         such that sub is contained within S[start:end].  Optional
#         arguments start and end are interpreted as in slice notation.
#
#         Raises ValueError when the substring is not found.
#         """
#         return 0
#
#     def rjust(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a right-justified string of length width.
#
#         Padding is done using the specified fill character (default is a space).
#         """
#         pass
#
#     def rpartition(self, *args, **kwargs):  # real signature unknown
#         """
#         Partition the string into three parts using the given separator.
#
#         This will search for the separator in the string, starting at the end. If
#         the separator is found, returns a 3-tuple containing the part before the
#         separator, the separator itself, and the part after it.
#
#         If the separator is not found, returns a 3-tuple containing two empty strings
#         and the original string.
#         """
#         pass
#
#     def rsplit(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a list of the words in the string, using sep as the delimiter string.
#
#           sep
#             The delimiter according which to split the string.
#             None (the default value) means split according to any whitespace,
#             and discard empty strings from the result.
#           maxsplit
#             Maximum number of splits to do.
#             -1 (the default value) means no limit.
#
#         Splits are done starting at the end of the string and working to the front.
#         """
#         pass
#
#     def rstrip(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a copy of the string with trailing whitespace removed.
#
#         If chars is given and not None, remove characters in chars instead.
#         """
#         pass
#
#     def split(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a list of the words in the string, using sep as the delimiter string.
#
#           sep
#             The delimiter according which to split the string.
#             None (the default value) means split according to any whitespace,
#             and discard empty strings from the result.
#           maxsplit
#             Maximum number of splits to do.
#             -1 (the default value) means no limit.
#         """
#         pass
#
#     def splitlines(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a list of the lines in the string, breaking at line boundaries.
#
#         Line breaks are not included in the resulting list unless keepends is given and
#         true.
#         """
#         pass
#
#     def startswith(self, prefix, start=None, end=None):  # real signature unknown; restored from __doc__
#         """
#         S.startswith(prefix[, start[, end]]) -> bool
#
#         Return True if S starts with the specified prefix, False otherwise.
#         With optional start, test S beginning at that position.
#         With optional end, stop comparing S at that position.
#         prefix can also be a tuple of strings to try.
#         """
#         return False
#
#     def strip(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a copy of the string with leading and trailing whitespace removed.
#
#         If chars is given and not None, remove characters in chars instead.
#         """
#         pass
#
#     def swapcase(self, *args, **kwargs):  # real signature unknown
#         """ Convert uppercase characters to lowercase and lowercase characters to uppercase. """
#         pass
#
#     def title(self, *args, **kwargs):  # real signature unknown
#         """
#         Return a version of the string where each word is titlecased.
#
#         More specifically, words start with uppercased characters and all remaining
#         cased characters have lower case.
#         """
#         pass
#
#     def translate(self, *args, **kwargs):  # real signature unknown
#         """
#         Replace each character in the string using the given translation table.
#
#           table
#             Translation table, which must be a mapping of Unicode ordinals to
#             Unicode ordinals, strings, or None.
#
#         The table must implement lookup/indexing via __getitem__, for instance a
#         dictionary or list.  If this operation raises LookupError, the character is
#         left untouched.  Characters mapped to None are deleted.
#         """
#         pass
#
#     def upper(self, *args, **kwargs):  # real signature unknown
#         """ Return a copy of the string converted to uppercase. """
#         pass
#
#     def zfill(self, *args, **kwargs):  # real signature unknown
#         """
#         Pad a numeric string with zeros on the left, to fill a field of the given width.
#
#         The string is never truncated.
#         """
#         pass
#
#     def __add__(self, *args, **kwargs):  # real signature unknown
#         """ Return self+value. """
#         pass
#
#     def __contains__(self, *args, **kwargs):  # real signature unknown
#         """ Return key in self. """
#         pass
#
#     def __eq__(self, *args, **kwargs):  # real signature unknown
#         """ Return self==value. """
#         pass
#
#     def __format__(self, *args, **kwargs):  # real signature unknown
#         """ Return a formatted version of the string as described by format_spec. """
#         pass
#
#     def __getattribute__(self, *args, **kwargs):  # real signature unknown
#         """ Return getattr(self, name). """
#         pass
#
#     def __getitem__(self, *args, **kwargs):  # real signature unknown
#         """ Return self[key]. """
#         pass
#
#     def __getnewargs__(self, *args, **kwargs):  # real signature unknown
#         pass
#
#     def __ge__(self, *args, **kwargs):  # real signature unknown
#         """ Return self>=value. """
#         pass
#
#     def __gt__(self, *args, **kwargs):  # real signature unknown
#         """ Return self>value. """
#         pass
#
#     def __hash__(self, *args, **kwargs):  # real signature unknown
#         """ Return hash(self). """
#         pass
#
#     def __init__(self, value='', encoding=None, errors='strict'):  # known special case of str.__init__
#         """
#         str(object='') -> str
#         str(bytes_or_buffer[, encoding[, errors]]) -> str
#
#         Create a new string object from the given object. If encoding or
#         errors is specified, then the object must expose a data buffer
#         that will be decoded using the given encoding and error handler.
#         Otherwise, returns the result of object.__str__() (if defined)
#         or repr(object).
#         encoding defaults to sys.getdefaultencoding().
#         errors defaults to 'strict'.
#         # (copied from class doc)
#         """
#         pass
#
#     def __iter__(self, *args, **kwargs):  # real signature unknown
#         """ Implement iter(self). """
#         pass
#
#     def __len__(self, *args, **kwargs):  # real signature unknown
#         """ Return len(self). """
#         pass
#
#     def __le__(self, *args, **kwargs):  # real signature unknown
#         """ Return self<=value. """
#         pass
#
#     def __lt__(self, *args, **kwargs):  # real signature unknown
#         """ Return self<value. """
#         pass
#
#     def __mod__(self, *args, **kwargs):  # real signature unknown
#         """ Return self%value. """
#         pass
#
#     def __mul__(self, *args, **kwargs):  # real signature unknown
#         """ Return self*value. """
#         pass
#
#     @staticmethod  # known case of __new__
#     def __new__(*args, **kwargs):  # real signature unknown
#         """ Create and return a new object.  See help(type) for accurate signature. """
#         pass
#
#     def __ne__(self, *args, **kwargs):  # real signature unknown
#         """ Return self!=value. """
#         pass
#
#     def __repr__(self, *args, **kwargs):  # real signature unknown
#         """ Return repr(self). """
#         pass
#
#     def __rmod__(self, *args, **kwargs):  # real signature unknown
#         """ Return value%self. """
#         pass
#
#     def __rmul__(self, *args, **kwargs):  # real signature unknown
#         """ Return value*self. """
#         pass
#
#     def __sizeof__(self, *args, **kwargs):  # real signature unknown
#         """ Return the size of the string in memory, in bytes. """
#         pass
#
#     def __str__(self, *args, **kwargs):  # real signature unknown
#         """ Return str(self). """
#         pass


class HID_BUFFER(TimeKeeperMixin):
    __all__ = []
    _text: str = ''
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
        if not self._text: raise ValueError(f'{self.__class__.__name__}.Value is empty')
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
    def __repr__(self) -> str: return f'<{self.__class__.__name__} Object: "{self._text}">'
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
        l = tuple(self._text)
        l[key] = value
        self._text = ''.join(l)
    def __getitem__(self, key: Union[int, slice]) -> str:
        return self._text.__getitem__(key)



# class HID_BUFFER_NUMBER(float, HID_BUFFER):
#     def __abs__(self, *args, **kwargs):
#         pass
#
#     def __add__(self, *args, **kwargs):
#         pass
#
#     def __bool__(self, *args, **kwargs):
#         pass
#
#     def __ceil__(self, *args, **kwargs):
#         pass
#
#     def __divmod__(self, *args, **kwargs):
#         pass
#
#     def __eq__(self, *args, **kwargs):
#         pass
#
#     def __float__(self, *args, **kwargs):
#         pass
#
#     def __floordiv__(self, *args, **kwargs):
#         pass
#
#     def __floor__(self, *args, **kwargs):
#         pass
#
#     def __format__(self, *args, **kwargs):
#         pass
#
#     def __getformat__(self, *args, **kwargs):
#         pass
#
#     def __getnewargs__(self, *args, **kwargs):  # real signature unknown
#
#         pass
#
#     def __ge__(self, *args, **kwargs):
#         pass
#
#     def __gt__(self, *args, **kwargs):
#         pass
#
#     def __hash__(self, *args, **kwargs):
#         pass
#
#     def __init__(self):
#         super(HID_BUFFER_NUMBER, self).__init__()
#         HID_BUFFER.__init__(self)
#
#     def __int__(self, *args, **kwargs):
#         pass
#
#     def __le__(self, *args, **kwargs):
#         pass
#
#     def __lt__(self, *args, **kwargs):
#         pass
#
#     def __mod__(self, *args, **kwargs):
#         pass
#
#     def __mul__(self, *args, **kwargs):
#         pass
#
#     def __neg__(self, *args, **kwargs):
#         pass
#
#     @staticmethod  # known case of __new__
#     def __new__(*args, **kwargs):
#         pass
#
#     def __ne__(self, *args, **kwargs):
#         pass
#
#     def __pos__(self, *args, **kwargs):
#         pass
#
#     def __pow__(self, *args, **kwargs):
#         pass
#
#     def __radd__(self, *args, **kwargs):
#         pass
#
#     def __rdivmod__(self, *args, **kwargs):
#         pass
#
#     def __repr__(self, *args, **kwargs):
#         pass
#
#     def __rfloordiv__(self, *args, **kwargs):
#         pass
#
#     def __rmod__(self, *args, **kwargs):
#         pass
#
#     def __rmul__(self, *args, **kwargs):
#         pass
#
#     def __round__(self, *args, **kwargs):
#         pass
#
#     def __rpow__(self, *args, **kwargs):
#         pass
#
#     def __rsub__(self, *args, **kwargs):
#         pass
#
#     def __rtruediv__(self, *args, **kwargs):
#         pass
#
#     def __set_format__(self, *args, **kwargs): pass
#
#     def __sub__(self, *args, **kwargs):
#         pass
#
#     def __truediv__(self, *args, **kwargs):
#         pass
#
#     def __trunc__(self, *args, **kwargs):
#         pass
