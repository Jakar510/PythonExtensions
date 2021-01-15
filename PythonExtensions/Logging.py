import logging
import logging.config
import os
import sys
import tarfile
from logging.handlers import RotatingFileHandler
from typing import *




__all__ = [
        'logging',
        'LoggingManager',
        'Error_Handler',
        'Info_Handler',
        'Console_Error', 'Console_Debug', 'Console_Info',
        'InfoFilter', 'ErrorFilter', 'DebugFilter', 'PngImagePlugin_Filter',
        'LogPaths', 'Formats'
        ]

class Formats(object):
    def __init__(self,
                 info="""%(name)s ---- %(message)s""",

                 simple="""[ %(levelname)-10s ] [ %(module)s.%(funcName)s @ Line#: %(lineno)d ] [ %(processName)s.%(threadName)s ] 
%(message)s
""",

                 detailed="""            
[  %(levelname)-10s         %(asctime)s ] 
[ FILE: "%(pathname)s" : %(module)s.%(funcName)s @ Line # %(lineno)d ] 
[ Process ID: %(process)-7d | %(processName)s ] 
[ Thread ID: %(thread)-7d | %(threadName)s ] 
MESSAGE: %(message)s
"""):
        self.INFO: Final[str] = info
        self.SIMPLE: Final[str] = simple
        self.DETAILED: Final[str] = detailed



class LogPaths(object):
    def __init__(self, *processes: str, app_name: str, root_path: str, max_logs: int = 5, max_log_size: int = 10240):
        self.MAX_LOGS: Final[int] = max_logs
        self.MAX_LOG_SIZE: Final[int] = max_log_size
        self.APP_NAME: Final[str] = app_name
        self._root_path: Final[str] = root_path
        self.__log_paths__ = { }

        for proc in set(processes):
            self.__log_paths__[proc] = os.path.join(root_path, self.GetFileName(proc))
            self.__log_paths__[self.GetErrorName(proc)] = os.path.join(root_path, self.GetErrorFileName(proc))

        self.__dict__.update(self.__log_paths__)

    @property
    def logs(self) -> List[str]:
        return [os.path.join(self._root_path, f'{name}.{i}') if i != 0 else name for i in range(self.MAX_LOGS + 1) for name in self.__log_paths__.keys()]

    def Zip_Log_Files(self, path: str):
        with tarfile.open(path, "w:gz") as tar:
            for file in self.logs:
                tar.add(file, arcname=os.path.basename(file))

    def Delete_Log_Files(self):
        for file in self.logs:
            if os.path.isfile(file): os.remove(file)

    @staticmethod
    def GetFileName(base: str): return f'{base}.log'
    @staticmethod
    def GetErrorFileName(base: str): return f'{base}_errors.log'
    @staticmethod
    def GetErrorName(base: str): return f'{base}_errors'





class DebugFilter(logging.Filter):
    _allowed = (logging.DEBUG,)
    def filter(self, rec):
        return rec.levelno in self._allowed
class InfoFilter(logging.Filter):
    _allowed = (logging.INFO,)
    def filter(self, rec):
        return rec.levelno in self._allowed
class ErrorFilter(logging.Filter):
    _allowed = (logging.WARNING, logging.ERROR, logging.CRITICAL, logging.FATAL)
    def filter(self, rec):
        return rec.levelno in self._allowed
class PngImagePlugin_Filter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.module == 'PngImagePlugin':
            return False

        return True



class Error_Handler(RotatingFileHandler):
    _allowed = (logging.WARNING, logging.ERROR, logging.CRITICAL, logging.FATAL)
    def __init__(self, *, file, path: LogPaths, fmt: Formats, **kwargs):
        super().__init__(filename=file, maxBytes=path.MAX_LOG_SIZE, backupCount=path.MAX_LOGS, **kwargs)
        self.formatter = logging.Formatter(fmt=fmt.DETAILED)
        self.setLevel(logging.ERROR)
        self.addFilter(ErrorFilter())


class Info_Handler(logging.FileHandler):
    _allowed = (logging.DEBUG, logging.INFO)
    def __init__(self, *, file, mode='w', fmt: Formats, **kwargs):
        super().__init__(filename=file, mode=mode, **kwargs)
        self.formatter = logging.Formatter(fmt=fmt.INFO)
        self.setLevel(logging.DEBUG)
        self.addFilter(InfoFilter())


class Console_Debug(logging.StreamHandler):
    _allowed: tuple
    def __init__(self, *, fmt: Formats, stream=sys.stdout):
        super().__init__(stream)
        self.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(fmt=fmt.INFO)
        self.addFilter(DebugFilter())
class Console_Info(logging.StreamHandler):
    _allowed: tuple
    def __init__(self, *, fmt: Formats, stream=sys.stdout):
        super().__init__(stream)
        self.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(fmt=fmt.INFO)
        self.addFilter(InfoFilter())
class Console_Error(logging.StreamHandler):
    _allowed: tuple
    # def __init__(self, *, allowed=(logging.WARNING, logging.ERROR, logging.CRITICAL, logging.FATAL), stream=sys.stderr):
    def __init__(self, *, fmt: Formats, stream=sys.stderr):
        super().__init__(stream)
        # self._allowed = allowed
        self.setLevel(logging.WARNING)
        self.formatter = logging.Formatter(fmt=fmt.DETAILED)
        self.addFilter(ErrorFilter())




class LoggingManager(object):
    mapper: Dict[Type, str]
    def __init__(self, *types: Type, mapper: Dict[Type, str] = None, paths: LogPaths, fmt: Formats = Formats()):
        self.fmt = fmt
        self.paths = paths
        if not isinstance(mapper, dict):
            mapper = { item: item.__name__ for item in set(types) }

        self.mapper = mapper
        logging.basicConfig(format=fmt.DETAILED, level=logging.DEBUG)
        self._root_logger = logging.getLogger()
        self._root_logger.handlers.clear()

        self.app_logger = logging.getLogger(self.paths.APP_NAME)

        logging.getLogger("PIL.PngImagePlugin").disabled = True

    def CreateLogger(self, source, *, debug: bool = __debug__) -> logging.Logger:
        for key, value in self.mapper.items():
            # if issubclass(source, key): raise InstanceError('source is not identified')

            if isinstance(source, key):
                logger = self.app_logger.getChild(source.__class__.__name__)
                logger.addHandler(Info_Handler(file=self.paths.__log_paths__[value], fmt=self.fmt))
                logger.addHandler(Error_Handler(file=self.paths.__log_paths__[LogPaths.GetErrorName(value)], fmt=self.fmt, path=self.paths))

                logger.addHandler(Console_Error(fmt=self.fmt))
                logger.addHandler(Console_Debug(fmt=self.fmt))
                logger.addHandler(Console_Info(fmt=self.fmt))
                logger.addFilter(PngImagePlugin_Filter())
                logger.setLevel(logging.DEBUG if debug else logging.ERROR)
                return logger

        else:
            raise ValueError(f'source is not identified: [ {source} ]')

    @classmethod
    def FromTypes(cls, *types: Type, app_name: str, root_path: str):
        mapper = { item: item.__name__ for item in types }
        return cls(mapper=mapper,
                   paths=LogPaths(*mapper.values(), app_name=app_name, root_path=root_path))

