import socket
s = socket.socket()
s.connect(('localhost',8888))

while True:
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
