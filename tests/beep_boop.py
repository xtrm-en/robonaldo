try:
    import rsk2 as rsk
except Exception as e:
    print("Couldn't load rsk2:", e)

    import sys
    sys.exit()

import mido
import robonaldo.music.MIDITranslator

mid = mido.MidiFile('tests/yes.mid')


with rsk.Client(host="172.19.39.223") as client:
    index = 0
    for msg in mid.play():
        robot = ['blue', 'blue', 'green', 'green'][index % 4]
        number = [1, 2, 1, 2][index % 4]

        freq, duration, valid = MIDITranslator.translate(msg)
        if not valid:
            continue

        client.robots[robot][number].beep(frequency, duration)
        index += 1
