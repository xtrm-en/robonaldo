from robonaldo.cli.command import Command, CommandContext, register
from robonaldo.context import robots
import traceback
from typing import List


class Emergency(Command):
    def execute(self, ctx: CommandContext) -> bool:
        for robot in robots.all:
            try:
                robot.controller.stop()
            except Exception as _:
                traceback.print_exc()

        return (True, "")

    def description(self) -> str:
        return "Stops all robots"

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return ["fuck", "deadlock"]


register(Emergency(), "emergency")
