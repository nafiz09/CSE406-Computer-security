import socket
from BitVector import *
from AES import *
import time
from RSA import *

s = socket.socket()
s.connect(('localhost',4545))

AES_output = BitVector(size=0)
decipher_output = BitVector(size=0)
decryption_time = 0

a = BitVector(size=0)
msg = s.recv(1024)
# print(msg.decode("utf-8"))
keystring = msg.decode("utf-8")
t = keystring.split(",")
CK = []

for i in range(len(t)-1):
    CK.append(int(t[i]))

pk1 = open("Don't Open this/privatekey.txt", "r")
token = pk1.read().split("\n")

privatekey = (int(token[0]),int(token[1]))

key = rsa_decrypt(privatekey,CK)
# print(key)

ms = s.recv(1024)
AES_output += BitVector(hexstring=ms.decode("utf-8"))
# print(msg.decode("utf-8"))
#print(decipher_output.get_bitvector_in_ascii())
publickey = s.recv(1024)
print(publickey.decode("utf-8"))

round_keys = []

round_keys.append(BitVector(textstring=key))

round_keys = gen_round_keys(round_keys)
# print(round_keys)

decryption_time = time.time()
decipher_output += decrypt(BitVector(hexstring=AES_output.get_bitvector_in_hex()[0:32]),round_keys)
decryption_time = time.time() - decryption_time


print("Deciphered text [in ASCII]: {}".format(decipher_output.get_bitvector_in_ascii()))
print("Decryption time: {} seconds".format(decryption_time))

