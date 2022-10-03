'''
import logging
import time
from random import *
import midi

tempo = 120

ctrack = 1
cchannel = 1
ctime = 0
crandomnoteduration = 0
crandomvolume = 0
cpauseduration = 0
global no_tension
global dominant_tension
global subdominant_tension
global dominant_parallel_tension
global subdominant_parallel_tension

random_sequence_identifier = 0

keys = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}

Gammas = {'Maj_seq': [0, 2, 4, 5, 7, 9, 11, 12],
          'Min_seq': [0, 2, 3, 5, 7, 8, 10, 12],
          'HarMin_seq': [0, 2, 3, 5, 7, 8, 11, 12],
          'MelMin_seq': [0, 2, 4, 5, 7, 9, 11, 12],
          }
# MAJOR_seq = [0, 2, 4, 5, 7, 9, 11, 12]
# MINOR_seq = [0, 2, 3, 5, 7, 8, 10, 12]
# HARMINOR_seq = [0, 2, 3, 5, 7, 8, 11, 12]
# MELMINOR_seq = [0, 2, 3, 5, 7, 9, 10, 12]
# midikey = keys["G"]
# midigamma = Gammas["Min_seq"]
CNotepitches = []
CNotedurations = []
CNotepauses = []
CNotevolumes = []

### class Arpeggio
class Arpeggio():
    key = keys['C']
    def __init__(self, arpeggio_steps=None, key=None, octave=None, randseed=None):
        self.key = key
        self.arpeggio_list = []
        self.arpeggio_notes = 0
        self.arpeggio_samples = {
            0: [0, 4, 7],  # "maj"
            1: [7, 4, 0],  # "maj_reverse"
            2: [0, 3, 7],  # "min"
            3: [7, 3, 0],  # "min_reverse"
            4: [0, 4, 7, 12],  # "maj8"
            5: [12, 7, 4, 0],  # "maj8_reverse"
            6: [0, 3, 7, 12],  # "min8"
            7: [12, 7, 3, 0],  # "min8_reverse"
            8: [0, 2, 4, 5, 7, 9, 11, 12],  # "maj_seq"
            9: [0, 2, 3, 5, 7, 8, 10, 12]  # "min_seq"
        }
        randnum = randint(0, len(self.arpeggio_samples))
        print(self.arpeggio_samples[randnum])
        print(randnum)
        for i in range(0, len(self.arpeggio_samples[randnum])-1):
            self.arpeggio_list.append(self.key + self.arpeggio_samples[randnum][i] + 24 + 12 * octave)
            self.arpeggio_notes += 1
            if (i == len(self.arpeggio_samples[randnum]) - 1):
                for j in reversed(range(0, len(self.arpeggio_samples[randnum]) - 1)):
                    self.arpeggio_list.append(self.key + self.arpeggio_samples[randnum][j] + 24 + 12 * octave)
                    self.arpeggio_notes += 1

        print(self.arpeggio_list)
        print(self.arpeggio_notes)
        self.crandomnoteduration = randint(12, 30) / tempo
        self.crandomvolume = randint(80, 120)
        self.cpauseduration = abs(0.25 - (self.crandomnoteduration))

        print("rnotedur: ", crandomnoteduration)
        print("rpausedur: ", cpauseduration)
        print("notedur: ", self.crandomnoteduration)
        print("pausedur: ", self.cpauseduration)

    def save(self):
        global ctime
        print(ctime)
        for iter in range(0, self.arpeggio_notes):
            midi.addNote_chords(ctrack, cchannel, self.arpeggio_list[iter], ctime, self.crandomnoteduration,
                                self.crandomvolume)
            CNotepitches.append(self.arpeggio_list[iter])

            ctime += self.crandomnoteduration
            ctime += self.cpauseduration

### class Chords
class Chords_progr():
    global subdominant_parallel_tension
    global subdominant_tension
    def __init__(self, key=None, randseed=None, one_octave_on = None):
        self.one_octave_on = one_octave_on
        self.key = key
        self.note = 0
        self.chord_notes_list = [[],[],[],[]]
        self.chords_samples = {
            0: [0, 4, 7],  # "maj"
            1: [0, 4, 7, 9],  # maj6
            2: [0, 4, 7, 11], # maj7
            3: [0, 4, 7, 12],  # "maj8"
            4: [0, 3, 7],  # "min"
            5: [0, 3, 7, 9],  # min6
            6: [0, 3, 7, 10],  # "min7"
            7: [0, 3, 7, 12], # min8
            8: [0, 4, 8], # aug
            9: [0, 4, 8, 11], #aug7
            10: [0, 3, 6], # dim
            11: [0, 3, 6, 10]  # dim7
        }
        self.chord_progr = {
            1: [0, 9, 5, 7], #"C","A","F","G"
            2: [0, 2, 5, 7], #"C","D","F","G"
            3: [0, 7, 5, 4], #"C","G","F","E"
            4: [0, 4, 11 ,2 ,7], #"C","E","B","D","G"
        }
        randnum = randint(1, len(self.chord_progr))
        print(self.chord_progr[randnum])
        print(randnum)
        if randnum == 1:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append([x + 9 for x in self.chords_samples[4]])
            self.chord_notes_list[2].append([x + 5 for x in self.chords_samples[0]])
            self.chord_notes_list[3].append([x + 7 for x in self.chords_samples[0]])
        elif randnum == 2:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append([x + 2 for x in self.chords_samples[4]])
            self.chord_notes_list[2].append([x + 5 for x in self.chords_samples[0]])
            self.chord_notes_list[3].append([x + 7 for x in self.chords_samples[0]])

        elif randnum == 3:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append([x + 7 for x in self.chords_samples[0]])
            self.chord_notes_list[2].append([x + 5 for x in self.chords_samples[0]])
            self.chord_notes_list[3].append([x + 4 for x in self.chords_samples[4]])

        elif randnum == 4:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append([x + 4 for x in self.chords_samples[4]])
            self.chord_notes_list[2].append([x + 11 for x in self.chords_samples[10]])
            self.chord_notes_list[3].append([x + 2 for x in self.chords_samples[4]])
            self.chord_notes_list.append([[x + 7 for x in self.chords_samples[0]]])

        ###########преоброзование двумерного списка в одномерный: исправление ошибок
        print(self.chord_notes_list)
        x = len(self.chord_notes_list[0])
        y = len(self.chord_notes_list)
        lst = []
        for i in range(y):
            for j in self.chord_notes_list[i]:
                lst.append(j)
        self.chord_notes_list = lst
        print(self.chord_notes_list)
        print(len(self.chord_notes_list))
        #####################

    def save(self):
        global ctime
        print(ctime)

        for i in range(0, len(self.chord_notes_list)):
            self.crandomnoteduration = randint(120, 240) / tempo
            self.crandomvolume = randint(80, 120)
            self.cpauseduration = abs(0.5 - (self.crandomnoteduration))

            for j in range(0, len(self.chord_notes_list[i])):
                print(i,j)
                self.note = self.chord_notes_list[i][j]
                if self.one_octave_on == True:
                    if self.note > self.key + 12:
                        self.note -= 12
                if self.note == (self.key + 8):
                    subdominant_tension +=2
                    subdominant_parallel_tension+=1
                midi.addNote_chords(ctrack, cchannel, self.note+24, ctime, self.crandomnoteduration,
                                    self.crandomvolume)
                ctime+=0.01
                CNotepitches.append(self.chord_notes_list[i][j])

            ctime += self.crandomnoteduration - 0.01*len(self.chord_notes_list[i])
            ctime += self.cpauseduration

###########randoming
def note_randomizer():
    key = keys["C"]
    global ctime
    seed(time.time())
    while ctime < 180:
        random_sequence_identifier = randint(0, 100)
        if random_sequence_identifier % 50 == 0:
            print("arpeggio")
            arp = Arpeggio(5, keys['C'], 2, random_sequence_identifier)
            arp.save()
            del arp
        else:
            chrd = Chords_progr("C",random_sequence_identifier,False)
            randomnoteduration = randint(1, 2)
            randomvolume = randint(80, 120)
            pauseduration = abs(0.5 - (randomnoteduration))
            print(ctime)
            chrd.save()
            del chrd
    midi.save_chords()
        # randint(24,84)
    print(CNotepitches)
'''