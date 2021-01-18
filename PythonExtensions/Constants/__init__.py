import platform
import re
import socket
import uuid

import psutil




__all__ = [
    'ARCHITECTURE', 'PROCESSOR',
    'PLATFORM', 'PLATFORM_RELEASE', 'PLATFORM_VERSION',
    'PLATFORM_IS_LINUX', 'PLATFORM_IS_WINDOWS',
    'CPU_COUNT', 'RAM',
    'HOSTNAME', 'IP_ADDRESS', 'MAC_ADDRESS'
    ]

ARCHITECTURE = platform.machine()
PROCESSOR = platform.processor()

PLATFORM = platform.system()
PLATFORM_RELEASE = platform.release()
PLATFORM_VERSION = platform.version()

PLATFORM_IS_LINUX = PLATFORM == 'Linux'
PLATFORM_IS_WINDOWS = PLATFORM == 'Window'

CPU_COUNT = psutil.cpu_count()
RAM = str(round(psutil.virtual_memory().total / (1024.0 ** 3), 2)) + " GB"

HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
MAC_ADDRESS = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
