#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time
sys.path.append("../lib")       # for params
import params

def fileDecoder():


    restore = open("rF.archServ", 'rb')


    print("Decoding recieved file...")
    metadata = []

    for i in range(4):
        metadata.append(restore.readline())

    fname1 = str(metadata[0])
    fname2 = str(metadata[2])

    fname1 = fname1[1:len(fname1) - 3]
    fname2 = fname2[1:len(fname2) - 3]

    undo = open(fname1, 'wb')
    rest = open(fname2, 'wb')

    undo.write(restore.read(int(metadata[1])))

    rest.write(restore.read())
    print("Done.\n")
    return

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(int(delay))
    print("done sleeping")

chunks = []
print("Connected. Recieving data...")
while 1:
    chunk = s.recv(1024)

    if len(chunk) == 0:
        break


    chunks.append(chunk)


print("Zero length read.  Closing socket...")
s.close()

recievFile = open("rF.archServ", 'wb+')
rejoint =  bytes()

for i in range( len(chunks)):
    rejoint = rejoint + chunks[i]

recievFile.write(rejoint)

recievFile.close()

fileDecoder()
