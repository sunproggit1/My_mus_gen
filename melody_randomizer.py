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


### class Arpeggio
class Arpeggio():
    # seed(time.time())
    global key

    def __init__(self, octave=None):
        self.arpeggio_list = []
        self.arpeggio_notes = 0
        self.arpeggio_samples = {
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
            12: [0, 2, 4, 5, 7, 9, 11, 12],  # "maj_seq"
            13: [0, 2, 3, 5, 7, 8, 10, 12]  # "min_seq"

        }
        randnum = randint(0, len(self.arpeggio_samples) - 1)
        for i in range(0, len(self.arpeggio_samples[randnum])):
            self.arpeggio_list.append(key + self.arpeggio_samples[randnum][i] + 12 + 12 * octave)
            self.arpeggio_notes += 1
            if (i == len(self.arpeggio_samples[randnum]) - 1):
                for j in reversed(range(0, len(self.arpeggio_samples[randnum]) - 1)):
                    self.arpeggio_list.append(key + self.arpeggio_samples[randnum][j] + 12 + 12 * octave)
                    self.arpeggio_notes += 1

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
            midi.addNote_chords(ctrack, cchannel, key + self.arpeggio_list[iter], ctime, self.crandomnoteduration,
                                self.crandomvolume)
            CNotepitches.append(self.arpeggio_list[iter])

            ctime += self.crandomnoteduration
            ctime += self.cpauseduration
        ctime += ctime - math.floor(ctime)

### class Chords
class Chords_progr():
    # seed(time.time())
    global key
    global subdominant_parallel_tension
    global subdominant_tension

    def __init__(self, chord_long=0):
        if chord_long is not None:
            self.chord_long = chord_long
        self.note = 0
        self.chord_notes_list = [[], [], [], []]
        self.chords_samples = {
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
        }
        self.chord_progr = {
            1: [0, 9, 5, 7],  # "C","A","F","G"
            2: [0, 2, 5, 7],  # "C","D","F","G"
            3: [0, 7, 5, 4],  # "C","G","F","E"
            4: [0, 4, 11, 2, 2, 7],  # "C","E","B","Dm","D","G"
        }
        randnum = randint(1, len(self.chord_progr))
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
            self.chord_notes_list.append([[x + 2 for x in self.chords_samples[0]]])
            self.chord_notes_list.append([[x + 7 for x in self.chords_samples[0]]])

        ###########преоброзование двумерного списка в одномерный: исправление ошибок

        x = len(self.chord_notes_list[0])
        y = len(self.chord_notes_list)
        lst = []
        for i in range(y):
            for j in self.chord_notes_list[i]:
                lst.append(j)
        self.chord_notes_list = lst
        #####################

    def save(self):
        global ctime
        print(ctime)

        for i in range(0, len(self.chord_notes_list)):
            self.crandomnoteduration = randint(1, 2)
            self.cpauseduration = abs(1 - (self.crandomnoteduration))
            if (self.chord_long is not None):
                self.crandomnoteduration += self.chord_long
            self.crandomvolume = randint(80, 120)

            for j in range(0, len(self.chord_notes_list[i])):
                self.note = self.chord_notes_list[i][j]
                '''if self.one_octave_on == True:
                    if self.note > self.key + 12:
                        self.note -= 12
                if self.note == (self.key + 8):
                    subdominant_tension +=2
                    subdominant_parallel_tension+=1'''
                midi.addNote_chords(ctrack, cchannel, key + self.note + 24, ctime, self.crandomnoteduration,
                                    self.crandomvolume)
                ctime += 0.01
                CNotepitches.append(self.chord_notes_list[i][j])

            ctime += self.crandomnoteduration - 0.01 * len(self.chord_notes_list[i])
            ctime += self.cpauseduration

### class keychanger
class Keychanger():
    global subdominant_parallel_tension
    global subdominant_tension
    global key
    global gamma

    def __init__(self):
        global key
        global gamma
        self.note = 0
        self.chord_notes_list = [[], [], [], []]
        self.chords_samples = {
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
        }
        self.key_chg_progr = {
            1: [0, 0, 5, 5],  # "C","Caug","Fm","F"
            2: [0, 2, 2, 7],  # "C","Dm","D","G"
            3: [0, 4, 4, 11],  # "C","Em","Em14","Bm"
        }
        randnum = randint(1, len(self.key_chg_progr))
        print(self.key_chg_progr[randnum])
        print(randnum)
        if randnum == 1:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append(self.chords_samples[8])
            self.chord_notes_list[2].append([x + 5 for x in self.chords_samples[4]])
            self.chord_notes_list[3].append([x + 5 for x in self.chords_samples[0]])
            key += keys["F"]
            gamma = Gammas["Maj_seq"]
        elif randnum == 2:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append([x + 2 for x in self.chords_samples[4]])
            self.chord_notes_list[2].append([x + 2 for x in self.chords_samples[0]])
            self.chord_notes_list[3].append([x + 7 for x in self.chords_samples[0]])
            key += keys["G"]
            gamma = Gammas["Maj_seq"]

        elif randnum == 3:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append([x + 4 for x in self.chords_samples[4]])
            self.chord_notes_list[2].append([x + 4 for x in self.chords_samples[13]])
            self.chord_notes_list[3].append([x + 11 for x in self.chords_samples[4]])
            key += keys["B"]
            gamma = Gammas["Min_seq"]
        '''
        elif randnum == 4:
            self.chord_notes_list[0].append(self.chords_samples[0])
            self.chord_notes_list[1].append([x + 4 for x in self.chords_samples[4]])
            self.chord_notes_list[2].append([x + 11 for x in self.chords_samples[10]])
            self.chord_notes_list[3].append([x + 2 for x in self.chords_samples[4]])
            self.chord_notes_list.append([[x + 7 for x in self.chords_samples[0]]])'''

        ###########преоброзование двумерного списка в одномерный: исправление ошибок

        x = len(self.chord_notes_list[0])
        y = len(self.chord_notes_list)
        lst = []
        for i in range(y):
            for j in self.chord_notes_list[i]:
                lst.append(j)
        self.chord_notes_list = lst
        #####################

    def save(self):
        global ctime
        print(ctime)

        for i in range(0, len(self.chord_notes_list)):
            self.crandomnoteduration = randint(120, 240) / tempo
            self.crandomvolume = randint(80, 120)
            self.cpauseduration = abs(0.5 - (self.crandomnoteduration))

            for j in range(0, len(self.chord_notes_list[i])):
                self.note = self.chord_notes_list[i][j]
                '''if self.one_octave_on == True:
                    if self.note > self.key + 12:
                        self.note -= 12
                if self.note == (self.key + 8):
                    subdominant_tension +=2
                    subdominant_parallel_tension+=1'''
                midi.addNote_chords(ctrack, cchannel, key + self.note + 24, ctime, self.crandomnoteduration,
                                    self.crandomvolume)
                ctime += 0.01
                CNotepitches.append(self.chord_notes_list[i][j])

            ctime += self.crandomnoteduration - 0.01 * len(self.chord_notes_list[i])
            ctime += self.cpauseduration

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


###########randoming
def note_randomizer(current_seed=None):
    seed(current_seed)
    global key
    global gamma
    key = keys["D"]
    global rtime
    global mtime
    global ctime

    prologue = 20
    v1time = 60
    chorus = 80
    '''v2time = 60
    chorus2 = 80
    chorus3 = 80
    epilogue = 20'''


    while mtime <= prologue and ctime <= prologue and rtime <= prologue:
        random_sequence_identifier = randint(0, 100)

        if random_sequence_identifier % 10 == 0:
            print("arpeggio")
            arp = Arpeggio(2)
            arp.save()
            del arp

        elif random_sequence_identifier % 41 == 0:
            print("key change")
            keychg = Keychanger()
            if key >= 12:
                key -= 12

            print("key: ", key)
            keychg.save()
            del keychg

        elif mtime >= ctime:
            chrd = Chords_progr()
            crandomnoteduration = randint(1, 2)
            crandomvolume = randint(80, 120)
            cpauseduration = abs(math.ceil(crandomnoteduration) - (crandomnoteduration))

            chrd.save()
            del chrd
        if random_sequence_identifier % 7 == 0:
            mel = Melody_combs()
            mel.save()
            del mel

        '''mrandompitch = key + choice(gamma) + 12 * randint(3, 5)

        # randint(24,84)
        mrandomnoteduration = randint(60, 120) / tempo
        mpauseduration = abs(0.5 - (mrandomnoteduration))
        mrandomvolume = randint(80, 120)
        midi.addNote_mel(mtrack, mchannel, mrandompitch, mtime, mrandomnoteduration, mrandomvolume)

        mtime += mrandomnoteduration
        mtime += mpauseduration'''

        if rtime <= prologue:
            randompitch = choice([key, key + 2, key + 5, key + 7]) + 12 * 5
            rrandomnoteduration = randint(2, 2) / 2
            rrandomvolume = randint(80, 120)
            for i in range(0, 4):
                midi.addNote_rhytm(rtrack, rchannel, randompitch, rtime, rrandomnoteduration, rrandomvolume)
                # rpauseduration = abs(0.5 - (rrandomnoteduration))
                rtime += rrandomnoteduration
                # rtime += rpauseduration

        print("ctime: ", ctime)
        print("mtime: ", mtime)
        print("rtime: ", rtime)

    while prologue < mtime <= v1time or prologue < ctime <= v1time or prologue < rtime <= v1time:
        random_sequence_identifier = randint(0, 100)

        if random_sequence_identifier % 10 == 0:
            print("arpeggio")
            arp = Arpeggio(4)
            arp.save()
            del arp

        elif random_sequence_identifier % 41 == 0:
            print("key change")
            keychg = Keychanger()
            if key >= 12:
                key -= 12

            print("key: ", key)
            keychg.save()
            del keychg

        elif mtime > ctime:
            chrd = Chords_progr()
            crandomnoteduration = randint(1, 2)
            crandomvolume = randint(80, 120)
            cpauseduration = abs(math.ceil(crandomnoteduration) - (crandomnoteduration))

            chrd.save()
            del chrd
        if random_sequence_identifier % 7 == 0:
            mel = Melody_combs()
            mel.save()
            del mel
        '''mrandompitch = key + choice(gamma) + 12 * randint(4, 6)

        # randint(24,84)
        mrandomnoteduration = randint(60, 120) / tempo
        mpauseduration = abs(0.5 - (mrandomnoteduration))
        mrandomvolume = randint(80, 120)
        midi.addNote_mel(mtrack, mchannel, mrandompitch, mtime, mrandomnoteduration, mrandomvolume)

        mtime += mrandomnoteduration
        mtime += mpauseduration'''

        if prologue < rtime <= v1time:
            randompitch = choice([key, key + 2, key + 5, key + 7]) + 12 * 5
            rrandomnoteduration = randint(2, 2) / 2
            rrandomvolume = randint(80, 120)
            for i in range(0, 4):
                midi.addNote_rhytm(rtrack, rchannel, randompitch, rtime, rrandomnoteduration, rrandomvolume)
                rtime += rrandomnoteduration

        print("ctime: ", ctime)
        print("mtime: ", mtime)
        print("rtime: ", rtime)

    while v1time < mtime <= chorus or v1time < ctime <= chorus or v1time < rtime <= chorus:
        random_sequence_identifier = randint(0, 100)

        if random_sequence_identifier % 10 == 0:
            print("arpeggio")
            arp = Arpeggio(3)
            arp.save()
            del arp

        elif random_sequence_identifier % 41 == 0:
            print("key change")
            keychg = Keychanger()
            if key >= 12:
                key -= 12

            print("key: ", key)
            keychg.save()
            del keychg

        elif mtime > ctime:
            chrd = Chords_progr()
            crandomnoteduration = randint(1, 2)
            crandomvolume = randint(80, 120)
            cpauseduration = abs(math.ceil(crandomnoteduration) - (crandomnoteduration))

            chrd.save()
            del chrd
        if random_sequence_identifier % 7 == 0:
            mel = Melody_combs()
            mel.save()
            del mel
        '''mrandompitch = key + choice(gamma) + 12 * randint(4, 6)

        # randint(24,84)
        mrandomnoteduration = randint(60, 120) / tempo
        mpauseduration = abs(0.5 - (mrandomnoteduration))
        mrandomvolume = randint(80, 120)
        midi.addNote_mel(mtrack, mchannel, mrandompitch, mtime, mrandomnoteduration, mrandomvolume)

        mtime += mrandomnoteduration
        mtime += mpauseduration'''

        if rtime < chorus:
            randompitch = choice([key, key + 2, key + 5, key + 7]) + 12 * 5
            rrandomnoteduration = randint(2, 2) / 2
            rrandomvolume = randint(80, 120)
            for i in range(0, 4):
                midi.addNote_rhytm(rtrack, rchannel, randompitch, rtime, rrandomnoteduration, rrandomvolume)
                rtime += rrandomnoteduration

        print("ctime: ", ctime)
        print("mtime: ", mtime)
        print("rtime: ", rtime)
    random_sequence_identifier = randint(0, 10)
    if random_sequence_identifier == 0:
        arp = Arpeggio(4)
        arp.save()
    elif random_sequence_identifier == 1:
        chrd = Chords_progr(4)
        chrd.save()

    midi.save_in_main()

    # randint(24,84)
    print(CNotepitches)
    print(MNotepitches)
