from typing import List

try:
    import rsk2 as rsk
except:
    import rsk

from .context.robot import RobotColor


class NetworkHandler:
    def __init__(self, host: str, key: str = ''):
        self.__host = host
        self.__key = key
        self.__client = None

    def connect(self, wait: bool = True) -> None:
        self.__client = rsk.Client(host = self.__host, key = self.__key, wait_ready = wait)

    def close(self) -> None:
        self.__client.stop()
        self.__client = None

    def set_hook(self, hook) -> None:
        self.__client.on_update = hook

    def send(self, robot_color: RobotColor, robot_index: int, command: str, parameters: List[object]) -> str:
        if self.__client == None:
            raise Exception("Cannot send command from a disconnected client.")

        self.__client.lock.acquire()
        self.__client.req.send_json([self.__key, robot_color.name.lower(), robot_index, [command, *parameters]])
        success, message = self.__client.req.recv_json()
        self.__client.lock.release()

        if not success:
            raise rsk.client.ClientError('Command "' + command + '" failed: ' + message)
        
        return message