'''import time
from random import *
import midi

track = 2
channel = 2
rtime = 0
tempo = 120
randomnoteduration = 0
randomvolume = 0
pauseduration = 0

keys = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}

Gammas = {'Maj_seq':[0, 2, 4, 5, 7, 9, 11, 12],
          'Min_seq': [0, 2, 3, 5, 7, 8, 10, 12],
          'HarMin_seq': [0, 2, 3, 5, 7, 8, 11, 12],
          'MelMin_seq': [0, 2, 4, 5, 7, 9, 11, 12],
          }
#MAJOR_seq = [0, 2, 4, 5, 7, 9, 11, 12]
#MINOR_seq = [0, 2, 3, 5, 7, 8, 10, 12]
#HARMINOR_seq = [0, 2, 3, 5, 7, 8, 11, 12]
#MELMINOR_seq = [0, 2, 3, 5, 7, 9, 10, 12]
# midikey = keys["G"]
# midigamma = Gammas["Min_seq"]
RNotepitches = []
RNotedurations = []
RNotepauses = []
RNotevolumes = []

def note_randomizer():
    seed(time.time())
    global rtime
    while rtime<180:
        # randint(24,84)
        randompitch = choice([keys["C"],keys["C"]+2,keys["C"]+4]) + 12 * 7
        randomnoteduration = randint(2,2)/2
        randomvolume = randint(80, 120)
        for i in range(0,4):
            midi.addNote_rhytm(track, channel, randompitch, rtime, randomnoteduration, randomvolume)
            pauseduration = abs(0.5 - (randomnoteduration))
            rtime += randomnoteduration
            rtime += pauseduration



'''