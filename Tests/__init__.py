# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2021.
#
# ------------------------------------------------------------------------------

from .base import Test_base, TestLogging
from .debug import Test_debug
from .SwitchCase import run_tests
from .test_tk import run_all

def run_all():
    Test_base()
    TestLogging()
    # run_tests()
    Test_debug()
    run_all()
