# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2021.
#
# ------------------------------------------------------------------------------

import os
from importlib.metadata import PackageNotFoundError, version
from os.path import *
from typing import *

from .Classifiers import *




pycache = '__pycache__'

def ReadLinesFromFile(path: str) -> List[str]:
    with open(path, "r") as f:
        return f.readlines()

def ReadFromFile(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def GetVersion(o) -> str:
    if hasattr(o, '__version__'): return o.__version__
    if hasattr(o, 'version'): return o.version
    if hasattr(o, 'Version'): return o.Version
    if hasattr(o, 'VERSION'): return o.VERSION

    raise AttributeError(f"can't get version from {o}")



def GetRequirements(path: str, *, separator: str = '>=') -> List[str]:
    install_requires: List[str] = []
    for line in ReadLinesFromFile(path):
        line = line.strip()
        if not line: continue
        try:
            install_requires.append(f'{line}{separator}{version(line)}')
        except PackageNotFoundError as e:
            raise PackageNotFoundError(f'package "{line}" not found') from e

    return install_requires


def GetPath(name: str, *args: str) -> str: return '.'.join([name, *args])
def MatchExtension(name: str) -> str: return f'*.{name}'
def MatchFileTypes(*names: str) -> List[str]: return list(map(MatchExtension, names))


def GetRootFiles(root: str):
    files: Set[str] = set()
    for f in os.listdir(root):
        if isfile(join(root, f)):
            files.add(f)

    return files


def Get_Packages_Data(path: str, root: str, *, includes: List[str], ignorables: List[str] = [pycache]):
    _packages: List[str] = []
    _package_data: Dict[str, List[str]] = { root: includes }


    for top, sub_dirs, files in os.walk(path):
        sub_dirs = set(sub_dirs)
        sub_dirs.discard(pycache)
        parent = basename(top)

        if parent in ignorables:
            continue

        if parent == root:
            for d in sub_dirs:
                _packages.append(GetPath(root, d))
        else:
            for d in sub_dirs:
                _packages.append(GetPath(root, parent, d))

        for item in _packages:
            _package_data[item] = includes


    return sorted(_packages), _package_data
