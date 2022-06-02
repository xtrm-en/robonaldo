from ... import config

import logging
import rsk
import time
from typing import List, Callable


class NetworkManager:
    """Handles the connections between Robonaldo and the rsk server."""

    def __init__(self):
        self.__log = logging.getLogger("robonaldo-network")
        self.__client: rsk.Client = None
        self.__connected = False

        self.__update_hooks: List[Callable[[rsk.Client, float], None]] = []

        self.__server_ip = None
        self.__client_key = None

        self.__autoconnect = False

    @property
    def connected(self) -> bool:
        return self.__connected

    @property
    def client(self) -> rsk.Client:
        self.__require_connection()
        return self.__client

    @property
    def ip(self) -> str:
        return self.__server_ip

    @property
    def key(self) -> str:
        return self.__client_key

    @property
    def hooks(self) -> List[Callable[[rsk.Client, float], None]]:
        return self.__update_hooks

    # This theoretically could be removed by exclusively
    # using the configuration module, but me likey cool log in console :D
    def set_server(
        self,
        server_ip: str = None,
        client_key: str = None,
    ) -> None:
        self.__autoconnect = config.cfg["rsk.client.autoconnect"]
        self.__server_ip = (
            server_ip if server_ip is not None else config.cfg["rsk.server.ip"]
        )
        self.__client_key = (
            client_key
            if client_key is not None
            else config.default("rsk.client.key", None)
        )

        self.__log.info(
            (
                "Setting server to %s"
                + (
                    (" (Key: '%s')" % self.__client_key)
                    if self.__client_key is not None
                    else ""
                )
            )
            % self.__server_ip
        )

        config.cfg["rsk.server.ip"] = self.__server_ip
        config.cfg["rsk.client.key"] = self.__client_key

        if self.__autoconnect:
            self.connect(True)

    def connect(self, wait: bool = True, is_autoconnect: bool = False) -> bool:
        if self.__connected:
            self.disconnect()

        key = self.__client_key if self.__client_key is not None else ""

        self.__log.info(("Auto-" if is_autoconnect else "") + "Connecting...")
        self.__client = rsk.Client(host=self.__server_ip, key=key, wait_ready=False)

        if wait:
            self.__log.info("Waiting for client response...")

            timeout = False
            timeout_delay: int = 10
            t = time.time()
            while True:
                diff = time.time() - t
                if self.__client.sub_packets > 0:
                    break
                if diff > timeout_delay:
                    timeout = True
                    break

            if timeout:
                self.__log.error(
                    "Server didn't respond after %i seconds, not connected."
                    % timeout_delay
                )
                self.__client.stop()
                self.__client = None
                self.__connected = False
                return False

        self.__log.info("Successfully connected!")
        self.__connected = True
        self.__client.on_update = lambda client, delta: self.__dispatch_hooks(
            client, delta
        )
        return True

    def send(
        self, color: str, index: int, command: str, *parameters: List[object]
    ) -> str:
        if self.__client == None:
            raise Exception("Cannot send command from a disconnected client.")

        return self.__client.command(color.lower(), index, command, [*parameters])

    def disconnect(self) -> bool:
        self.__require_connection()
        self.__log.info("Disconnecting...")
        self.__client.stop()
        self.__client = None
        self.__connected = False

        self.__dispatch_hooks(None, -1)

    def __dispatch_hooks(self, client: rsk.Client, delta: float) -> None:
        for hook in self.__update_hooks:
            hook(client, delta)

    def __require_connection(self) -> None:
        if not self.__connected:
            raise Exception("Not connected to any server.")


NetworkManager.INSTANCE: NetworkManager = NetworkManager()
