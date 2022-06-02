import logging
from .net import NetworkManager
from robonaldo.context import ContextUpdater, robots
from ..context.entities.robot import TeamColor
from .logic import StrategyManager
from .controller import RobotController
from .. import config


class Robonaldo:
    """Robonado's logic Core."""

    def __init__(self):
        self.__log = logging.getLogger("robonaldo-core")
        self.__log.info("Constructing Robonaldo...")

        NetworkManager.INSTANCE.set_server()  # set based on config

        # NetworkManager.INSTANCE = self.__netmgr

        self.__ctxupdater = ContextUpdater()
        NetworkManager.INSTANCE.hooks.append(
            lambda client, delta: self.__ctxupdater.handle_update(client, delta)
        )

        self.__stratmgr = StrategyManager()

        self.__running = False
        # self.__gameanalyser = GameAnalyser()

    @property
    def running(self) -> bool:
        return self.__running

    def start(self):
        # To start Robonaldo, we need a few things set:
        # - A proper server connection
        # - A team color
        # - 2 robots on our team

        team = config.cfg["rsk.client.color"]

        if not NetworkManager.INSTANCE.connected:
            NetworkManager.INSTANCE.connect()

        assert NetworkManager.INSTANCE.connected, "Must be connected to the RSK server."
        assert type(team) == TeamColor, "Team must be valid."
        assert len(robots.for_team(team)) == 2, "Must have 2 robots in game."

        self.__log.info("Starting logic core...")
        self.__stratmgr.start()

        self.__running = True

    def stop(self) -> None:
        self.__log.info("Stopping Robonaldo...")

        self.__stratmgr.stop()
        # self.__dispatcher.set_enabled(False)
        # self.__dispatcher.stop_all()

        for robot in robots.ally:
            robot.controller.stop()

        if NetworkManager.INSTANCE.connected:
            NetworkManager.INSTANCE.disconnect()

        self.__running = False

    @property
    def stratmgr(self) -> StrategyManager:
        return self.__stratmgr
