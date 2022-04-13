from robonaldo.command import Command, CommandContext
from robonaldo.command import CommandManager
from robonaldo.controller import GameController
from robonaldo.core import Robonaldo
import sys
from typing import List

class Stop(Command):
    def execute(self, ctx: CommandContext) -> bool:
        Robonaldo().stop()

        return (True, "")

    def description(self) -> str:
        return "Stops the current game"

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return ["end"]

CommandManager().register(Stop(), "stop")