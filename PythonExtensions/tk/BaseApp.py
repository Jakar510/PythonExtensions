from abc import ABC
from asyncio import AbstractEventLoop, get_event_loop
from logging import Logger
from typing import *

from .Core import *
from .Events import Bindings, TkinterEvent, tkEvent
from ..Files import FilePath
from ..Logging import LoggingManager
from ..Names import class_name
from ..Threads import AutoStartThread




__all__ = [
    'BaseApp',
    'BaseAsyncApp',
    'BaseSyncApp',
    'BaseWindow',
    'BaseLabelWindow',
    'Updater',
    'AsyncUpdater',
    ]

class Updater(AutoStartThread, ABC):
    __slots__ = ['_app']
    _app: Optional['BaseApp']
    def __init__(self, app: 'BaseApp'):
        self._app = app
        AutoStartThread.__init__(self)

    def stop(self): raise NotImplementedError()



class AsyncUpdater(AutoStartThread):
    __slots__ = ['_loop']
    _loop: Optional[AbstractEventLoop]
    def __init__(self, loop: AbstractEventLoop):
        self._loop = loop
        AutoStartThread.__init__(self)

    def run(self):
        self._loop.run_forever()

    def stop(self):
        self._loop.stop()

    @property
    def loop(self) -> AbstractEventLoop: return self._loop



_TUpdater = TypeVar('_TUpdater', Updater, AsyncUpdater)
class BaseApp(Generic[_TUpdater], ABC):
    """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
    __slots__ = ['root', 'logger', '_logging_manager', '_loop']
    root: tkRoot
    logger: Logger
    _logging_manager: LoggingManager
    _loop: _TUpdater
    def __init__(self, updater: _TUpdater, app_name: str, root: tkRoot, *types: Type, **kwargs):
        root_path = kwargs.pop('root_path', '.')

        self._logging_manager = LoggingManager.FromTypes(self.__class__, *types, app_name=app_name, root_path=FilePath.convert(root_path))
        self.logger = self._logging_manager.CreateLogger(self, debug=self.DEBUG)
        self._loop = updater
        self.root = root

        self.root.protocol('WM_DELETE_WINDOW', self.Close)

        self.root.Bind(Bindings.ButtonPress, self._OnPress)
        self.root.Bind(Bindings.Key, self._OnKeyPress)
        self._setup()

    @property
    def DEBUG(self) -> bool:
        return __debug__


    def Close(self):
        """ Override to add functionality. Closes updater loop then closes application. """
        self._loop.stop()
        self.root.destroy()
    def start_gui(self, *_args, **_kwargs):
        self.root.mainloop()

    def _setup(self):
        """Called on class creation. use this to create any required attributes, views, threads, processes, etc for the app to run."""
        raise NotImplementedError()


    def _OnPress(self, event: tkEvent) -> Optional[bool]:
        return self.Handle_Press(TkinterEvent(event))
    def Handle_Press(self, event: TkinterEvent) -> Optional[bool]:
        raise NotImplementedError()



    def _OnKeyPress(self, event: tkEvent) -> Optional[bool]:
        return self.Handle_KeyPress(TkinterEvent(event))
    def Handle_KeyPress(self, event: TkinterEvent) -> Optional[bool]:
        raise NotImplementedError()



class BaseAsyncApp(BaseApp[AsyncUpdater], ABC):
    """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
    def __init__(self, *types: Type,
                 app_name: str,
                 loop: Type[AbstractEventLoop] = None,
                 x: int = 0,
                 y: int = 0,
                 Screen_Width: Optional[int] = None,
                 Screen_Height: Optional[int] = None,
                 updater: Type[AsyncUpdater] = None,
                 fullscreen: Optional[bool] = None,
                 root_path: Union[str, FilePath] = None,
                 **kwargs):
        if fullscreen is None: fullscreen = not self.DEBUG
        root = tkRoot.Create(Screen_Width, Screen_Height, fullscreen, x, y, **kwargs)
        _updater = (updater or AsyncUpdater)(loop or get_event_loop())

        BaseApp.__init__(self, _updater, app_name, root, *types, root_path=root_path, **kwargs)

    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop.loop



class BaseSyncApp(BaseApp[Updater], ABC):
    """ Override to extend functionality. Indented to be the base class for the Application level class, which is passed to all child windows and frames. """
    def __init__(self, *types: Type,
                 app_name: str,
                 x: int = 0,
                 y: int = 0,
                 Screen_Width: Optional[int] = None,
                 Screen_Height: Optional[int] = None,
                 updater: Type[Updater] = None,
                 fullscreen: Optional[bool] = None,
                 root_path: Union[str, FilePath] = None,
                 **kwargs):
        if fullscreen is None: fullscreen = not self.DEBUG
        root = tkRoot.Create(Screen_Width, Screen_Height, fullscreen, x, y, **kwargs)
        _updater = (updater or Updater)(self)

        BaseApp.__init__(self, _updater, app_name, root, *types, root_path=root_path, **kwargs)



    # @staticmethod
    # def InitAsync(): 
    #     set_event_loop_policy(AsyncTkinterEventLoopPolicy())



_TBaseApp = TypeVar('_TBaseApp', bound=BaseApp)
class _WindowMixin(Generic[_TBaseApp]):
    __log_name__: str
    _app: _TBaseApp
    def __init__(self, app: _TBaseApp):
        assert (isinstance(app, BaseApp))
        self._app = app
        self._logger = app.logger.getChild(str(class_name(self)))

    def OnPress(self, event: TkinterEvent): pass
    def OnKeyPress(self, event: TkinterEvent): pass


class BaseWindow(Frame, _WindowMixin[_TBaseApp]):
    def __init__(self, master, app: _TBaseApp, **kwargs):
        Frame.__init__(self, master, **kwargs)
        _WindowMixin.__init__(self, app)

    @classmethod
    def Root(cls, app: _TBaseApp, **kwargs):
        return cls(app.root, app, **kwargs)


class BaseLabelWindow(LabelFrame, _WindowMixin[_TBaseApp]):
    def __init__(self, master, app: _TBaseApp, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        _WindowMixin.__init__(self, app)

    @classmethod
    def Root(cls, app: _TBaseApp, **kwargs):
        return cls(app.root, app, **kwargs)
