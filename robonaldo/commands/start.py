from robonaldo.command import Command, CommandContext
from robonaldo.command import CommandManager
from robonaldo.context.robot import RobotColor
from robonaldo.core import Robonaldo
import sys
from typing import List

class Start(Command):
    def execute(self, ctx: CommandContext) -> bool:
        if len(ctx.args) == 1:
            Robonaldo().initialize(RobotColor[ctx.args[0].upper()])
            return (True, "")

        return (False, "Invalid command arguments")

    def description(self) -> str:
        return "Starts the match."

    def usages(self) -> List[str]:
        return ["%NAME% <blue/green>"]

    def aliases(self) -> List[str]:
        return ["go"]

CommandManager().register(Start(), "start")