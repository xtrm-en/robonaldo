from robonaldo.command import Command, CommandContext
from robonaldo.command import CommandManager
from robonaldo.core import Robonaldo
import sys
from typing import List

class Help(Command):
    def execute(self, ctx: CommandContext) -> bool:
        if len(ctx.args) == 0:
            self.print_commands()
            return (True, "")
        
        if len(ctx.args) == 1:
            primary = ctx.args[0]
            name = str(primary)
            cmd = CommandManager().by_name(name)
            if cmd is not None:
                self.print_command(name, cmd)
                return (True, "")
            return (False, "Unknown command '" + name + "'")

        return (False, "Invalid command arguments")

    def print_commands(self) -> None:
        for name, cmd in CommandManager().commands.items():
            desc = ""
            if cmd.description() is not None:
                desc = " - " + cmd.description()
            print(name + desc)

    def print_command(self, name: str, command: Command) -> None:
        desc = ""
        if command.description() is not None:
            desc = " - " + command.description()

        print(name + desc)
        print("Usages:")
        for u in command.usages():
            print(">", u.replace("%NAME%", name))

    def description(self) -> str:
        return "Gives help related to Robonaldo's commands"

    def usages(self) -> List[str]:
        return ["%NAME%", "%NAME% <command>"]

    def aliases(self) -> List[str]:
        return ["h", "?"]

CommandManager().register(Help(), "help")