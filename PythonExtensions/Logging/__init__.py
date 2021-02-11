import logging
import logging.config
import sys
import tarfile
from logging.handlers import RotatingFileHandler
from typing import *

from ..Files import FilePath
from ..Names import class_name




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
    _logs: List[FilePath]
    __log_paths__: Dict[str, FilePath] = { }
    def __init__(self, app_name: str, root_path: Union[str, FilePath], max_logs: int, max_log_size: int):
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
    def FileName(base: str): return f'{base}.log'

    @staticmethod
    def ErrorName(base: str): return f'{base}_errors'

    def GetErrorFileName(self, base: str): return f'{self.ErrorName(base)}.log'

    @classmethod
    def Create(cls, app_name: str, root_path: Union[str, FilePath], *processes: str, max_logs: int = 5, max_log_size: int = 10240) -> 'LogPaths':
        obj = cls(app_name, root_path, max_logs, max_log_size)

        for proc in set(processes):
            obj.__log_paths__[proc] = FilePath.Join(root_path, obj.FileName(proc))
            obj.__log_paths__[obj.ErrorName(proc)] = FilePath.Join(root_path, obj.GetErrorFileName(proc))

        obj.__dict__.update(obj.__log_paths__)
        return obj


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
    _mapper: Dict[Type, str]
    def __init__(self, paths: LogPaths, fmt: Formats, mapper: Dict[Type, str] = None, *types: Type, ):
        self.fmt = fmt
        self.paths = paths
        if not isinstance(mapper, dict):
            mapper = { item: item.__name__ for item in set(types) }

        self._mapper = mapper
        logging.basicConfig(format=fmt.DETAILED, level=logging.DEBUG)
        self._root_logger = logging.getLogger()
        self._root_logger.handlers.clear()

        self.app_logger = logging.getLogger(self.paths.APP_NAME)

        logging.getLogger("PIL.PngImagePlugin").disabled = True

    def CreateLogger(self, source, *, debug: bool = __debug__) -> logging.Logger:
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
                logger.setLevel(logging.DEBUG if debug else logging.ERROR)
                return logger

        else:
            raise ValueError(f'source is not identified: [ {source} ]  Expected one of {tuple(self._mapper.keys())}')

    @classmethod
    def FromTypes(cls, *types: Type, app_name: str, root_path: Union[str, FilePath], logs: Type[LogPaths] = LogPaths, fmt: Formats = Formats()):
        mapper = { item: item.__name__ for item in set(types) }
        return cls(logs.Create(app_name, root_path, *mapper.values()), fmt, mapper)
