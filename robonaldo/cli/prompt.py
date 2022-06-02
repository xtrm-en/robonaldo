import logging
from ..core.robonaldo import Robonaldo
from . import command as manager


__log = logging.getLogger("robonaldo-cli")
robonaldo: Robonaldo = None
__running = True


def stop_prompt(value: bool = False):
    global __running

    __running = value


def initialize(r: Robonaldo) -> None:
    global robonaldo
    robonaldo = r

    manager.register_all()


def serve() -> None:
    assert robonaldo != None, "what the fuck"

    __log.info("Serving on CLI Prompt.")

    success = None
    while __running:
        prefix = "[?] "
        if success is not None:
            if success:
                prefix = "[✓] "
            else:
                prefix = "[✗] "

        print(prefix + "Enter a command [help] > ", end="")

        command = input().strip()
        if len(command) > 0:
            result, message = manager.handle(command, robonaldo)

            if not result and len(message) > 0:
                print(message)

            success = result
