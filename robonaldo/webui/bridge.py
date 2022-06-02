from flask import jsonify, request
import inspect
import json
import logging
from rsk import constants
import typing
from ..core.robonaldo import Robonaldo
from .. import config
from ..context import ball, robots


class BridgeAPI:
    """Exposes Robonaldo's internal APIs and rsk's APIs to the WebUI."""

    def __init__(self, robonaldo: Robonaldo):
        self.__robonaldo = robonaldo
        self.__log = logging.getLogger("robonaldo-bridge")

        self.__cached_consts = {}

        self.__methods = {}

        # Taken from rsk.api
        for name, member in inspect.getmembers(self):
            if not name.startswith("_") and callable(member):
                hints = typing.get_type_hints(member)
                args = inspect.signature(member).parameters.keys()
                args = list(map(lambda name: hints.get(name, None), args))
                result = hints.get("return", None)

                self.__methods[member.__name__] = {
                    "func": member,
                    "args": args,
                    "result": result,
                }

    def __require_connection(self):
        if self.__robonaldo.netmgr.connected:
            raise Exception("Not connected to a server.")

    def get_connection_data(self) -> object:
        return {
            "ip": self.__robonaldo.netmgr.ip,
            "key": self.__robonaldo.netmgr.key,
        }

    def set_connection_data(self, ip: str, key: str) -> None:
        self.__robonaldo.netmgr.ip = ip
        self.__robonaldo.netmgr.key = key

    def is_connected(self) -> bool:
        return self.__robonaldo.netmgr.connected

    def get_robots(self) -> object:
        self.__require_connection()

        result_data = {}
        for robot in robots:
            data = {
                "index": robot.index,
                "team": robot.color,
                "position": [robot.x, robot.y],
                "orientation": robot.orientation,
                "owned": robot.color == config.cfg["rsk.client.color"],
                "ghost": robot.is_ghost,
                "last_updated": robot.last_updated,
            }
            result_data[robot.identifier] = data

        return result_data

    def get_ball(self) -> object:
        self.__require_connection()

        return {
            "position": [ball.x, ball.y],
            "ghost": ball.is_ghost,
            "last_updated": ball.last_updated,
        }

    def __cache_data(self) -> object:
        if len(self.__cached_consts) == 0:
            for key, member in inspect.getmembers(constants):
                if key.startswith("_"):
                    continue

                value = getattr(constants, key)
                if type(value) == type(constants):
                    continue

                if callable(member):
                    hints = typing.get_type_hints(member)
                    args = inspect.signature(member).parameters.keys()
                    args = list(map(lambda name: hints.get(name, None), args))

                    value = member

                    if len(args) == 0:
                        self.__cached_consts[key] = value()
                    else:
                        if args[0] == bool:
                            self.__cached_consts[key + "_true"] = value(True)
                            self.__cached_consts[key + "_false"] = value(False)
                        elif args[0] == float:
                            for k in dir(constants):
                                v = getattr(constants, key)
                                if type(v) == float and "margin" in k:
                                    self.__cached_consts[key + "_" + k] = value(v)
                else:
                    self.__cached_consts[key] = value
        return self.__cached_consts

    def get_constants(self) -> object:
        return self.__cache_data()

    def _handle_request(self, command: str, *args) -> object:
        chr = "'" if len(args) > 0 else ""
        start = " / " if len(args) > 0 else ""
        self.__log.info("%s%s" % (command, start + chr + "', '".join(list(args)) + chr))

        if command not in self.__methods:
            return False

        method = self.__methods[command]

        a = list(args)
        try:
            m_args = method["args"]
            for i in range(len(m_args)):
                if m_args[i] is not None:
                    arg_type = m_args[i]
                    arg = args[i]
                    arg = arg_type(arg)
                    a[i] = arg
        except ValueError:
            return True

        func = method["func"]
        return func(*a)


if __name__ == "__main__":
    print(BridgeAPI(None).get_constants())
