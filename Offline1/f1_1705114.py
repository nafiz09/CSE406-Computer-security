import socket
from BitVector import *
import time
from f3_1705114 import *
from f4_1705114 import *


s = socket.socket()

s.bind(('localhost', 1234))
s.listen(1)

c, add = s.accept()
print("connection stablished:", add)

key_scheduling_time = 0
encryption_time = 0
round_keys = []


text = input("Plain Text:\n")
print("{} [in ASCII]".format(text))
if len(text) > 16:
    text = text[0:16]
if len(text)<16:
    padding = 16 - len(text)%16
    text = text + " " * padding
AES_input = BitVector(textstring=text)
print("{} [in HEX]\n".format(AES_input.get_bitvector_in_hex()))


while True:
    round_key0 = input("Key:\n")
    if len(round_key0) != 16:
        print("Invalid key size. Please enter valid key.")
    if len(round_key0) == 16:
        break
round_keys.append(BitVector(textstring=round_key0))
print("{} [in ASCII]".format(round_keys[0].get_bitvector_in_ascii()))
print("{} [in HEX]\n".format(round_keys[0].get_bitvector_in_hex()))

k = input("Enter bit size of RSA key:\n")



key_scheduling_time = time.time()
round_keys = gen_round_keys(round_keys)
key_scheduling_time = time.time() - key_scheduling_time


AES_output = BitVector(size=0)
encryption_time = time.time()
AES_output = encrypt(BitVector(textstring=AES_input.get_bitvector_in_ascii()[0:16]),round_keys)
encryption_time = time.time() - encryption_time


print("\n\nCipher Text:")
print("{} [in HEX]".format(AES_output.get_bitvector_in_hex()))
print("{} [in ASCII]".format(AES_output.get_bitvector_in_ascii()))
print("\n\nExecution Time")
print("Key scheduling : {} seconds".format(key_scheduling_time))
print("Encryption Time : {} seconds".format(encryption_time))

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
    st += str(item)

# print(type(st))
# print(st)
c.send(bytes(sr,"utf-8"))
c.send(bytes(AES_output.get_bitvector_in_hex(), "utf-8"))
c.send(bytes(st,"utf-8"))
