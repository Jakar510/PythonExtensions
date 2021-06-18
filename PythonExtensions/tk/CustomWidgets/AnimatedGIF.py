# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import base64
from typing import List, Union

from PIL.Image import Image, open as img_open
from PIL.ImageTk import PhotoImage

from ..Base import *
from ..Widgets import *




__all__ = [
    'AnimatedGIF',
    ]

class AnimatedGIF(Label, object):
    """
    Creates an Animated loading screen with a GIF whose animation is started by AnimatedGIF.Pack/Place/Grid/show and stopped by AnimatedGIF.hide.

    Based off of:
        AnimatedGIF - a class to show an animated gif without blocking the tkinter mainloop()
        Copyright (c) 2016 Ole Jakob Skjelten <olesk@pvv.org>
        Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md.md
        https://github.com/olesk75/AnimatedGIF/blob/master/AnimatedGif.py
    """
    _callback_id = None
    _is_running: bool = False
    _forever: bool = False

    _loc: int = 0
    _frames: List[PhotoImage] = []
    def __init__(self, master: tk.Widget, *, root: Union[tk.Tk, tk.Toplevel] = None, path: str, forever=True, defaultDelay: int = 100):
        super().__init__(master)
        self._master = master
        self._forever = forever
        self.Root = root

        with img_open(path) as img:
            assert (isinstance(img, Image))

            try: self._delay = img.info['duration']
            except (AttributeError, KeyError): self._delay = defaultDelay

            i = 0
            while True:
                try:
                    frame = PhotoImage(image=img.copy().convert(mode='RGBA'), master=self.Root or self)
                    self._frames.append(frame)

                    i += 1
                    img.seek(i)
                except EOFError: break

        self._setFrame()
    def start_animation(self, frame: int = None):
        if self._is_running: return

        if frame is not None:
            self._loc = frame
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True
    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False
    def _setFrame(self): self.configure(image=self._frames[self._loc])
    def _animate_GIF(self):
        self._loc += 1
        self._setFrame()

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    @property
    def _last_index(self) -> int: return len(self._frames) - 1



    def Pack(self, start_animation: bool = True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Pack(**kwargs)
    def Grid(self, start_animation: bool = True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Grid(**kwargs)
    def Place(self, start_animation: bool = True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Place(**kwargs)

    def show(self, start_animation: bool = True, **kwargs) -> bool:
        if start_animation: self.start_animation()
        return super().show()
    def hide(self, parent: tk.Widget = None) -> bool:
        self.stop_animation()
        return super().hide(parent)

    @classmethod
    def FromBase64Data(cls, master, *, root: Union[tk.Tk, tk.Toplevel] = None, data: Union[str, bytes], path: str, forever=True, defaultDelay: int = 100):
        with open(path, 'wb') as fp:
            fp.write(base64.urlsafe_b64decode(data))

        return cls(master, root=root, path=path, forever=forever, defaultDelay=defaultDelay)
