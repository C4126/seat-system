from socket import *

IP='127.0.0.1'
SERVER_PORT=50000
BUFLEN=512

dataSocket=socket(AF_INET,SOCK_STREAM)
dataSocket.connect((IP,SERVER_PORT))

while True:
    toSend=input('>>')
    if toSend=='':
        break
    dataSocket.send(toSend.encode())
    recved=dataSocket.recv(BUFLEN)
    if not recved:
        break
    print(recved.decode())

dataSocket.close()