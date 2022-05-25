import socket
from BitVector import *



s = socket.socket()
s.connect(('localhost',1112))

# while True:
a = BitVector(size=0)
msg = s.recv(1024)
a += BitVector(hexstring=msg.decode("utf-8"))
print(msg)
print(a.get_bitvector_in_ascii())
