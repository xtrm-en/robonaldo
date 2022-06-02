from enum import Enum
from toml import TomlEncoder
from ...context.entities.robot import TeamColor


class TomlEnumEncoder(TomlEncoder):
    def __init__(self, _dict=dict, preserve=False):
        super(TomlEnumEncoder, self).__init__(_dict, preserve)
        self.dump_funcs[Enum] = self._dump_enum
        self.dump_funcs[TeamColor] = self._dump_enum

    def _dump_enum(self, v: Enum) -> str:
        return '"%s"' % v.name
