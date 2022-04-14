from argparse import ArgumentParser

from robonaldo.context.robot import RobotColor, RobotOwnership
from robonaldo.context.updater import ContextUpdater
from robonaldo.controller import GameController
from robonaldo.log import Logger, LogLevel
from robonaldo.network import NetworkHandler
from robonaldo.strategy import StrategyManager
from robonaldo.utils import Singleton

class Robonaldo(metaclass = Singleton):
    __constructed = False
    __connected = False
    __initialized = False

    def construct(self) -> None:
        if self.__constructed is True:
            return
        self.__constructed = True

        self.__logger = Logger(name = 'Robonaldo')

        self.__logger.info("Setting up NetworkHandler...")
        self.network_handler = NetworkHandler()
        self.__logger.info("Setting up ContextUpdater...")
        self.context_updater = ContextUpdater(self.network_handler)

        self.__logger.info("Initializing GameController with NetworkHandler...")
        GameController().set_network(self.network_handler)

        # self.__logger.info("Setting up StrategyManager...")
        # StrategyManager().construct()
 
    def connect(self, host: str, key: str) -> None:
        self.__logger.info("Initializing connection to the server...")
        self.network_handler.connect(host = host, key = key, wait = True)
        self.__logger.info("Connection established.")

        self.__connected = True

    def initialize(self, team_color: RobotColor, side: int = 1) -> None:
        if self.__connected is not True:
            self.__logger.error("Robonaldo client not connected to a server!")
            return

        self.side = side

        if self.__initialized is True:
            return
        self.__initialized = True

        self.__logger.info("Defining color as " + team_color.name + ".")
        self.team_color = team_color
        self.ally_map = {
            team_color: RobotOwnership.ALLY,
            team_color.get_other(): RobotOwnership.ENEMY
        }

        self.__logger.info("Initializing ContextUpdater...")
        self.context_updater.initialize()
        
        self.__logger.info("Registering StrategyManager to ContextUpdater...")
        StrategyManager().register_on(self.context_updater)

        self.__logger.info("Let's rock.")

    def stop(self) -> None:
        self.__logger.info("Stopping...")
        for robot in GameController().controllers:
            try:
                robot.control(0, 0, 0)
            except:
                # might not have da key, who cares
                pass

        self.network_handler.close()

        if StrategyManager().attack_thread is not None:
            StrategyManager().attack_thread.stop()
        if StrategyManager().defense_thread is not None:
            StrategyManager().defense_thread.stop()


Robonaldo().construct()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("color", help="our team's color")
    parser.add_argument("host", help="the host controller IPv4 address")
    parser.add_argument("-k", "--key", type=str, help="the team's api key")
    args = parser.parse_args()
    
    color = RobotColor[args.color]
    host = args.host
    key = args.key
    if key is None:
        key = ''

    Robonaldo().initialize(team_color = color, host = host, key = key)