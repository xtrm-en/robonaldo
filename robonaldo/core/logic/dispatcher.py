from attrs import define
import logging
from threading import Thread
from typing import Callable, List


class Dispatcher:
    def __init__(self, nthread: int = 2):
        self.__log = logging.getLogger("robonaldo-dispatcher")
        self.__threads: List[RobonaldoThread] = []

    def start(self, nthread: int) -> None:
        self.__log.info("Initializing Dispatcher with %i threads." % nthread)
        for _ in range(nthread):
            self.__threads.append(RobonaldoThread())

    def stop(self) -> None:
        for thread in self.__threads:
            thread.stop()
        self.__threads = []


class RobonaldoThread(Thread):
    def __init__(self):
        self.queue: List[Callable[["RobonaldoThread"], bool]] = []
        self.running = True

        super().__init__(target=self.__exec)
        super().setDaemon(True)
        super().start()

    def __exec(self) -> None:
        while self.running:
            if len(self.queue) > 0:
                task = self.queue.pop(0)
                task(self)

    def sync(self):
        super().join()

    def stop(self):
        self.running = False
