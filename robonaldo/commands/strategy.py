from robonaldo.command import Command, CommandContext
from robonaldo.command import CommandManager
from robonaldo.controller import GameController
from robonaldo.strategy import StrategyManager
import sys
from typing import List

class Strategy(Command):
    def execute(self, ctx: CommandContext) -> bool:
        if len(ctx.args) == 1:
            if ctx.args[0] == "list":
                self.print_strategies()
                return (True, "")
            return (False, "Invalid command argument")
        if len(ctx.args) == 2:
            if ctx.args[0] == "toggle":
                strat_id = 
                pass
            if ctx.args[0] == "enable":
                pass
            if ctx.args[0] == "disable":
                pass

            return (False, "Invalid argument '" + ctx.args[0] + "'")

        return (False, "Invalid command arguments")

    def print_strategies(self) -> None:
        for strat in StrategyManager().strategies.values():
            if StrategyManager().is_enabled(strat):
                suffix = '[✓]'
            else:
                suffix = '[✗]'
            print(">", strat.id, suffix)
                

    def description(self) -> str:
        return "Strategy management"

    def usages(self) -> List[str]:
        return ["%NAME% list", "%NAME% <toggle/enable/disable> <strat_id>", "%NAME% <toggle/enable/disable> all"]

    def aliases(self) -> List[str]:
        return ["strat"]

CommandManager().register(Strategy(), "strategy")