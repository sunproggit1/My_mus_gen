import math
from random import *
import midi
import time

tempo = 120

mtrack = 0
mchannel = 0
mtime = 0
mrandomnoteduration = 0
mrandomvolume = 0
mpauseduration = 0

ctrack = 0
cchannel = 0
ctime = 0
crandomnoteduration = 0
crandomvolume = 0
cpauseduration = 0

rtrack = 0
rchannel = 0
rtime = 0
rrandomnoteduration = 0
rrandomvolume = 0
rpauseduration = 0

'''global no_tension
global dominant_tension
global subdominant_tension
global dominant_parallel_tension
global subdominant_parallel_tension'''

prologue = 20
v1time = 60
chorus = 80
v2time = 120
chorus2 = 140
chorus3 = 160
epilogue = 180

keys = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
key = keys["C"]
seed(time.time())
Gammas = {'Maj_seq': [0, 2, 4, 5, 7, 9, 11, 12],
          'Min_seq': [0, 2, 3, 5, 7, 8, 10, 12],
          'HarMin_seq': [0, 2, 3, 5, 7, 8, 11, 12],
          'MelMin_seq': [0, 2, 4, 5, 7, 9, 11, 12],
          }
gamma = Gammas["Maj_seq"]

# MAJOR_seq = [0, 2, 4, 5, 7, 9, 11, 12]
# MINOR_seq = [0, 2, 3, 5, 7, 8, 10, 12]
# HARMINOR_seq = [0, 2, 3, 5, 7, 8, 11, 12]
# MELMINOR_seq = [0, 2, 3, 5, 7, 9, 10, 12]
# midikey = keys["G"]
# midigamma = Gammas["Min_seq"]

MNotepitches = []
MNotedurations = []
MNotepauses = []
MNotevolumes = []
CNotepitches = []
CNotedurations = []
CNotepauses = []
CNotevolumes = []
RNotepitches = []
RNotedurations = []
RNotepauses = []
RNotevolumes = []

class Arpeggio:
    def __init__(self, key, octave=None):
        self.key = key
        self.octave = octave if octave is not None else 0
        self.arpeggio_list = self.generate_arpeggio()

    def generate_arpeggio(self):
        arpeggio_samples = [
            [0, 4, 7],  # "maj"
            [0, 4, 7, 9],  # maj6
            [0, 4, 7, 11],  # maj7
            [0, 4, 7, 12],  # "maj8"
            [0, 3, 7],  # "min"
            [0, 3, 7, 9],  # min6
            [0, 3, 7, 10],  # "min7"
            [0, 3, 7, 12],  # min8
            [0, 4, 8],  # aug
            [0, 4, 8, 11],  # aug7
            [0, 3, 6],  # dim
            [0, 3, 6, 10],  # dim7
            [0, 2, 4, 5, 7, 9, 11, 12],  # "maj_seq"
            [0, 2, 3, 5, 7, 8, 10, 12]  # "min_seq"
            # Добавьте остальные образцы аккордов здесь
        ]
        sample = random.choice(arpeggio_samples)
        return [self.key + note + 12 * self.octave for note in sample]

    def save(self, midi, track, channel, start_time, tempo):
        duration = random.randint(12, 30) / tempo
        volume = random.randint(80, 120)
        for note in self.arpeggio_list:
            midi.addNote(track, channel, note, start_time, duration, volume)
            start_time += duration

# arp = Arpeggio(key=60, octave=2)
# arp.save(midi_object, track=0, channel=0, start_time=0, tempo=120)



### class Chords
class ChordsProgression:
    def __init__(self, key, chord_length=0):
        self.key = key
        self.chord_length = chord_length
        self.chords_samples = self._init_chords_samples()
        self.chord_progression = self._generate_chord_progression()

    def _init_chords_samples(self):
        # Ваши образцы аккордов
        return {
            0: [0, 4, 7],  # "maj"
            1: [0, 4, 7, 9],  # maj6
            2: [0, 4, 7, 11],  # maj7
            3: [0, 4, 7, 12],  # "maj8"
            4: [0, 3, 7],  # "min"
            5: [0, 3, 7, 9],  # min6
            6: [0, 3, 7, 10],  # "min7"
            7: [0, 3, 7, 12],  # min8
            8: [0, 4, 8],  # aug
            9: [0, 4, 8, 11],  # aug7
            10: [0, 3, 6],  # dim
            11: [0, 3, 6, 10]  # dim7
            # Добавьте остальные образцы здесь
        }

    def _generate_chord_progression(self):
        # Генерация последовательности аккордов
        chord_prog_samples = {
            1: [0, 9, 5, 7],  # "C","A","F","G"
            2: [0, 2, 5, 7],  # "C","D","F","G"
            3: [0, 7, 5, 4],  # "C","G","F","E"
            4: [0, 4, 11, 2, 2, 7],  # "C","E","B","Dm","D","G"
            # Добавьте другие последовательности здесь
        }
        chosen_prog = random.choice(list(chord_prog_samples.values()))
        return [self.chords_samples[chord] for chord in chosen_prog]

    def save(self, midi, track, channel, start_time, tempo):
        for chord in self.chord_progression:
            duration = random.randint(1, 2)
            if self.chord_length:
                duration += self.chord_length
            volume = random.randint(80, 120)
            for note in chord:
                midi.addNote(track, channel, self.key + note, start_time, duration, volume)
                start_time += duration

# chords_prog = ChordsProgression(key=60)
# chords_prog.save(midi_object, track=1, channel=0, start_time=0, tempo=120)

### class keychanger
class KeyChanger:
    def __init__(self, base_key):
        self.base_key = base_key
        self.new_key = None
        self.new_scale = None
        self.chords_samples = self._init_chords_samples()
        self.key_change_progression = self._generate_key_change_progression()

    def _init_chords_samples(self):
        # Определение образцов аккордов
        return {
            # Ваши образцы аккордов здесь
            0: [0, 4, 7],  # "maj"
            1: [0, 4, 7, 9],  # maj6
            2: [0, 4, 7, 11],  # maj7
            3: [0, 4, 7, 12],  # "maj8"
            4: [0, 3, 7],  # "min"
            5: [0, 3, 7, 9],  # min6
            6: [0, 3, 7, 10],  # "min7"
            7: [0, 3, 7, 12],  # min8
            8: [0, 4, 8],  # aug
            9: [0, 4, 8, 11],  # aug7
            10: [0, 3, 6],  # dim
            11: [0, 3, 6, 10],  # dim7
            12: [0, 4, 7, 12, 14],  # maj14
            13: [0, 3, 7, 12, 14]  # min14
            # Добавьте другие образцы здесь
        }

    def _generate_key_change_progression(self):
        # Примеры последовательностей смены ключа
        key_change_samples = {
            1: [0, 0, 5, 5],  # "C","Caug","Fm","F"
            2: [0, 2, 2, 7],  # "C","Dm","D","G"
            3: [0, 4, 4, 11],  # "C","Em","Em14","Bm"
            # Добавьте другие последовательности здесь
        }
        chosen_progression = random.choice(list(key_change_samples.values()))
        return [self.chords_samples[chord] for chord in chosen_progression]

    def apply_key_change(self, midi, track, channel, start_time, tempo):
        for chord in self.key_change_progression:
            duration = random.randint(120, 240) / tempo
            volume = random.randint(80, 120)
            for note in chord:
                midi.addNote(track, channel, self.base_key + note, start_time, duration, volume)
                start_time += duration


### class melody_combinations
class Melody_combs():
    global key
    global gamma

    def __init__(self, octave=None):
        print("melody comb")
        self.majors = 8
        self.minors = 14
        self.combo_notes_list = []
        self.combo_notes_dur_list = []
        self.combo_samples = {
            ##for major scale
            0: [12, 12, 12, 17, 16, 19, 16, 11, 11, 12, 16],  # combo1
            1: [16, 16, 16, 14, 17, 19, 17, 16],  # combo2 advancement of combo1
            2: [12, 7, 11, 12, 16, 14, 10, 7, 11, 14, 9],  # combo3
            3: [9, 9, 12, 16, 12, 9, 9, 9, 9, 12, 14],  # "combo4 advancement of combo3
            4: [0, 4, 8],  # aug
            5: [0, 4, 8, 11],  # aug7
            6: [0, 3, 6],  # dim
            7: [0, 3, 6, 10],  # dim7
            # for minor scale
            8: [12, 12, 12, 17, 15, 19, 15, 11, 11, 12, 15],  # combo1
            9: [15, 15, 15, 14, 17, 19, 17, 15],  # combo2 advancement of combo1
            10: [12, 7, 10, 12, 15, 14, 11, 7, 12, 14, 9],  # combo3
            11: [9, 9, 12, 16, 12, 9, 9, 9, 11, 12, 14],  # "combo4 advancement of combo3
            12: [0, 2, 4, 5, 7, 9, 11, 12],  # "maj_seq"
            13: [0, 2, 3, 5, 7, 8, 10, 12]  # "min_seq"
        }
        self.combo_sample_duration = {

            ##for major scale
            0: [0.25, 0.25, 0.5, 0.25, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.5],  # combo1
            1: [0.25, 0.25, 0.5, 0.25, 0.5, 1, 0.25, 1],  # combo2 advancement of combo1
            2: [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5],  # combo3
            3: [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5],  # "combo4 advancement of combo3
            4: [0, 4, 8],  # aug
            5: [0, 4, 8, 11],  # aug7
            6: [0, 3, 6],  # dim
            7: [0, 3, 6, 10],  # dim7
            # for minor scale
            8: [0.25, 0.25, 0.5, 0.25, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.5],  # combo1
            9: [0.25, 0.25, 0.5, 0.25, 0.5, 1, 0.25, 1],  # combo2 advancement of combo1
            10: [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5],  # combo3
            11: [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5],  # "combo4 advancement of combo3
            12: [0, 2, 4, 5, 7, 9, 11, 12],  # "maj_seq"
            13: [0, 2, 3, 5, 7, 8, 10, 12]  # "min_seq"
        }

        randcycle = choice([1, 2, 4])
        if gamma == Gammas["Maj_seq"]:
            randnum = randint(0, self.majors - 1)
        else:
            randnum = randint(self.majors, self.minors - 1)

        for i in range(0, randcycle):
            for x in range(0, len(self.combo_samples[randnum])):
                self.combo_notes_list.append(self.combo_samples[randnum][x])
                self.combo_notes_dur_list.append(self.combo_sample_duration[randnum][x])
            if i % 2 == 0 and randnum % 2 == 0:
                for x in range(0, len(self.combo_samples[randnum + 1])):
                    self.combo_notes_list.append(self.combo_samples[randnum + 1][x])
                    self.combo_notes_dur_list.append(self.combo_sample_duration[randnum + 1][x])
            elif i % 2 == 0 and randnum % 2 == 1:
                for x in range(0, len(self.combo_samples[randnum - 1])):
                    self.combo_notes_list.append(self.combo_samples[randnum - 1][x])
                    self.combo_notes_dur_list.append(self.combo_sample_duration[randnum - 1][x])

    def save(self):
        global mtime
        print(mtime)
        for i in range(0, len(self.combo_notes_list)):
            self.mrandomvolume = randint(80, 120)
            self.note = self.combo_notes_list[i]
            self.durat = self.combo_notes_dur_list[i]

            midi.addNote_mel(mtrack, mchannel, key + self.note + 36, mtime, self.durat,
                             self.mrandomvolume)
            mtime += self.durat
            MNotepitches.append(self.combo_notes_list[i])

# key_changer = KeyChanger(base_key=60)
# key_changer.apply_key_change(midi_object, track=1, channel=0, start_time=0, tempo=120)


###########randoming
def note_randomizer(midi, tempo, start_time=0, end_time=180):
    current_time = start_time
    key = 60  # Пример начального ключа

    while current_time <= end_time:
        random_sequence_identifier = random.randint(0, 100)

        if random_sequence_identifier % 10 == 0:
            arp = Arpeggio(key=key, octave=2)
            arp.save(midi, track=1, channel=0, start_time=current_time, tempo=tempo)
            current_time += arp.get_total_duration()  # Обновляем текущее время

        elif random_sequence_identifier % 41 == 0:
            key_changer = KeyChanger(base_key=key)
            key_changer.apply_key_change(midi, track=1, channel=0, start_time=current_time, tempo=tempo)
            key = key_changer.new_key  # Обновляем ключ
            current_time += key_changer.get_total_duration()

        elif random_sequence_identifier % 7 == 0:
            mel = Melody_combs(key=key)
            mel.save(midi, track=0, channel=0, start_time=current_time, tempo=tempo)
            current_time += mel.get_total_duration()

        else:
            chords_prog = ChordsProgression(key=key)
            chords_prog.save(midi, track=2, channel=0, start_time=current_time, tempo=tempo)
            current_time += chords_prog.get_total_duration()

    return midi  # Возвращаем объект MIDI с добавленными нотами


# # Создание MIDI объекта
# midi_object = MidiFile()

# # Вызов функции note_randomizer
# midi_object = note_randomizer(midi_object, tempo=120, start_time=0, end_time=180)

# # Сохранение MIDI файла
# with open("output.mid", "wb") as output_file:
#     midi_object.writeFile(output_file)
