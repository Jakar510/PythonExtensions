# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from logging import Logger

from .Root import *




__all__ = ['BaseApp']

class BaseApp(object):
    """ Override to extend functionallity. Intented to be the base class for the Application level class, which is passed to all child windows and frames. """
    logger: Logger
    root: tkRoot

    @property
    def DEBUG(self) -> bool: return __debug__
