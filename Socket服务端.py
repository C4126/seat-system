from socket import *

IP='127.0.0.1'
PORT=50000
BUFLEN=512

listenSocket=socket(AF_INET,SOCK_STREAM)
listenSocket.bind((IP,PORT))

listenSocket.listen(10)
print(f'服务端启动成功，在{PORT}端口等待客户端连接')

dataSocket,addr=listenSocket.accept()
print('接受一个客户端连接：',addr)

while True:
    recved=dataSocket.recv(BUFLEN)
    if not recved:
        break
    info=recved.decode()
    print(f'收到信息：{info}')
    dataSocket.send(f'服务端接受信息{info}'.encode())

dataSocket.close()
listenSocket.close()