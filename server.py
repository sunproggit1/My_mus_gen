# Модуль socket для сетевого программирования
import datetime
from socket import *
import threading
import logging
import time
# данные сервера
import mysql.connector

host1 = 'localhost'
port1 = 8686
addr1 = (host1, port1)

host2 = 'localhost'
port2 = 9443
addr2 = (host2, port2)
# socket - функция создания сокета
# первый параметр socket_family может быть AF_INET или AF_UNIX
# второй параметр socket_type может быть SOCK_STREAM(для TCP) или SOCK_DGRAM(для UDP)
udp_socket1 = socket(AF_INET, SOCK_DGRAM)
udp_socket2 = socket(AF_INET, SOCK_DGRAM)
# bind - связывает адрес и порт с сокетом
udp_socket1.bind(addr1)
udp_socket2.bind(addr2)

try:
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
    for x in myresult:
        print(x)

    mycursor.close()
    mycursor = mydb.cursor()
    query1="select username from users"

    mycursor.execute(query1)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    mycursor.close()


    #mydb.close()
except error:
    print(error,"Not connected")

date_data = 0
def thread_function1(name):
    global date_data
    logging.info("Thread %s: starting", name)
    # Бесконечный цикл работы программы
    while True:
        # Если мы захотели выйти из программы
        # question = input('Do you want to quit? y\\n: ')
        # if question == 'y': break

        print('server1 wait data...')
        # recvfrom - получает UDP сообщения

        seed_data, addr = udp_socket1.recvfrom(1024)
        # key_data, addr = udp_socket.recvfrom(1024)
        #date_data = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(".", "_").replace(":", "_")
        if date_data == 0:
            date_data = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_"). \
                replace(".", "_").replace(":", "_")
        print('client addr: ', addr)
        # print('client key: ', key_data)
        print('client seed: ', seed_data)
        print('client datetime: ', date_data)
        data1 = "Successful!! "
        data1 = str.encode(data1)
        udp_socket1.sendto(data1, addr)

        data_time = date_data
        data_time = str.encode(data_time)
        udp_socket1.sendto(data_time, addr)
        # sendto - передача сообщения UDP
        # udp_socket.sendto(b'message received by the server', addr)
    udp_socket1.close()
    logging.info("Thread %s: finishing", name)


def thread_function2(name):
    logging.info("Thread %s: starting", name)
    # Бесконечный цикл работы программы
    while True:
        # Если мы захотели выйти из программы
        # question = input('Do you want to quit? y\\n: ')
        # if question == 'y': break

        print('server2 wait data...')
        # recvfrom - получает UDP сообщения

        date_data = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(".", "_").replace(":", "_")

        username_data, addr = udp_socket2.recvfrom(1024)

        firstname_data, addr = udp_socket2.recvfrom(1024)

        lastname_data, addr = udp_socket2.recvfrom(1024)

        email_data, addr = udp_socket2.recvfrom(1024)
        # key_data, addr = udp_socket.recvfrom(1024)
        username_data = bytes.decode(username_data)
        firstname_data = bytes.decode(firstname_data)
        lastname_data = bytes.decode(lastname_data)
        email_data = bytes.decode(email_data)

        print('client addr: ', addr)
        # print('client key: ', key_data)
        print('client username: ', username_data)
        print('client firstname: ', firstname_data)
        print('client lastname: ', lastname_data)
        print('client email: ', email_data)
        print('client date: ', date_data)

        try:
            query = "insert into users values(Null,%s,%s,%s,%s,%s)"
            print(query)
            mycursor = mydb.cursor()
            mycursor.execute(query, (username_data,firstname_data,lastname_data, email_data, date_data))
            mydb.commit()
            mycursor.close()

            print("Data succesfully inserted!")
            query = "select id from users where date=(%s)"
            print(query)
            mycursor = mydb.cursor()
            mycursor.execute(query, (date_data,))
            myresult = mycursor.fetchall()
            for x in myresult:
                userid=x
            mycursor.close()
            print(userid[0])

        except error:
            print(error,"Not connected to database")

        data1 = str.encode(str(userid[0]))
        udp_socket2.sendto(data1, addr)
        data_time = date_data
        data_time = str.encode(data_time)
        udp_socket2.sendto(data_time, addr)
        # sendto - передача сообщения UDP
        # udp_socket.sendto(b'message received by the server', addr)
    udp_socket2.close()
    mycursor.close()
    mydb.close()
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    server1 = threading.Thread(target=thread_function1, args=(1,))
    logging.info("Main    : before running thread")
    server1.start()
    server2 = threading.Thread(target=thread_function2, args=(2,))
    server2.start()
    logging.info("Main    : wait for the thread to finish")

    logging.info("Main    : all done")