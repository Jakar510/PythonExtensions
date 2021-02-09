from logging import Logger
from typing import *

from ..Core import *
from ..Events import Bindings, TkinterEvent
from ...Files import FilePath
from ...Logging import LoggingManager
from ...nameof import class_name




__all__ = [
    'BaseApp',
    'BaseWindow',
    'BaseLabelWindow',
    ]

class BaseApp(object):
    """ Override to extend functionallity. Intented to be the base class for the Application level class, which is passed to all child windows and frames. """
    root: tkRoot
    logger: Logger
    _logging_manager: LoggingManager
    def __init__(self, *types: Type, app_name: str, root_path: Union[str, FilePath],
                 Screen_Width: Optional[int] = None, Screen_Height: Optional[int] = None,
                 fullscreen: Optional[bool] = None, x: int = 0, y: int = 0, **kwargs):
        self._logging_manager = LoggingManager.FromTypes(self.__class__, *types, app_name=app_name, root_path=root_path)
        self.logger = self._logging_manager.CreateLogger(self, debug=self.DEBUG)

        if fullscreen is None: fullscreen = not self.DEBUG
        self.root = tkRoot.Create(Screen_Width, Screen_Height, fullscreen, x, y, **kwargs)
        self.root.protocol('WM_DELETE_WINDOW', self.Close)

        self.root.Bind(Bindings.ButtonPress, self.Handle_Press)
        self.root.Bind(Bindings.Key, self.Handle_KeyPress)


    def Close(self):
        """ Override to add functinality. Closes application. """
        self.root.destroy()


    # noinspection PyUnusedLocal
    def start_gui(self, *args, **kwargs): self._main()

    def _main(self): self.root.mainloop()

    @property
    def DEBUG(self) -> bool: return __debug__

    def Handle_Press(self, event: TkinterEvent): pass
    def Handle_KeyPress(self, event: TkinterEvent): pass

    def _OnPress(self, event: TkinterEvent): pass
    def _OnKeyPress(self, event: TkinterEvent): pass



_TBaseApp = TypeVar('_TBaseApp', bound=BaseApp)
class _WindowMixin(Generic[_TBaseApp]):
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
