# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------

from setuptools import setup

from PythonExtensions.Debug import PrettyPrint
from PythonExtensions.Setup import *
from PythonExtensions.__metadata__ import *




long_description = ReadFromFile(abspath("./PyPiReadme.md"))

install_requires = GetRequirements(abspath('./requirements.txt'))

_packages, _package_data = Get_Packages_Data(abspath('PythonExtensions'), __name__, includes=MatchFileTypes('py', 'png', 'txt', 'json'))


print()
print()
PrettyPrint(_package_data=_package_data, _packages=_packages)
print()
print()


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
      keywords=f'{__name__} Debug Files async Setup Tkinter Extensions tk ttk tkinter',
      package_dir={ __name__: __name__ },
      package_data=_package_data,
      )

