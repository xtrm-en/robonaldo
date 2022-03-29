import sys
try:
    import rsk2 as rsk
except Exception as e:
    print("Couldn't load rsk2:", e)
    sys.exit()

from mido import MidiFile
from robonaldo.music import MIDITranslator

mid = MidiFile('tests/MILF.mid')

with rsk.Client(host="172.19.39.223") as client:
    index = 0
    for msg in mid.play():
        robot = ['blue', 'green'][index % 2]
        number = [2, 2][index % 2]

        freq, duration, valid = MIDITranslator.translate(msg)
        if not valid:
            continue
        
        freq *= 1.5
        duration *= 1.0
        if duration == 0:
            continue

        print("f", freq, "d", duration)
        client.robots[robot][number].beep(int(freq), int(duration))
        
        index += 1
