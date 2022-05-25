import socket

s = socket.socket()

s.bind(('localhost', 8888))
s.listen(1)

c, add = s.accept()
print("connection stablished:", add)
while True:
    msg = input("type msg:")
    c.send(bytes(msg, "utf-8"))
