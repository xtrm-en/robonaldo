from robonaldo.cli.command import Command, CommandContext, register, by_name, commands
from typing import List


class Stop(Command):
    def execute(self, ctx: CommandContext) -> bool:
        ctx.robonaldo.stop()

        return (True, "")

    def description(self) -> str:
        return "Stops the current game"

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return ["end"]


register(Stop(), "stop")
