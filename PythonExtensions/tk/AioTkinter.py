import asyncio
import tkinter as tk
from selectors import EVENT_READ, EVENT_WRITE, SelectSelector, SelectorKey
from typing import *




__all__ = ['AsyncTkinterEventLoopPolicy', '__doc__']

__doc__ = """
https://github.com/montag451/aiotkinter

Copyright (c) 2011, montag451.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""





class _TkinterSelector(SelectSelector):
    """
    Based off of _TkinterSelector from https://github.com/montag451/aiotkinter/blob/master/aiotkinter.py
    See also: https://gist.github.com/damonjw/35aac361ca5d313ee9bf79e00261f4ea
    """
    __slots__ = []
    def __init__(self, root=None):
        super().__init__()

        # from ..Core.tkRoot import tkRoot
        self._tk = root or tk.Tk(useTk=0)
        assert (isinstance(self._tk, tk.Tk))

        self._ready: List[Tuple[SelectorKey, int]] = []


    # def get_map(self) -> Mapping[FileDescriptorLike, SelectorKey]:
    #     """Return a mapping of file objects to selector keys."""
    #     return super().get_map()

    def register(self, file_obj, events, data=None) -> SelectorKey:
        """Register a file object.

        Parameters:
        file_obj -- file object or file descriptor
        events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)
        data    -- attached data

        Returns:
        SelectorKey instance

        Raises:
        ValueError if events is invalid
        KeyError if file_obj is already registered
        OSError if file_obj is closed or otherwise is unacceptable to
                the underlying system call (if a system call is made)

        Note:
        OSError may or may not be raised
        """
        key: SelectorKey = super().register(file_obj, events, data)

        mask = 0
        if events & EVENT_READ: mask |= tk.READABLE
        if events & EVENT_WRITE: mask |= tk.WRITABLE

        def ready(fd, _mask):
            assert key.fd == fd
            _events = 0
            if _mask & tk.READABLE:
                _events |= EVENT_READ
            if _mask & tk.WRITABLE:
                _events |= EVENT_WRITE
            self._ready.append((key, _events))


        self._tk.tk.createfilehandler(key.fd, mask, ready)
        return key

    def unregister(self, file_obj) -> SelectorKey:
        """Unregister a file object.

        Parameters:
        file_obj -- file object or file descriptor

        Returns:
        SelectorKey instance

        Raises:
        KeyError if file_obj is not registered

        Note:
        If file_obj is registered but has since been closed this does
        *not* raise OSError (even if the wrapped syscall does)
        """
        key = super().unregister(file_obj)
        self._tk.deletefilehandler(key.fd)
        return key

    def select(self, timeout: float = None):
        """Perform the actual selection, until some monitored file objects are
        ready or a timeout expires.

        Parameters:
        timeout -- if timeout > 0, this specifies the maximum wait time, in
                   seconds
                   if timeout <= 0, the select() call won't block, and will
                   report the currently ready file objects
                   if timeout is None, select() will block until a monitored
                   file object becomes ready

        Returns:
        list of (key, events) for ready file objects
        `events` is a bitwise mask of EVENT_READ|EVENT_WRITE
        """
        self._ready = []

        token = None
        if timeout is not None: token = self._tk.after(int(timeout * 1000), lambda: True)
        self._tk.do_one_event()
        if timeout is not None: self._tk.after_cancel(token)

        return self._ready



class AsyncTkinterEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    """
    Based off of TkinterEventLoopPolicy from https://github.com/montag451/aiotkinter/blob/master/aiotkinter.py
    See also: https://gist.github.com/damonjw/35aac361ca5d313ee9bf79e00261f4ea
    """
    __slots__ = []
    def new_event_loop(self):
        try:
            # from ...Names import nameof
            # print(nameof(self._loop_factory))
            # asyncio.windows_events.ProactorEventLoop
            return self._loop_factory(selector=_TkinterSelector())
        except TypeError as e:
            raise Exception('The default event loop is not a selector event loop') from e
