import logging


def propaganda(logger: str = "robonaldo-launcher", prefix: str = "Launching "):
    from . import __title__, __version__, __copyright__

    log = logging.getLogger(logger)
    log.info(prefix + "%s v%s." % (__title__, __version__))
    log.info(__copyright__)


if __name__ == "__main__":
    # Logging config
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    propaganda()

    # Load Config
    from . import config

    config.load_config()

    from argparse import ArgumentParser
    from distutils.util import strtobool
    import sys
    import threading
    import time
    from .core.robonaldo import Robonaldo
    from .webui import server
    from .cli import prompt
    from .context.entities.robot import TeamColor

    # Argument Parsing
    parser = ArgumentParser()

    # Game Configuration
    color_def: TeamColor = None
    try:
        color_def = TeamColor[config.cfg["rsk.client.color"]]
    except:
        color_def = TeamColor.BLUE
    autostart_def: bool = config.default("logic.autostart", False)

    parser.add_argument(
        "--team-color",
        "-c",
        type=TeamColor,
        help="The current team color.",
        default=color_def,
    )
    parser.add_argument(
        "--autostart",
        "-as",
        type=lambda x: bool(strtobool(x)),
        help="Whether to automatically start Robonaldo's logic core.",
        default=autostart_def,
    )

    # Server Info
    ip_def = config.default("rsk.server.ip", "172.19.39.223")
    key_def = config.default("rsk.client.key", None)
    autoconnect_def = config.default("rsk.client.autoconnect", True)

    parser.add_argument(
        "--ip",
        "-ip",
        type=str,
        help="The server IP to connect to.",
        default=ip_def,
    )
    parser.add_argument(
        "--key",
        "-k",
        type=str,
        help="The client KEY to connect with.",
        default=key_def,
    )
    parser.add_argument(
        "--autoconnect",
        "-ac",
        type=lambda x: bool(strtobool(x)),
        help="Whether to automatically connect to the server.",
        default=autoconnect_def,
    )

    # WebUI
    w_def = config.default("webui.enabled", True)
    w_ip_def = config.default("webui.ip", "127.0.0.1")
    w_p_def = config.default("webui.port", "6969")

    parser.add_argument(
        "--web-ui",
        "-web",
        "-ui",
        type=lambda x: bool(strtobool(x)),
        help="Whether to enable the WebUI controller.",
        default=w_def,
    )
    parser.add_argument(
        "--web-ui-ip",
        "-ui-ip",
        type=str,
        help="The WebUI IP to listen to.",
        default=w_ip_def,
    )
    parser.add_argument(
        "--web-ui-port",
        "-ui-p",
        type=str,
        help="The WebUI PORT to listen to.",
        default=w_p_def,
    )
    args = parser.parse_args()

    # Save new config
    config.cfg["logic.autostart"] = args.autostart
    config.cfg["rsk.client.color"] = args.team_color

    config.cfg["rsk.server.ip"] = args.ip
    config.cfg["rsk.client.key"] = args.key
    config.cfg["rsk.client.autoconnect"] = args.autoconnect

    config.cfg["webui.enabled"] = args.web_ui
    config.cfg["webui.ip"] = args.web_ui_ip
    config.cfg["webui.port"] = args.web_ui_port

    config.save_config()

    # Instantiate Robonaldo's core
    robonaldo = Robonaldo()

    # Delegate to the appropriate service manager
    if config.cfg["webui.enabled"]:
        logger.warn("WebUI is yet to be implemented properly, we recommend using the cli")
        server.initialize(robonaldo)
        server.serve()
    else:
        prompt.initialize(robonaldo)
        prompt.serve()
