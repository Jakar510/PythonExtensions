# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2021.
#
# ------------------------------------------------------------------------------

from .SwitchCase import test_switch_case
from .base import TestLogging, Test_base
from .debug import Test_debug
from .test_tk import run_all
from .test_files import test_files




__all__ = ['RUN_TESTS']

def RUN_TESTS():
    test_files()
    Test_base()
    TestLogging()
    # test_switch_case()
    Test_debug()
    run_all()
