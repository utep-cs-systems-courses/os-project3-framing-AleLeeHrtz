#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params
from threading import Thread

def servTask(conn, addr):
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)

        file1 = open("encoded.arch", 'rb')

        totalsent = 0
        temp = file1.read()

        while totalsent < len(temp):

            sent = conn.send(temp[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent


        time.sleep(0.25)       # delay 1/4s
        #conn.send(file2.read())
        conn.shutdown(socket.SHUT_WR)
    return


def fileMixer(file1, file2):
    files = [file1, file2]

    file1 = open(files[0], 'rb')
    file2 = open(files[1], 'rb')

    print("Encoding files \"" + str(file1) + "\" and \"" + str(file2) + "\"...")

    encodedarch = open("encoded.arch", 'wb+')

    hdrAndfiles = [str(files[0]).encode(),str(os.stat(files[0]).st_size).encode(), str(files[1]).encode(), str(os.stat(files[1]).st_size).encode(), ]

    for i in range(len(hdrAndfiles)):
        encodedarch.seek(0, 2)
        encodedarch.write(hdrAndfiles[i] + "\n".encode())

    encodedarch.seek(0, 2)
    encodedarch.write(file1.read())

    encodedarch.seek(0, 2)
    encodedarch.write(file2.read())
    print("Done.\n")
    return

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50002),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

#

#
fileMixer("test2.jpg", "test3.jpg")

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)

    t1 = Thread(target=servTask())

    t1.start()

