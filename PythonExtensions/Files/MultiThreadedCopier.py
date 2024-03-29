import os
from multiprocessing.pool import ThreadPool
from shutil import copy2
from typing import Union

from .FilePath import FilePath




__all__ = ['MultiThreadedCopier']

class MultiThreadedCopier(object):
    """
    Based on https://stackoverflow.com/a/64813422

src_dir = /path/to/src/dir
dest_dir = /path/to/dest/dir

with MultiThreadedCopier(max_threads=16) as copier:
    shutil.copytree(src_dir, dest_dir, copy_function=copier.copy)
    """
    __slots__ = ['pool', '_max_threads']
    def __init__(self, max_threads: int = os.cpu_count()): self._max_threads = max_threads
    def __enter__(self):
        self.pool = ThreadPool(self._max_threads)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()
        del self.pool

    def copy(self, source: Union[str, FilePath], dest: Union[str, FilePath]): return self.pool.apply_async(copy2, args=(source, dest))
