from robonaldo.command import Command, CommandContext
from robonaldo.command import CommandManager
from robonaldo.context.robot import RobotColor
from robonaldo.core import Robonaldo
import sys
from typing import List

class Connect(Command):
    def execute(self, ctx: CommandContext) -> bool:
        if len(ctx.args) == 2:
            Robonaldo().connect(ctx.args[0], ctx.args[1])
            return (True, "")

        return (False, "Invalid command arguments")

    def description(self) -> str:
        return "Sets-up the connection with the server."

    def usages(self) -> List[str]:
        return ["%NAME% <host> [key]"]

    def aliases(self) -> List[str]:
        return ["link"]

CommandManager().register(Connect(), "connect")