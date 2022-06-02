from robonaldo.cli.command import Command, CommandContext, register, commands, by_name
from typing import List


class Help(Command):
    def execute(self, ctx: CommandContext) -> bool:
        if len(ctx.args) == 0:
            self.print_commands()
            return (True, "")

        if len(ctx.args) == 1:
            primary = ctx.args[0]
            name = str(primary)
            cmd = by_name(name)
            if cmd is not None:
                self.print_command(name, cmd)
                return (True, "")
            return (False, "Unknown command '" + name + "'")

        return (False, "Invalid command arguments")

    def print_commands(self) -> None:
        for name, cmd in commands.items():
            desc = ""
            if cmd.description() is not None:
                desc = " - " + cmd.description()
            print(name + desc)

    def print_command(self, name: str, command: Command) -> None:
        desc = ""
        if command.description() is not None:
            desc = " - " + command.description()

        def get_original_name():
            for n, cmd in commands.items():
                if cmd == command:
                    return n
            raise Exception("fuck.")

        print(name + desc)
        print("Aliases:", ", ".join([get_original_name()] + command.aliases()))
        print("Usages:")
        for u in command.usages():
            print(">", u.replace("%NAME%", name))

    def description(self) -> str:
        return "Gives help related to Robonaldo's commands"

    def usages(self) -> List[str]:
        return ["%NAME%", "%NAME% <command>"]

    def aliases(self) -> List[str]:
        return ["h", "?", ":help", ":h"]


register(Help(), "help")
