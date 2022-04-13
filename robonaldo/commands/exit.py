from robonaldo.command import Command, CommandContext
from robonaldo.command import CommandManager
from robonaldo.core import Robonaldo
import sys
from typing import List

class Exit(Command):
    def execute(self, ctx: CommandContext) -> bool:
        Robonaldo().stop()
        sys.exit(0)

        return (True, "")

    def description(self) -> str:
        return "Exits the current session"

    def usages(self) -> List[str]:
        return ["%NAME% [page]", "%NAME% <command>"]

    def aliases(self) -> List[str]:
        return ["quit", "q", ":q"] # vim gaming

CommandManager().register(Exit(), "exit")