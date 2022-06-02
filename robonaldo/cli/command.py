from attrs import frozen
import logging
import os
import sys
import traceback
from typing import List, Tuple
from ..core.robonaldo import Robonaldo


@frozen
class CommandContext:
    """Wrapper class for all informations required for a command"""

    cmd: str
    args: List[str]
    robonaldo: Robonaldo


class Command:
    def execute(self, ctx: CommandContext) -> Tuple[bool, str]:
        raise Exception("Unimplemented command.")

    def description(self) -> str:
        return None

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return []


__target = "robonaldo/cli/commands"
__log = logging.getLogger("robonaldo-command")
commands = {}
__cmd_lookup = {}


def register_all():
    sys.path.append(__target)
    for file in os.listdir(__target):
        if ".py" in file and ".pyc" not in file and "__" not in file:
            name = file.replace(".py", "")
            __import__(name)

    global commands

    __log.info(
        "Registered %s commands: %s" % (len(commands), ", ".join(commands.keys()))
    )


def register(command: Command, name: str):
    global commands

    __log.debug("Registering command '" + name + "'.")
    commands[name] = command


def by_name(name: str) -> Command:
    global commands

    result = __cmd_lookup.get(name)
    if result is None:
        result = commands.get(name)
        if result is None:
            for cmd in commands.values():
                if name.lower() in cmd.aliases():
                    result = cmd
                    break
        __cmd_lookup[name] = result
    return result


def handle(command: str, robonaldo: Robonaldo) -> Tuple[bool, str]:
    tokens = command.split(" ")
    cmd = tokens[0]

    handler = by_name(cmd)
    if handler is not None:
        args = tokens[1:]

        ctx = CommandContext(cmd, args, robonaldo)

        try:
            return handler.execute(ctx)
        except Exception as _:
            traceback.print_exc()
            return (False, "")

    return (False, "Unknown command '" + cmd + "'.")
