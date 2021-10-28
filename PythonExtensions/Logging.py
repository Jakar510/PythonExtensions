import logging
import sys
import tarfile
from logging import CRITICAL, DEBUG, ERROR, FATAL, FileHandler, Filter, Formatter, INFO, LogRecord, Logger, StreamHandler, WARNING, basicConfig, getLogger
from logging.handlers import RotatingFileHandler
from os.path import *
from pathlib import Path
from typing import *

from .Files import FilePath
from .Names import class_name




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
                 info: str = """%(name)s ---- %(message)s""",

                 simple: str = """[ %(levelname)-10s ] [ %(module)s.%(funcName)s @ Line#: %(lineno)d ] [ %(processName)s.%(threadName)s ] 
%(message)s
""",

                 detailed: str = """            
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
    __slots__ = ['_logs', '__log_paths__', 'MAX_LOGS', 'MAX_LOG_SIZE', 'APP_NAME', '_root_path', '__dict__']
    _logs: List[FilePath]
    __log_paths__: Dict[str, FilePath]
    def __init__(self, app_name: str, root_path: Union[str, FilePath], max_logs: int, max_log_size: int):
        self.__log_paths__ = { }
        self.MAX_LOGS: Final[int] = max_logs
        self.MAX_LOG_SIZE: Final[int] = max_log_size
        self.APP_NAME: Final[str] = app_name
        self._root_path: Final[Union[str, FilePath]] = root_path

    @property
    def logs(self) -> List[FilePath]:
        _logs: List[FilePath] = []
        for name, path in self.__log_paths__.items():
            _logs.append(path)
            for i in range(1, self.MAX_LOGS + 1):
                _logs.append(FilePath.Join(path.DirectoryName, f'{path.FileName}.{i}'))

        return _logs

    def Zip_Log_Files(self, path: str, mode: str = "w:gz"):
        """
            Open a tar archive for all logs.

        :param path: path to save the result.
        :param mode:
            Must be one of the following:
               'w' or 'w:'  open for writing without compression
               'w:gz'       open for writing with gzip compression
               'w:bz2'      open for writing with bzip2 compression
               'w:xz'       open for writing with lzma compression

               'w|'         open an uncompressed stream for writing
               'w|gz'       open a gzip compressed stream for writing
               'w|bz2'      open a bzip2 compressed stream for writing
               'w|xz'       open an lzma compressed stream for writing
        """
        with tarfile.open(path, mode) as tar:
            for file in self.logs:
                tar.add(file, arcname=file.BaseName)

    def Delete_Log_Files(self):
        for file in self.logs: file.Remove()

    @staticmethod
    def FileName(base: str):
        return f'{base}.log'

    @staticmethod
    def ErrorName(base: str):
        return f'{base}_errors'

    def GetErrorFileName(self, base: str):
        return f'{self.ErrorName(base)}.log'

    @classmethod
    def Create(cls, app_name: str, root_path: Union[str, Path, FilePath], *processes: str, max_logs: int = 5, max_log_size: int = 10240) -> 'LogPaths':
        if isfile(root_path): root_path = dirname(root_path)

        return cls(app_name, root_path, max_logs, max_log_size)._init(root_path, processes)

    def _init(self, root_path: Union[str, Path, FilePath], processes: Iterable[str]):
        for proc in set(processes):
            self.__log_paths__[proc] = FilePath.Join(root_path, self.FileName(proc))
            self.__log_paths__[self.ErrorName(proc)] = FilePath.Join(root_path, self.GetErrorFileName(proc))

        self.__dict__.update(self.__log_paths__)
        return self



class DebugFilter(Filter):
    __slots__ = ['_allowed']
    _allowed: Tuple[int, ...]
    def __init__(self, name=''):
        super().__init__(name)
        self._allowed = (DEBUG,)
    def filter(self, rec): return rec.levelno in self._allowed
class InfoFilter(Filter):
    __slots__ = ['_allowed']
    _allowed: Tuple[int, ...]
    def __init__(self, name=''):
        super().__init__(name)
        self._allowed = (INFO,)
    def filter(self, rec): return rec.levelno in self._allowed
class ErrorFilter(Filter):
    __slots__ = ['_allowed']
    _allowed: Tuple[int, ...]
    def __init__(self, name=''):
        super().__init__(name)
        self._allowed = (WARNING, ERROR, CRITICAL, FATAL)
    def filter(self, rec):
        return rec.levelno in self._allowed
class PngImagePlugin_Filter(Filter):
    __slots__ = []
    def filter(self, record: LogRecord) -> bool:
        if record.module == 'PngImagePlugin':
            return False

        return True


class LoggingFilterMixin:
    __slots__ = ['_allowed', 'formatter']
    _allowed: Tuple[int, ...]
    formatter: Formatter
    def __init__(self, formatter: Formatter, *args: int):
        self._allowed = args
        self.formatter = formatter


class Error_Handler(RotatingFileHandler, LoggingFilterMixin):
    def __init__(self, *, file, path: LogPaths, fmt: Formats, **kwargs):
        RotatingFileHandler.__init__(self, filename=file, maxBytes=path.MAX_LOG_SIZE, backupCount=path.MAX_LOGS, **kwargs)
        LoggingFilterMixin.__init__(self, Formatter(fmt=fmt.DETAILED), WARNING, ERROR, CRITICAL, FATAL)
        self.setLevel(ERROR)
        self.addFilter(ErrorFilter())


class Info_Handler(FileHandler, LoggingFilterMixin):
    __slots__ = ['_allowed', 'formatter']
    _allowed: Tuple[int, ...]
    def __init__(self, *, file, mode='w', fmt: Formats, **kwargs):
        FileHandler.__init__(self, filename=file, mode=mode, **kwargs)
        LoggingFilterMixin.__init__(self, Formatter(fmt=fmt.INFO), DEBUG, INFO)
        self.setLevel(DEBUG)
        self.addFilter(InfoFilter())


class Console_Debug(StreamHandler, LoggingFilterMixin):
    def __init__(self, *, fmt: Formats, stream=sys.stdout):
        super().__init__(stream)
        LoggingFilterMixin.__init__(self, Formatter(fmt=fmt.INFO))
        self.setLevel(DEBUG)
        self.addFilter(DebugFilter())
class Console_Info(StreamHandler, LoggingFilterMixin):
    def __init__(self, *, fmt: Formats, stream=sys.stdout):
        super().__init__(stream)
        LoggingFilterMixin.__init__(self, Formatter(fmt=fmt.INFO))
        self.setLevel(DEBUG)
        self.addFilter(InfoFilter())
class Console_Error(StreamHandler, LoggingFilterMixin):
    def __init__(self, *, fmt: Formats, stream=sys.stderr):
        super().__init__(stream)
        LoggingFilterMixin.__init__(self, Formatter(fmt=fmt.DETAILED))
        self.setLevel(WARNING)
        self.addFilter(ErrorFilter())




class LoggingManager(object):
    __slots__ = ['_mapper', 'fmt', 'paths', '_root_logger', 'app_logger', 'paths']
    _mapper: Dict[Type, str]
    def __init__(self, paths: LogPaths, fmt: Formats, mapper: Dict[Type, str] = None, *types: Type, ):
        self.fmt = fmt
        self.paths = paths
        if not isinstance(mapper, dict):
            mapper = { item: item.__name__ for item in set(types) }

        self._mapper = mapper
        basicConfig(format=fmt.DETAILED, level=DEBUG)
        self._root_logger = getLogger()
        self._root_logger.handlers.clear()

        self.app_logger = getLogger(self.paths.APP_NAME)

        getLogger("PIL.PngImagePlugin").disabled = True


    def CreateLogger(self, source, *, debug: bool = __debug__) -> Logger:
        for key, value in self._mapper.items():
            # if issubclass(source, key): raise InstanceError('source is not identified')

            if isinstance(source, key):
                logger = self.app_logger.getChild(class_name(self))
                logger.addHandler(Info_Handler(file=self.paths.__log_paths__[value], fmt=self.fmt))
                logger.addHandler(Error_Handler(file=self.paths.__log_paths__[LogPaths.ErrorName(value)], fmt=self.fmt, path=self.paths))

                logger.addHandler(Console_Error(fmt=self.fmt))
                logger.addHandler(Console_Debug(fmt=self.fmt))
                logger.addHandler(Console_Info(fmt=self.fmt))
                logger.addFilter(PngImagePlugin_Filter())
                logger.setLevel(DEBUG if debug else ERROR)

                return logger

        else:
            raise ValueError(f'source is not identified: [ {source} ]  Expected one of {tuple(self._mapper.keys())}')


    @classmethod
    def FromTypes(cls, *types: Type, app_name: str, root_path: Union[str, Path, FilePath], logs: Type[LogPaths] = LogPaths, fmt: Formats = Formats()):
        """
        For each Type passed, the logger's name is the class's __log_name__ field or __name__ is used if it doesn't exist.
        If you wish to change the field name, override LoggingManager._getName

        :param types: the Types used to initialize
        :param app_name: name of the app
        :param root_path: absolute path to the folder where logs should be stored
        :param logs:
        :param fmt:
        :return:
        """
        mapper = { item: cls._getName(item) for item in set(types) }
        return cls(logs.Create(app_name, root_path, *mapper.values()), fmt, mapper)

    @staticmethod
    def _getName(item: Type) -> str:
        if hasattr(item, '__log_name__'): return str(item.__log_name__)

        return item.__name__
