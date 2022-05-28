from BitVector import *
import random
import time

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



def rsa_encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def rsa_decrypt(pk, ciphertext):
    key, n = pk
    aux = [str(pow(char, key, n)) for char in ciphertext]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


def report_generation():
    k = 16
    text = input("Enter plain text:\n")
    for i in range(4):
        keygeneration = 0
        encryption = 0
        decryption = 0
        keygeneration = time.time()
        publickey,privatekey = Gen_Key(k)
        keygeneration = time.time()-keygeneration
        encryption = time.time()
        c = rsa_encrypt(publickey,text)
        encryption = time.time()-encryption
        decryption = time.time()
        text = rsa_decrypt(privatekey, c)
        decryption = time.time() - decryption
        # print(text)
        print("k = {}: ".format(k))
        print("Key generation time :{}".format(keygeneration))
        print("Encryption time :{}".format(encryption))
        print("Decryption time :{}".format(decryption))
        k *= 2

def RSA():
    text = input("Enter plain text:\n")
    k = input("Number of bits if key:\n")
    publickey,privatekey = Gen_Key(int(k))
    c = rsa_encrypt(publickey,text)
    deciphered_text = rsa_decrypt(privatekey,c)
    print(deciphered_text)

# RSA()

# report_generation()


