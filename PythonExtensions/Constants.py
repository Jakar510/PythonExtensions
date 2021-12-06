import platform
import re
import socket
import uuid
from typing import *

import psutil




__all__ = [
    'ARCHITECTURE', 'PROCESSOR',
    'PLATFORM', 'PLATFORM_RELEASE', 'PLATFORM_VERSION',
    'PLATFORM_IS_LINUX', 'PLATFORM_IS_WINDOWS',
    'CPU_COUNT', 'RAM',
    'HOSTNAME', 'IP_ADDRESS', 'MAC_ADDRESS'
    ]

ARCHITECTURE: Final[str] = platform.machine()
PROCESSOR: Final[str] = platform.processor()

PLATFORM: Final[str] = platform.system()
PLATFORM_RELEASE: Final[str] = platform.release()
PLATFORM_VERSION: Final[str] = platform.version()

PLATFORM_IS_LINUX: Final[bool] = PLATFORM == 'Linux'
PLATFORM_IS_WINDOWS: Final[bool] = PLATFORM == 'Window'

CPU_COUNT: Final[int] = psutil.cpu_count()
RAM: Final[str] = str(round(psutil.virtual_memory().total / (1024.0 ** 3), 2)) + " GB"

HOSTNAME: Final[str] = socket.gethostname()
IP_ADDRESS: Final[str] = socket.gethostbyname(socket.gethostname())
MAC_ADDRESS: Final[str] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))



# IsRaspberryPi = FilePath.FromString('/boot/config.txt').Exists
