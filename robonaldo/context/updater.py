try:
    import rsk2 as rsk
except:
    import rsk

from robonaldo.log import Logger, LogLevel
from robonaldo.network import NetworkHandler
from robonaldo.context.game import GameContext, Terrain, Ball

class ContextUpdater():
    def __init__(self, net_handler: NetworkHandler):
        self.__logger = Logger(name = "ContextUpdater", priority = LogLevel.DEBUG)

        self.__nethandler = net_handler
        self.__ctx = None
        
        self.__audience = []


    def initialize(self) -> None:
        self.__logger.info("Setting context hook...")
        self.__nethandler.set_hook(lambda cl, dt: self.dispatch_context(cl, dt))
        

    def register(self, listener) -> None:
        self.__audience.append(listener)

    
    def unregister(self, listener) -> None:
        self.__audience.remove(listener)


    def dispatch_context(self, client: rsk.Client, deltaTime: float):
        self.__logger.debug("Dispatching context")
        self.update_context(client, deltaTime)

        for listener in self.__audience:
            listener(self.__ctx, deltaTime)

        
    def update_context(self, client: rsk.Client, deltaTime: float):
        if self.__ctx is None:
            self.__ctx = GameContext()

