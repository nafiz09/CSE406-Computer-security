from BitVector import *
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def Gen_Key(k):
    bv = BitVector(intVal = 0)
    while True:
        bv = bv.gen_random_bits(int(k/2))
        check = bv.test_for_primality()
        if check != 0:
            break
    # print(bv.get_bitvector_in_hex())
    # print(bv.intValue())

    p = bv.intValue()

    while True:
        bv = bv.gen_random_bits(int(k/2))
        check = bv.test_for_primality()
        if check != 0:
            break
    # print(bv.get_bitvector_in_hex())
    # print(bv.intValue())

    q = bv.intValue()

    phi = (p-1)*(q-1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    E = BitVector(intVal = e)
    PHI = BitVector(intVal = phi)

    d = int(E.multiplicative_inverse(PHI))

    publickey = (e,p*q)
    privatekey = (d,p*q)
    return publickey,privatekey
    # print(publickey)
    # print(privatekey)

# a,b = Gen_Key(16)
#
# print(a)
# print(b)
# print(str(b))


def rsa_encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # Return the array of bytes
    return cipher

def rsa_decrypt(pk, ciphertext):
    key, n = pk
    aux = [str(pow(char, key, n)) for char in ciphertext]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


# c = encrypt(a,"Thats my Kung Fu")
# sr = ""
# print(c)
# for i in c:
#     sr += str(i) + ","
#
# print(sr)
#
# t = sr.split(",")
# s = []
# # print(len(t))
# for k in range(len(t)-1):
#     print(t[k])
#     al = int(t[k])
#     s.append(al)
#
# print(s)
# print(s==c)
#
# # print(cipher)
#
#
# print(decrypt(b,s))

