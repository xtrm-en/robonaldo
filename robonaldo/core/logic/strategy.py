import logging
from threading import Thread
import time
from .dispatcher import Dispatcher
from ...utils.analysis.predict import Predict


class StrategyManager:
    def __init__(self):
        self.__log = logging.getLogger("strategy-manager")
        self.__dispatcher = Dispatcher()
        self.__running = False

    def start(self) -> None:
        self.__running = True

        self.__dispatcher.start(2)

        self.__thread = Thread(target=lambda: self.__run())
        self.__thread.start()

    def __run(self):
        predict = Predict()
        while self.__running:
            time.sleep(0.05)
            print(predict.delta())
        self.__dispatcher.stop()

    def stop(self) -> None:
        self.__running = False
