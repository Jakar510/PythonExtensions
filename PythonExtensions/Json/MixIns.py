from typing import *




_AnyID = TypeVar("AnyID", str, int)

class _MixinBase:
    get: callable
    __setitem__: callable


class IdMixin(_MixinBase, Generic[_AnyID]):
    __id_key__ = 'ID'
    @property
    def ID(self) -> _AnyID: return self.get(self.__id_key__, None)
    @ID.setter
    def ID(self, v: _AnyID): self[self.__id_key__] = v


class NameMixin(_MixinBase):
    __name_key__ = 'Name'
    @property
    def Name(self) -> str: return self.get(self.__name_key__, None)
    @Name.setter
    def Name(self, v: str): self[self.__name_key__] = v



class AutoNameMixin:
    @property
    def __name__(self) -> str:
        try: return f'{self.__class__.__module__}.{self.__class__.__qualname__}'
        except AttributeError: return f'{self.__class__.__module__}.{self.__class__.__name__}'

class ItemNameMixin:
    __name__: str = None
