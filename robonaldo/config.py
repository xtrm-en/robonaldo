"""The Robonaldo global configuration definition.
"""
from appdirs import AppDirs
import logging
import os
import time
import toml
from . import __title__, __username__, __version__
from .utils.parsing.encoders import TomlEnumEncoder


__dirs = AppDirs(__title__, __username__, version=__version__)
__config_dir = __dirs.user_config_dir
__config_file = __config_dir + os.sep + "config.toml"
cfg = {}
if not os.path.exists(__config_dir):
    os.makedirs(__config_dir)

__log = logging.getLogger("robonaldo-config")
__log.info("Setting config file to: '%s'" % __config_file)


def save_config() -> None:
    if os.path.exists(__config_file):
        os.remove(__config_file)

    __log.debug("Saving config...")
    with open(__config_file, "w+") as f:
        toml.dump(split(cfg), f, encoder=TomlEnumEncoder())


def load_config() -> None:
    global cfg

    __log.debug("Loading config...")
    if not os.path.exists(__config_file):
        save_config()

    with open(__config_file, "r") as f:
        cfg = join(toml.load(f))


def default(key: str, default: object) -> object:
    global cfg

    return default if key not in cfg else cfg[key]


def split(input_dict: dict) -> dict:
    splt_chr = "."

    # Adapted from https://www.geeksforgeeks.org/python-group-hierarachy-splits-of-keys-in-dictionary/
    def internal_split(dictionary: dict) -> dict:
        res = dict()
        for key, val in dictionary.items():
            if type(val) == dict:
                # recursivly check for nested dicts
                val = internal_split(val)

            # prevent errors for already processed keys
            if splt_chr not in key:
                res[key] = val
                continue

            items = key.split(splt_chr)
            ini_key = items[0]
            low_key = ""
            for item in items[1:]:
                low_key += item + splt_chr
            low_key = low_key[0 : len(low_key) - 1]

            # check if key already present
            if ini_key not in res:
                res[ini_key] = dict()

            # add nested value if present key
            res[ini_key][low_key] = val

            res = internal_split(res)
        return res

    return internal_split(input_dict)


def join(input_dict: dict):
    splt_chr = "."

    def internal_join(dictionary: dict, base_key: str) -> dict:
        res = dict()

        for key, val in dictionary.items():
            if type(val) == dict:
                d = internal_join(val, base_key + splt_chr + key)
                for k, v in d.items():
                    res[k] = v
            else:
                res[base_key + splt_chr + key] = val

        return res

    tmp = internal_join(input_dict, "")
    final = dict((name[1:], val) for name, val in tmp.items())

    return final


if __name__ == "__main__":
    load_config()
    print("Original:", cfg)

    res = __split(cfg)
    print("Splitted:", str(res))

    res2 = __join(res)
    print("Original:", str(res2))
