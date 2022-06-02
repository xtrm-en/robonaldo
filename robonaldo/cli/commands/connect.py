from robonaldo.cli.command import Command, CommandContext, register
from robonaldo import config
from typing import List


class Connect(Command):
    def execute(self, ctx: CommandContext) -> bool:
        if len(ctx.args) == 0:
            success = ctx.robonaldo.netmgr.connect()

            return (success, "")
        if len(ctx.args) == 1:
            ctx.robonaldo.netmgr.set_server(ctx.args[0])
            success = ctx.robonaldo.netmgr.connect()

            return (success, "")
        if len(ctx.args) == 2:
            ctx.robonaldo.netmgr.set_server(ctx.args[0], ctx.args[1])
            success = ctx.robonaldo.netmgr.connect()

            return (success, "")

        return (False, "Invalid command arguments")

    def description(self) -> str:
        return "Sets-up the connection with the server."

    def usages(self) -> List[str]:
        return ["%NAME%", "%NAME% <host>", "%NAME% <host> <key>"]

    def aliases(self) -> List[str]:
        return ["link"]


register(Connect(), "connect")
