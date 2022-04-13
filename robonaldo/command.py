import os
from robonaldo.log import Logger, LogLevel
from robonaldo.utils import Singleton
import sys
from typing import List, Tuple


class CommandContext:
    """Wrapper class for all informations required for a command
    """

    def __init__(self, command: str, arguments: List[str]):
        self.__command = command
        self.__arguments = arguments

    @property
    def cmd(self) -> str:
        return self.__command

    @property
    def args(self) -> List[str]:
        return self.__arguments


class Command():
    def execute(self, ctx: CommandContext) -> Tuple[bool, str]:
        raise Exception("Unimplemented command.")

    def description(self) -> str:
        return None

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return []


class CommandManager(metaclass=Singleton):
    __target = 'robonaldo/commands'
    __logger = Logger("CommandManager", priority = LogLevel.TRACE)
    commands = {}
    __cmd_lookup = {}

    def register_all(self):
        sys.path.append(self.__target)
        for file in os.listdir(self.__target):
            if '.py' in file and '.pyc' not in file and '__' not in file:
                name = file.replace('.py', '')
                __import__(name)

    def register(self, command: Command, name: str):
        self.__logger.trace("Registering command \'" + name + "\'.")
        self.commands[name] = command

    def by_name(self, name: str) -> Command:
        result = self.__cmd_lookup.get(name)
        if result is None:
            result = self.commands.get(name)
            if result is None:
                for cmd in self.commands.values():
                    if name.lower() in cmd.aliases():
                        result = cmd
                        break
            self.__cmd_lookup[name] = result
        return result

    def handle(self, command: str) -> Tuple[bool, str]:
        tokens = command.split(" ")
        cmd = tokens[0]

        handler = self.by_name(cmd)
        if handler is not None:            
            args = tokens[1:]

            ctx = CommandContext(cmd, args)

            try:
                return handler.execute(ctx)
            except Exception as e:
                return (False, str(e))

        return (False, "Unknown command '" + cmd + "'.")
