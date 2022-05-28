import socket
from BitVector import *
import time
from AES import *
from RSA import *


s = socket.socket()

s.bind(('localhost', 4545))
s.listen(1)

c, add = s.accept()
print("connection stablished:", add)

key_scheduling_time = 0
encryption_time = 0
round_keys = []
while True:
    round_key0 = input("Enter initial roundkey: ")
    if len(round_key0) != 16:
        print("Invalid key size. Please enter valid key.")
    if len(round_key0) == 16:
        break
round_keys.append(BitVector(textstring=round_key0))
k = input("Enter bit size of RSA key:")


text = input("Enter your message:")
if len(text) > 16:
    text = text[0:16]
if len(text)<16:
    padding = 16 - len(text)%16
    text = text + " " * padding
AES_input = BitVector(textstring=text)


key_scheduling_time = time.time()
round_keys = gen_round_keys(round_keys)
key_scheduling_time = time.time() - key_scheduling_time


AES_output = BitVector(size=0)
encryption_time = time.time()
AES_output = encrypt(BitVector(textstring=AES_input.get_bitvector_in_ascii()[0:16]),round_keys)
encryption_time = time.time() - encryption_time


print("Ciphered output: {}".format(AES_output.get_bitvector_in_hex()))
print("Key scheduling time: {} seconds".format(key_scheduling_time))
print("Encryption time: {} seconds".format(encryption_time))

publickey,privatekey = Gen_Key(int(k))
CK = rsa_encrypt(publickey,round_key0)

# f = open("Don’t Open this/privatekey.txt", "x")
f = open("Don't Open this/privatekey.txt", "w")
f.write(str(privatekey[0]))
f.write("\n")
f.write(str(privatekey[1]))
f.close()

sr = ""
for i in CK:
    sr += str(i) + ","

# print(CK)

st = ''
for item in publickey:
    st = st + str(item)

# print(st)
c.send(bytes(sr,"utf-8"))
c.send(bytes(AES_output.get_bitvector_in_hex(), "utf-8"))
c.send(bytes(st,"utf-8"))
