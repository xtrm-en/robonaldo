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
                print_strategies()
                return (True, "")
            return (False, "Invalid argument")

        return (False, "Invalid command arguments")

    def print_strategies(self) -> None:
        for strat in StrategyManager().strategies:
            prefix = ""
            if StrategyManager().is_enabled(strat):
                prefix = '[✓] '
            else:
                prefix = '[✗] '
            print(prefix + strat.id)
                

    def description(self) -> str:
        return "Strategy management"

    def usages(self) -> List[str]:
        return ["%NAME% <list>", "%NAME% <toggle/enable/disable> <strat_id>", "%NAME% <toggle/enable/disable> all"]

    def aliases(self) -> List[str]:
        return ["strat"]

CommandManager().register(Strategy(), "strategy")