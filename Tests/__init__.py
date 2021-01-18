# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2021.
#
# ------------------------------------------------------------------------------

from .SwitchCase import run_tests
from .base import TestLogging, Test_base
from .debug import Test_debug
from .test_tk import run_all




__all__ = ['RUN_TESTS']

def RUN_TESTS():
    Test_base()
    TestLogging()
    # run_tests()
    Test_debug()
    run_all()
