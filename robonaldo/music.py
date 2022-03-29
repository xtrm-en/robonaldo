"""
Robonaldo Musicinator(tm)(copyrighted) UwU
"""

import mido
# import robonaldo.context.robot.Robot
# import robonaldo.controller.GameController

midiMap = {
    0: 8.176,
    1: 8.662,
    2: 9.177,
    3: 9.723,
    4: 10.301,
    5: 10.913,
    6: 11.562,
    7: 12.250,
    8: 12.978,
    20: 25.957,
    21: 27.500,
    22: 29.135,
    23: 30.868,
    24: 32.703,
    25: 34.648,
    26: 36.708,
    27: 38.891,
    28: 41.203,
    29: 43.654,
    30: 46.249,
    31: 48.999,
    32: 51.913,
    33: 55.000,
    34: 58.270,
    35: 61.735,
    36: 65.406,
    37: 69.296,
    38: 73.416,
    39: 77.782,
    40: 82.407,
    41: 87.307,
    42: 92.499,
    43: 97.999,
    44: 103.826,
    45: 110.000,
    46: 116.541,
    47: 123.471,
    48: 130.813,
    49: 138.591,
    50: 146.832,
    51: 155.563,
    52: 164.814,
    53: 174.614,
    54: 184.997,
    55: 195.998,
    56: 207.652,
    57: 220.000,
    58: 233.082,
    59: 246.942,
    60: 261.626,
    61: 277.183,
    62: 293.665,
    63: 311.127,
    64: 329.628,
    65: 349.228,
    66: 369.994,
    67: 391.995,
    68: 415.305,
    69: 440.000,
    70: 466.164,
    71: 493.883,
    72: 523.251,
    73: 554.365,
    74: 587.330,
    75: 622.254,
    76: 659.255,
    77: 698.456,
    78: 739.989,
    79: 783.991,
    80: 830.609,
    81: 880.000,
    82: 932.328,
    83: 987.767,
    84: 1046.502,
    85: 1108.731,
    86: 1174.659,
    87: 1244.508,
    88: 1318.510,
    89: 1396.913,
    90: 1479.978,
    91: 1567.982,
    92: 1661.219,
    93: 1760.000,
    94: 1864.655,
    95: 1975.533,
    96: 2093.005,
    97: 2217.461,
    98: 2349.318,
    99: 2489.016,
    100: 2637.020,
    101: 2793.826,
    102: 2959.955,
    103: 3135.963,
    104: 3322.438,
    105: 3520.000,
    106: 3729.310,
    107: 3951.066,
    108: 4186.009,
    109: 4434.922,
    110: 4698.636,
    111: 4978.032,
    112: 5274.041,
    113: 5587.652,
    114: 5919.911,
    115: 6271.927,
    116: 6644.875,
    117: 7040.000,
    118: 7458.620,
    119: 7902.133,
    120: 8372.018,
    121: 8869.844,
    122: 9397.273,
    123: 9956.063,
    124: 10548.080,
    125: 11175.300,
    126: 11839.820,
    127: 12543.850
}


class MIDITranslator:
    @staticmethod
    def translate(message: mido.messages.Message) -> (float, float, bool):
        internal_vars = vars(message)
        if 'note_on' not in internal_vars['type']:
            return (-1, -1, False)

        note = internal_vars['note']
        freq = midiMap[note]
        duration = internal_vars['time'] * 1000  # its in seconds
        return (freq, duration, True)


# class WavelengthPlayer:
#     @staticmethod
#     def play(midi: mido.MidiFile):
#         for message in midi.play():
#             target = GameController.random_robot()
#             freq, duration, valid = MIDITranslator.translate(message)
#             if valid:
#                 playNote(freq, duration, target)

#     @staticmethod
#     def play(midi: mido.MidiFile, target: Robot):
#         for message in midi.play():
#             freq, duration, valid = MIDITranslator.translate(message)
#             if valid:
#                 playNote(freq, duration, target)

#     @staticmethod
#     def playNote(frequency: float, duration: float):
#         target = GameController.random_robot()
#         playNote(frequency, duration, target)

#     @staticmethod
#     def playNote(frequency: float, duration: float, target: Robot):
#         pass
