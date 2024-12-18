import socket

s = socket.socket()
host = socket.gethostname()
port = 12312
s.bind((host, port))

s.listen(5)
c,addr = s.accept()
seat_number = c.recv(1024)
c.send('OK')
while True:
    c.recv(1024)