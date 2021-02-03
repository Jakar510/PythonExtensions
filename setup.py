# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------

from setuptools import setup

from PythonExtensions import __author__, __classifiers__, __email__, __license__, __maintainer__, __maintainer_email__, __name__, __short_description__, __url__, __version__
from PythonExtensions.Setup import *
from PythonExtensions.debug import *




long_description = ReadFromFile(os.path.abspath("./PyPiReadme.md"))

install_requires = GetRequirements(os.path.abspath('./requirements.txt'))

_packages, _package_data = Get_Packages_Data(os.path.abspath('PythonExtensions'), __name__, includes=MatchFileTypes('py', 'png'))

PrettyPrint('_packages', _packages)
PrettyPrint('_package_data', _package_data)
PrettyPrint('install_requires', install_requires)

setup(name=__name__,
      version=__version__,
      packages=_packages,
      url=__url__,
      license=__license__,
      author=__author__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__maintainer_email__,
      description=__short_description__,
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=install_requires,
      classifiers=__classifiers__,
      keywords=f'{__name__} Json Setup SwitchCase Switch Case Tkinter Extensions tk ttk tkinter',
      package_dir={ __name__: __name__ },
      package_data=_package_data,
      )
