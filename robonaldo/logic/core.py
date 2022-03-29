import argparse

from robonaldo.context.robot import RobotColor, RobotOwnership
from robonaldo.context.updater import ContextUpdater
from robonaldo.network import NetworkHandler
from robonaldo.log import Logger, LogLevel

class Robonaldo:
    def __init__(self, team_color: RobotColor, host: str, key: str):
        self.__logger = Logger(name = 'Robonaldo')

        self.__logger.info("Defining color as " + team_color.name + ".")
        self.__color = team_color
        self.__teams = {
            team_color: RobotOwnership.ALLY,
            team_color.get_other(): RobotOwnership.ENEMY
        }

        self.__logger.info("Constructing logic core...")
        self.__nethandler = NetworkHandler(host = host, key = key)
        self.__updater = ContextUpdater(self.__nethandler)

    def initialize(self):
        self.__logger.info("Initializing NetworkHandler...")
        self.__nethandler.connect(wait = False)

        self.__logger.info("Initializing ContextUpdater")
        self.__updater.initialize()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("color", help="our team's color")
    parser.add_argument("host", help="the host controller IPv4 address")
    parser.add_argument("-k", "--key", type=str, help="the team's api key")
    args = parser.parse_args()
    
    color = RobotColor[args.color]
    host = args.host
    key = args.key
    if key is None:
        key = ''

    Robonaldo(team_color = color, host = host, key = key).initialize()