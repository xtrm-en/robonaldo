from robonaldo.cli.command import Command, CommandContext, register, by_name, commands
from typing import List


class Start(Command):
    def execute(self, ctx: CommandContext) -> bool:
        ctx.robonaldo.start()

        return (True, "")

    def description(self) -> str:
        return "Starts the logic core."

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return ["run"]


register(Start(), "start")
