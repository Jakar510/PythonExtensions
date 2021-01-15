# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

from .Setup import *
from .__version__ import *




__name__ = 'PythonExtensions'
__author__ = "Tyler Stegmaier"
__email__ = "tyler.stegmaier.510@gmail.com"
__copyright__ = "Copyright 2020"
__credits__ = [
        "Tkinter library authors"
        "Copyright (c) 2020 Tyler Stegmaier",
        "Copyright (c) 2018 Pete Mojeiko for [Keyboard](src/Extensions/tk/Widgets/KeyBoard.py)",
        "Copyright (c) 2017 Ole Jakob Skjelten for [AnimatedGIF](src/Extensions/tk/Widgets/Custom.py)",
        "Copyright (c) 2018 paolo-gurisatti for [Html Widgets](src/Extensions/tk/Widgets/HTML.py)",
        ]
__license__ = "MIT"
__version__ = version
__maintainer__ = __author__
__maintainer_email__ = __email__

__status__ = DevelopmentStatus.Beta.value

__url__ = r'https://github.com/Jakar510/PythonExtensions'
# download_url=f'https://github.com/Jakar510/PyDebug/TkinterExtensions/releases/tag/{version}'
__classifiers__ = [
        __status__,

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: Free To Use But Restricted',

        # Support platforms
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',

        'Programming Language :: Python :: 3',
        ]

__short_description__ = 'Strongly typed classes with multiple built in helper functions to speed up development.'
