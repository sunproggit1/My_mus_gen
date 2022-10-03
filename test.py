from random import *
import datetime
import time
from tkinter import *
import tkinter.messagebox as mb
import logging
from random import *
import pygame
import midi
import melody_randomizer
import mysql.connector
import math
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.messagebox as mb
from socket import *
from time import sleep


###client-server
client_data = False


###
no_tension = 0
dominant_tension = 0
subdominant_tension = 0
dominant_parallel_tension = 0
subdominant_parallel_tension = 0

###tkinter window
form1 = Tk()
form1.title("Midi generator")
form1['bg']='#64c832'
form1.wm_geometry('1000x600')

frame = Frame(form1)
frame.pack()

###play music
pygame.init()
pygame.mixer.init()
def play_music():
    global midi_file
    try:
        pygame.mixer.music.load(midi_file)
        pygame.mixer.music.play()
        print("Done!")

    except FileNotFoundError:
        print("File not found!")

def stop_music():
    global midi_file
    try:
        pygame.mixer.music.unload()

    except FileNotFoundError:
        print("File not found!")


midi_file = ''
def open_f():
    global midi_file
    midi_file = filedialog.askopenfilename()

wrapper1 = LabelFrame(form1)
wrapper2 = LabelFrame(form1)
wrapper3 = LabelFrame(form1)

wrapper1.pack(fill="both", padx=10,pady=10)
wrapper2.pack(fill="both", padx=10,pady=10)

###label
label1 = Label(wrapper1, text="Welcome!", bg='yellow')
label1.pack()

###label
label2 = Label(wrapper1, text="", bg='yellow')
label2.pack()
###

###client-server
udp_socket = 0
def save_test():
    data1 = seed_to_send.get()
    data3 = str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(".","_").replace(":","_")
    melody_randomizer.note_randomizer(data1)
    canvas.delete("all")
    canvas.create_text(50, 15, text="Key: " + str(melody_randomizer.key))
    canvas.create_text(50, 30, text="Seed: " + str(data1))
    canvas.create_text(50, 45, text="Time: " + str(data3))


###label
labelseed = Label(wrapper1, text="Enter seed of random number generator:", bg='yellow')
labelseed.pack()

###
seed_to_send = Entry(wrapper1)
seed_to_send.pack()


play_button1=Button(wrapper1)
play_button1["text"]="Save all"
play_button1["command"]= midi.save_all
play_button1["font"]="-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
play_button1.pack()

play_button2=Button(wrapper1)
play_button2["text"]="Open file"
play_button2["command"]= open_f
play_button2["font"]="-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
play_button2.pack()

play_button3=Button(wrapper1)
play_button3["text"]="Audio play"
play_button3["command"]= play_music
play_button3["font"]="-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
play_button3.pack()

play_button4=Button(wrapper1)
play_button4["text"]="Audio stop"
play_button4["command"]= stop_music
play_button4["font"]="-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
play_button4.pack()

play_button5=Button(wrapper1)
play_button5["text"]="connect to server and melody generate"
play_button5["command"]= save_test
play_button5["font"]="-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
play_button5.pack()


canvas=Canvas(wrapper2)
canvas["height"]=500
canvas["width"]=1000
canvas["background"]="#eeeeff"
canvas["borderwidth"]=2
canvas.pack(side=LEFT)
xscrollbar = ttk.Scrollbar(wrapper2, orient="horizontal", command=canvas.xview)
xscrollbar.pack(side=TOP)
yscrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=canvas.yview)
yscrollbar.pack(side=RIGHT)


canvas.configure(xscrollcommand=xscrollbar.set)
canvas.configure(yscrollcommand=yscrollbar.set)
myframe = Frame(canvas)
canvas.create_window((0,0), window=myframe, anchor="nw")


'''
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="midi_user_db"
)
print(mydb)
query="select * from users"
mycursor = mydb.cursor()

mycursor.execute(query)

myresult = mycursor.fetchall()

canvas.create_text(50, 70, text="Database:")
for x in myresult:
    canvas.create_text(100, 100, text="User:"+str(x))'''

form1.mainloop()


