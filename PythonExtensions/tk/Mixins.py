
# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------



class AutoNameMixin:
    @property
    def __name__(self) -> str: return str(self.__class__.__name__)


class NameMixin:
    __name__: str = None
