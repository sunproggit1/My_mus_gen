import os
from contextlib import ExitStack
from os import error
from os.path import exists
from random import randint
import threading
import logging

import mysql.connector
from midiutil.MidiFile import *
import datetime
import pygame
import base64

MyMIDI1 = MIDIFile(1)
MyMIDI2 = MIDIFile(2)
MyMIDI3 = MIDIFile(3)
MyMIDI4 = MIDIFile(4)
track1 = 0
track2 = 1
track3 = 2
track4 = 3
time = 0
tempo = 120

MyMIDI1.addTrackName(track1, time, "Sample melody Track")
MyMIDI1.addTempo(track1, time, tempo)
MyMIDI2.addTrackName(track2, time, "Sample chords Track")
MyMIDI2.addTempo(track2, time, tempo)
MyMIDI3.addTrackName(track3, time, "Sample rhytm Track")
MyMIDI3.addTempo(track3, time, tempo)
MyMIDI4.addTrackName(track4, time, "Sample Track")
MyMIDI4.addTempo(track4, time, tempo)

def file_name_rand():
    return str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(".","_").replace(":","_")

def addNote_mel(track1, channel, pitch, time, duration, volume):
    MyMIDI1.addNote(track1, channel, pitch, time, duration, volume)
    MyMIDI4.addNote(track4, channel, pitch, time, duration, volume)

def addNote_chords(track2, channel, pitch, time, duration, volume):
    MyMIDI2.addNote(track2, channel, pitch, time, duration, volume)
    MyMIDI4.addNote(track4, channel, pitch, time, duration, volume)

def addNote_rhytm(track3, channel, pitch, time, duration, volume):
    MyMIDI3.addNote(track3, channel, pitch, time, duration, volume)
    MyMIDI4.addNote(track4, channel, pitch, time, duration, volume)

def save_all(data_userid,seed):

    newfolder = "Output"+file_name_rand()
    if not exists("Outputs/"+newfolder):
        os.mkdir("Outputs/"+newfolder)
    binfilemain = open("Outputs/"+newfolder+"/output"+file_name_rand()+".mid", 'wb')
    MyMIDI4.writeFile(binfilemain)
    binfilemain.close()

    binfile1 = open("Outputs/"+newfolder+"/output_melody"+file_name_rand()+".mid", 'wb')
    MyMIDI1.writeFile(binfile1)
    binfile1.close()

    binfile2 = open("Outputs/" + newfolder + "/output_chords" + file_name_rand() + ".mid", 'wb')
    MyMIDI2.writeFile(binfile2)
    binfile2.close()

    binfile3 = open("Outputs/" + newfolder + "/output_rhytm" + file_name_rand() + ".mid", 'wb')
    MyMIDI3.writeFile(binfile3)
    binfile3.close()

    print("DB data:",data_userid, newfolder, file_name_rand(), seed)
    #data_userid, newfolder, file_name_rand(), seed
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="midi_user_db"
        )
        print(mydb)
        query = "insert into midi_files values(Null,%s,%s,%s,%s)"
        mycursor = mydb.cursor()
        mycursor.execute(query, (data_userid, newfolder, file_name_rand(), seed,))
        mydb.commit()
        print("Success in db")
        mycursor.close()
        mydb.close()
    except error:
        print(error,"Not connected")

def save_in_main():

    binfilemain = open("output.mid", 'wb')
    MyMIDI4.writeFile(binfilemain)
    binfilemain.close()

    binfile1 = open("output_melody.mid", 'wb')
    MyMIDI1.writeFile(binfile1)
    binfile1.close()

    binfile2 = open("output_chords.mid", 'wb')
    MyMIDI2.writeFile(binfile2)
    binfile2.close()

    binfile3 = open("output_rhytm.mid", 'wb')
    MyMIDI3.writeFile(binfile3)
    binfile3.close()
