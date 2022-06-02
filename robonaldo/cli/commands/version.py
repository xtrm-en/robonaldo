from robonaldo.cli.command import Command, CommandContext, register
from typing import List
from robonaldo.launcher import propaganda


class Version(Command):
    def execute(self, ctx: CommandContext) -> bool:
        propaganda(logger="robonaldo-command", prefix="")

        return (True, "")

    def description(self) -> str:
        return "Gets the version information."

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return ["ver", "v"]


register(Version(), "version")
