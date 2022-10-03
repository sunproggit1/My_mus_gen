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

registered = False
###client-server

client_data = False

###
no_tension = 0
dominant_tension = 0
subdominant_tension = 0
dominant_parallel_tension = 0
subdominant_parallel_tension = 0
###userid for database
data_userid = 0
###Pagination
class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self["bg"] = ("#33aacc")
        label = Label(self, text="This is page 1")
        label.pack(side="top")

class Page2(Page):
    global registered
    def __init__(self, *args, **kwargs):
        global data_userid
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)

        frame = Frame(self)
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

        wrapper1 = LabelFrame(self)
        wrapper2 = LabelFrame(self)

        wrapper1.pack(fill="both", padx=10, pady=10)
        wrapper2.pack(fill="both", padx=10, pady=10)

        ###label
        label1 = Label(wrapper1, text="Welcome!", bg='yellow')
        label1.pack()

        ###label
        label2 = Label(wrapper1, text="", bg='yellow')
        label2.pack()
        ###

        ###client-server
        udp_socket1 = 0

        def connect_to_server1():
            global udp_socket1
            host1 = 'localhost'
            port1 = 8686
            addr1 = (host1, port1)
            try:
                udp_socket1 = socket(AF_INET, SOCK_DGRAM)

                client_data = True
                if client_data == True:
                    # while True:
                    # data1 = input('write to server: (if you want to quit - write "quit")')
                    data1 = seed_to_send.get()
                    # data2 = init_key_to_send.get()
                    '''if data1 == "quit":
                        break
                        udp_socket.close()
                        sys.exit(1)'''
                    data1 = str.encode(data1)
                    # data2 = str.encode(data2)
                    udp_socket1.sendto(data1, addr1)
                    # udp_socket.sendto(data2, addr)
                    data3,addr1 = udp_socket1.recvfrom(1024)
                    data3 = bytes.decode(data3)
                    # print(data2)
                    label2["text"] += str(data3) + '\n'

                    data3, addr1 = udp_socket1.recvfrom(1024)
                    data3 = bytes.decode(data3)

                    # udp_socket.close()
                    melody_randomizer.note_randomizer(data1)

                canvas.delete("all")
                canvas.create_text(100, 15, text="Key: " + str(melody_randomizer.key))
                canvas.create_text(100, 30, text="Seed: " + str(data1))
                canvas.create_text(100, 45, text="Time: " + str(data3))

            except:
                print("Connection Aborted. Host is not reachable")

        def disconnect_from_server1():
            global udp_socket1
            udp_socket1.close()
            print("Connection aborted.")

            ##save files in midi
        def save():
            midi.save_all(data_userid, seed_to_send.get())
        ###label
        labelseed = Label(wrapper1, text="Enter seed of random number generator:", bg='yellow')
        labelseed.pack()

        ###
        seed_to_send = Entry(wrapper1)
        seed_to_send.pack()

        ############buttons

        play_button1 = Button(wrapper1,width=30,height=1)
        play_button1["text"] = "Save all"
        play_button1["command"] = save
        play_button1["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        play_button1.pack(side=TOP)

        play_button2 = Button(wrapper1,width=30,height=1)
        play_button2["text"] = "Open file"
        play_button2["command"] = open_f
        play_button2["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        play_button2.pack(side=TOP)

        play_button3 = Button(wrapper1,width=30,height=1)
        play_button3["text"] = "Audio play"
        play_button3["command"] = play_music
        play_button3["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        play_button3.pack(side=TOP)

        play_button4 = Button(wrapper1,width=30,height=1)
        play_button4["text"] = "Audio stop"
        play_button4["command"] = stop_music
        play_button4["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        play_button4.pack(side=TOP)

        play_button5 = Button(wrapper1,width=30,height=1)
        play_button5["text"] = "connect to server and melody generate"
        play_button5["command"] = connect_to_server1
        play_button5["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        play_button5.pack(side=TOP)

        play_button6 = Button(wrapper1,width=30,height=1)
        play_button6["text"] = "disconnect from server"
        play_button6["command"] = disconnect_from_server1
        play_button6["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        play_button6.pack(side=TOP)

        canvas = Canvas(wrapper2)
        canvas["height"] = 500
        canvas["width"] = 1000
        canvas["background"] = "#33aacc"
        canvas["borderwidth"] = 2
        canvas.pack(side=LEFT)
        yscrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=canvas.yview)
        yscrollbar.pack(side=RIGHT)

        canvas.configure(yscrollcommand=yscrollbar.set)
        myframe = Frame(canvas)
        canvas.create_window((0, 0), window=myframe, anchor="nw")
        '''canvas.create_text(50, 15, text="Key: ")
        canvas.create_text(50, 25, text="Seed: ")
        canvas.create_text(50, 35, text="Time: ")'''

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
            canvas.create_text(100, 100, text="User:"+str(x))
        '''

    def show(self):
        if registered == True:
            self.lift()
        else:
            msg = "Сначала заполните дневник-форму"
            mb.showwarning("Предупреждение", msg)

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        p1 = Page1(self)
        p2 = Page2(self)
        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        lbl1 = Label(p1, text="User Name", height=1, width=30)
        lbl1.pack()
        entry_username = Entry(p1)
        entry_username.pack()
        lbl2 = Label(p1, text="First Name", height=1, width=30)
        lbl2.pack()
        entry_firstname = Entry(p1)
        entry_firstname.pack()
        lbl3 = Label(p1, text="Last Name", height=1, width=30)
        lbl3.pack()
        entry_lastname = Entry(p1)
        entry_lastname.pack()
        lbl4 = Label(p1, text="Email", height=1, width=30)
        lbl4.pack()
        entry_email = Entry(p1)
        entry_email.pack()

        ###client-server
        udp_socket2 = 0
        def register():

            global data_userid
            global registered
            if entry_username.get()=="" or entry_firstname.get()=="" or entry_lastname.get()=="" or entry_email.get()=="":
                msg="Сначала заполните форму!"
                mb.showwarning("Предупреждение!",msg)
            else:
                registered = True
                print(entry_username.get())
                print(entry_firstname.get())
                print(entry_lastname.get())
                print(entry_email.get())
                global udp_socket2
                host2 = 'localhost'
                port2 = 9443
                addr2 = (host2, port2)
                try:
                    udp_socket2 = socket(AF_INET, SOCK_DGRAM)
                    client_data = True
                    if client_data == True:
                        # while True:
                        # data1 = input('write to server: (if you want to quit - write "quit")')
                        data1 = entry_username.get()
                        data2 = entry_firstname.get()
                        data3 = entry_lastname.get()
                        data4 = entry_email.get()
                        # data2 = init_key_to_send.get()
                        '''if data == "quit":
                            break
                            udp_socket.close()
                            sys.exit(1)'''
                        data1 = str.encode(data1)
                        data2 = str.encode(data2)
                        data3 = str.encode(data3)
                        data4 = str.encode(data4)
                        # data2 = str.encode(data2)
                        udp_socket2.sendto(data1, addr2)
                        udp_socket2.sendto(data2, addr2)
                        udp_socket2.sendto(data3, addr2)
                        udp_socket2.sendto(data4, addr2)
                        # udp_socket.sendto(data2, addr)
                        data_userid,addr = udp_socket2.recvfrom(1024)
                        data_userid = bytes.decode(data_userid)
                        print(data_userid)

                        data_time, addr1 = udp_socket2.recvfrom(1024)
                        data_time = bytes.decode(data_time)
                        print(data_time)
                        if(data_userid and data_time):
                            p2.show()
                            print(registered)

                            print("Connection succesfully finished.")
                        else:
                            print("Something wrong")


                except:
                    print("Connection Aborted. Host is not reachable")


        def unregister():
            global registered
            global upd_socket2
            registered = False
            print("Unregistered!")
            udp_socket2.close()

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        buttonframe["bg"] = ("#33aacc")
        container["bg"] = ("#33aacc")

        b1 = Button(buttonframe, text="Page 1", command=p1.show)
        b2 = Button(buttonframe, text="Page 2", command=p2.show)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()

        btn = Button(p1)
        btn["text"] = "Submit"
        btn["command"] = register
        btn["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        btn.pack()
        unregbtn = Button(p1)
        unregbtn["text"] = "Unregister"
        unregbtn["command"] = unregister
        unregbtn["font"] = "-*-terminus-*-r-*-*-12-*-*-*-*-*-*-*"
        unregbtn.pack()

if __name__ == "__main__":
    root = Tk()
    root.title("Midi file generator")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x600")
    root["bg"]=("#33aacc")

    root.mainloop()
