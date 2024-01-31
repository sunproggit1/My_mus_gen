from midiutil.MidiFile import MIDIFile
from melody_randomizer import *


class MidiHandler:
    def __init__(self):
        self.MyMIDI = MIDIFile(1)  # Предполагаем одну дорожку для простоты
        self.track = 0
        self.time = 0
        self.tempo = 120

    def add_track_name(self, track_name):
        self.MyMIDI.addTrackName(self.track, self.time, track_name)

    def add_tempo(self, tempo):
        self.MyMIDI.addTempo(self.track, self.time, tempo)

    def add_note(self, channel, pitch, time, duration, volume):
        self.MyMIDI.addNote(self.track, channel, pitch, time, duration, volume)

    def save_midi(self, file_name):
        with open(file_name, "wb") as output_file:
            self.MyMIDI.writeFile(output_file)



