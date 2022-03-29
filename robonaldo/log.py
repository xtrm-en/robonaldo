import time
from enum import Enum

class LogLevel(Enum):
    INFO = 10
    WARN = 20
    ERROR = 30
    FATAL = 40
    DEBUG = 0

    def __init__(self, priority: int):
        self.__priority = priority

    def get_priority(self) -> int:
        return self.__priority

class Logger:
    def __init__(self, name: str, priority: LogLevel = LogLevel.INFO):
        self.__name = name
        self.__min_lvl = priority

    def set_min_level(self, level: LogLevel) -> None:
        self.__min_lvl = level

    def log(self, level: LogLevel, message: object) -> None:
        if level.get_priority() < self.__min_lvl.get_priority():
            return

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("[" + current_time + "] [" + self.__name + "/" + level.name + "]", message)

    def info(self, message: object) -> None:
        self.log(LogLevel.INFO, message)

    def warn(self, message: object) -> None:
        self.log(LogLevel.WARN, message)

    def error(self, message: object) -> None:
        self.log(LogLevel.ERROR, message)

    def fatal(self, message: object) -> None:
        self.log(LogLevel.FATAL, message)

    def debug(self, message: object) -> None:
        self.log(LogLevel.DEBUG, message)