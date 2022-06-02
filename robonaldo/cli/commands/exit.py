from robonaldo.cli.command import Command, CommandContext, register
from robonaldo.core.net import NetworkManager
import threading
from typing import List


class Exit(Command):
    def execute(self, ctx: CommandContext) -> bool:
        from robonaldo.cli import prompt

        ctx.robonaldo.stop()
        prompt.stop_prompt()

        return (True, "")

    def description(self) -> str:
        return "Exits the current session"

    def usages(self) -> List[str]:
        return ["%NAME% [page]", "%NAME% <command>"]

    def aliases(self) -> List[str]:
        return ["quit", "q", ":q"]  # vim gaming


register(Exit(), "exit")
