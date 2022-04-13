import mido
import sys
from robonaldo.music import MIDITranslator
from mido.midifiles.units import tick2second

mid = mido.MidiFile("tests/midi/bad2.mid")
print("MIDI Type:", mid.type)


tempo: int = -1
ticks_per_beat: int = mid.ticks_per_beat


def is_valid() -> bool:
    return tempo != -1 and ticks_per_beat != -1


tracks = []

for track in mid.tracks:
    track_len = len(track)
    print("Track:", track_len)

    waiting_for_note = False
    for i in range(track_len - 1, -1, -1):
        msg = track[i]
        if msg.is_meta: continue

        if i != 0:
            for i in range(i + 1, track_len):
                track[i].time += msg.time
    
    track_data = []
    to_be_registered = []
    for msg in track[0:200]:
        print(msg)

# U:\devoirs\NSI\Terminale\Python\robonaldo-main>"C:\\WPy-3670\\python-3.6.7.amd64\\python.exe" -m tests.beep
# MIDI Type: 1
# Track: 3
# MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)
# MetaMessage('set_tempo', tempo=408163, time=0)
# MetaMessage('end_of_track', time=0)
# Track: 5525
# MetaMessage('track_name', name='Elec. Piano (Classic)', time=0)
# program_change channel=0 program=0 time=0
# note_on channel=0 note=63 velocity=50 time=0
# note_on channel=0 note=51 velocity=50 time=0
# note_off channel=0 note=51 velocity=0 time=96
# note_off channel=0 note=63 velocity=0 time=96
# note_on channel=0 note=63 velocity=50 time=96
# note_on channel=0 note=51 velocity=50 time=96
# note_off channel=0 note=51 velocity=0 time=192
# note_off channel=0 note=63 velocity=0 time=192
# note_on channel=0 note=65 velocity=50 time=192

