from enum import Enum
from distutils.util import strtobool
from robonaldo.cli.command import Command, CommandContext, register
from robonaldo import config
from typing import List


class Config(Command):
    def execute(self, ctx: CommandContext) -> bool:
        if len(ctx.args) == 0:
            msg = "Displaying current configuration"
            print(msg)
            print("-" * len(msg))

            split_cfg = config.split(config.cfg)

            global_vals = {}
            sub_vals = {}

            for key, val in split_cfg.items():
                if type(val) != dict:
                    global_vals[key] = val
                else:
                    sub_vals[key] = val

            if len(global_vals) > 0:
                self.__display_category("global", global_vals, 0)

            for key, val in sub_vals.items():
                self.__display_category(key, val, 0)

            return (True, "")

        if len(ctx.args) == 1:
            node = ctx.args[0]
            if node in config.cfg:
                val = config.cfg[node]
                if type(val) == dict:
                    # FIXME: this doesnt occur even once, because we're using
                    # the joined/original cfg, but the split cfg doesnt have
                    # mid level dicts, so we need to rewrite this entire part
                    self.__display_category(node, val, 0)
                else:
                    print(node + ":", val, "(Type: '%s')" % str(type(val)))

                return (True, "")
            return (False, "Unknown configuration node: '%s'" % node)

        if len(ctx.args) == 2:
            node = ctx.args[0]
            if node in config.cfg:
                val = config.cfg[node]
                val_type = type(val)
                new_val = ctx.args[1]
                try:
                    # this is horrible
                    # TODO: better code here
                    if issubclass(val_type, Enum):
                        new_val = val_type[new_val]
                    elif val_type == bool:
                        new_val = bool(strtobool(new_val))
                    else:
                        new_val = val_type(new_val)

                    config.cfg[node] = new_val

                    print("Successfully set '%s' to '%s'." % (node, str(new_val)))

                    config.save_config()
                    return (True, "")
                except:
                    return (
                        False,
                        "Invalid new value '%s' for type %s." % (new_val, val_type),
                    )
            return (False, "Unknown configuration node: '%s'" % node)

        return (False, "Invalid command arguments")

    def __display_category(self, name: str, category: dict, spacing: int) -> None:
        item_chr = "· "
        cat_chr = "- "

        print((" " * spacing) + (cat_chr if spacing != 0 else "") + name + ":")
        spacing += 2

        def prnt(string: str) -> None:
            print((" " * spacing) + string)

        for key, val in category.items():
            if type(val) == dict:
                self.__display_category(key, val, spacing)
            else:
                prnt(item_chr + "%s: %s" % (key, str(val)))

    def description(self) -> str:
        return "Interact with the configuration."

    def usages(self) -> List[str]:
        return ["%NAME%", "%NAME% <key>", "%NAME% <key> <value>"]

    def aliases(self) -> List[str]:
        return ["cfg", "settings", "s"]


register(Config(), "config")
