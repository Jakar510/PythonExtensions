# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2021.
#
# ------------------------------------------------------------------------------

import importlib
import os
from enum import Enum
from os.path import *
from typing import *




__all__ = [
    'DevelopmentStatus',
    'ReadFromFile', 'ReadLinesFromFile', 'GetRequirements', 'GetVersion',
    'Get_Packages_Data', 'pycache', 'GetPath',
    'MatchExtension', 'MatchFileTypes',
    ]

def ReadLinesFromFile(path: str) -> List[str]:
    with open(path, "r") as f:
        return f.readlines()

def ReadFromFile(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def GetVersion(o) -> str:
    if hasattr(o, '__version__'): return o.__version__
    elif hasattr(o, 'version'): return o.version
    elif hasattr(o, 'Version'): return o.Version
    elif hasattr(o, 'VERSION'): return o.VERSION
    else: raise AttributeError(f"can't get version from {o}")


def GetRequirements(path: str) -> List[str]:
    install_requires = []
    for line in ReadLinesFromFile(path):
        line = line.strip('\n')
        if line == 'pillow': package = importlib.import_module('PIL')
        else: package = importlib.import_module(line)
        VERSION = GetVersion(package)
        if VERSION.__class__.__name__ == 'module': VERSION = GetVersion(VERSION)

        install_requires.append(f'{line}>={VERSION}')
    return install_requires

class DevelopmentStatus(str, Enum):
    """
    How mature is this project? Common values are
      3 - Alpha
      4 - Beta
      5 - Production/Stable
    """
    Alpha = '3 - Alpha'
    Beta = '4 - Beta'
    Stable = '5 - Production/Stable'

pycache = '__pycache__'

def GetPath(name: str, *args: str) -> str: return '.'.join([name, *args])
def MatchExtension(name: str) -> str: return f'*.{name}'
def MatchFileTypes(*names: str) -> List[str]: return list(map(MatchExtension, names))

def Get_Packages_Data(path: str, root: str, *, includes: List[str] = [MatchExtension('py')], ignorables: List[str] = [pycache]):
    _packages: List[str] = []
    _package_data: Dict[str, List[str]] = { root: includes }

    for top, sub_dirs, files in os.walk(path):
        sub_dirs = set(sub_dirs)
        sub_dirs.discard(pycache)
        parent = basename(top)
        if parent in ignorables: continue
        if parent == root:
            for d in sub_dirs:
                _packages.append(GetPath(root, d))
        else:
            for d in sub_dirs:
                _packages.append(GetPath(root, parent, d))

        for item in _packages:
            _package_data[item] = includes

    return sorted(_packages), _package_data
