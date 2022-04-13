from robonaldo.command import Command, CommandContext
from robonaldo.command import CommandManager
from robonaldo.controller import GameController
import sys
from typing import List

class Emergency(Command):
    def execute(self, ctx: CommandContext) -> bool:
        for robot in GameController().controllers:
            robot.control(0, 0, 0)

        return (True, "")

    def description(self) -> str:
        return "Stops all robots"

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return ["fuck"]

CommandManager().register(Emergency(), "emergency")