from robonaldo.cli.command import Command, CommandContext, register
from typing import List
from robonaldo.context import ball


class Context(Command):
    def execute(self, cmd: CommandContext) -> bool:
        if cmd.robonaldo.netmgr.connected:
            print(ball)

            return (True, "")

        return (False, "Client must be connected to check the game context.")

    def description(self) -> str:
        return "Check the game context."

    def usages(self) -> List[str]:
        return ["%NAME%"]

    def aliases(self) -> List[str]:
        return ["ctx", "info"]  # vim gaming


register(Context(), "context")
