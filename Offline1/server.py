import socket
from BitVector import *
import time

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

s = socket.socket()

s.bind(('localhost', 1234))
s.listen(1)

c, add = s.accept()
print("connection stablished:", add)

round_keys = []
AES_modulus = BitVector(bitstring="100011011")

key_scheduling_time = 0

encryption_time = 0

def sub_sbox(bitvector):
    sub_bitvector = BitVector(size=0)

    for i in range(0, bitvector.length(), 8):
            index = bitvector[i: i+8].intValue()
            sub_bitvector += BitVector(intVal=Sbox[index], size=8)
    return sub_bitvector


def g(w3,round_constant):
    w3 = w3 << 8
    w3 = sub_sbox(w3)
    w3 = w3^round_constant

    return w3


while True:
    round_key0 = input("Enter initial roundkey: ")
    if len(round_key0) != 16:
        print("Invalid key size. Please enter valid key.")
    if len(round_key0) == 16:
        break
round_keys.append(BitVector(textstring=round_key0))


text = input("Enter your message:")
if len(text) > 16:
    text = text[0:16]
if len(text)<16:
    padding = 16 - len(text)%16
    text = text + " " * padding
AES_input = BitVector(textstring=text)

def gen_round_keys():
    rc = BitVector(hexstring="01")
    multiplier = BitVector(hexstring="02")
    for i in range(10):
        round_constant = BitVector(hexstring=rc.get_bitvector_in_hex())
        round_constant += BitVector(hexstring="000000")

        w_0 = round_keys[i][0: 32] ^ g(round_keys[i][96: 128],round_constant)
        w_1 = w_0 ^ round_keys[i][32: 64]
        w_2 = w_1 ^ round_keys[i][64: 96]
        w_3 = w_2 ^ round_keys[i][96: 128]

        this_roundkey = w_0
        this_roundkey += w_1
        this_roundkey += w_2
        this_roundkey += w_3
        round_keys.append(this_roundkey)
        rc = multiplier.gf_multiply_modular(rc, BitVector(bitstring="100011011"), 8)
        # print(this_roundkey.get_bitvector_in_hex())


key_scheduling_time = time.time()
gen_round_keys()
key_scheduling_time = time.time() - key_scheduling_time


def convert_bitvector_into_matrix(bitvector):
    state_matrix = [[0 for x in range(4)] for y in range(4)]

    for i in range(4):
        for j in range(4):
            state_matrix[j][i] = bitvector[(i*32+j*8):(i*32+j*8)+8]

    return state_matrix

def convert_matrix_into_bitvector(state_matrix):
    shifted_bitvector = BitVector(size=0)

    for i in range(4):
        for j in range(4):
            shifted_bitvector += state_matrix[j][i]

    return shifted_bitvector

def shift_rows(bitvector):
    state_matrix = convert_bitvector_into_matrix(bitvector)

    state_matrix[0] = state_matrix[0][0:] + state_matrix[0][: 0]
    state_matrix[1] = state_matrix[1][1:] + state_matrix[1][: 1]
    state_matrix[2] = state_matrix[2][2:] + state_matrix[2][: 2]
    state_matrix[3] = state_matrix[3][3:] + state_matrix[3][: 3]

    return convert_matrix_into_bitvector(state_matrix)

def mix_column(bitvector):
    result_matrix = []
    matrix = convert_bitvector_into_matrix(bitvector)
    for i in range(4):
        result_matrix_row = []

        for j in range(4):
            temp = Mixer[i][0].gf_multiply_modular(matrix[0][j], AES_modulus, 8)
            temp ^= Mixer[i][1].gf_multiply_modular(matrix[1][j], AES_modulus, 8)
            temp ^= Mixer[i][2].gf_multiply_modular(matrix[2][j], AES_modulus, 8)
            temp ^= Mixer[i][3].gf_multiply_modular(matrix[3][j], AES_modulus, 8)
            result_matrix_row.append(temp)

        result_matrix.append(result_matrix_row)

    return convert_matrix_into_bitvector(result_matrix)


def encrypt(bitvector):
    bitvector = bitvector ^ round_keys[0]

    for i in range(9):
        bitvector = mix_column(shift_rows(sub_sbox(bitvector))) ^ round_keys[i+1]

    bitvector = shift_rows(sub_sbox(bitvector)) ^ round_keys[10]

    return bitvector



encryption_time = time.time()
AES_output = BitVector(size=0)
AES_output = encrypt(BitVector(textstring=AES_input.get_bitvector_in_ascii()[0:16]))
encryption_time = time.time() - encryption_time


print("Ciphered output: {}".format(AES_output.get_bitvector_in_hex()))

print("Key scheduling time: {} seconds".format(key_scheduling_time))
print("Encryption time: {} seconds".format(encryption_time))





# print(AES_output)

a = BitVector(size=0)
a += BitVector(textstring="Two one nine two")
# b = a.get_bitvector_in_hex()
# d = a.get_bitvector_in_ascii()
# print(d)
# while True:
#     msg = b
#     print(type(msg))
c.send(bytes(AES_output.get_bitvector_in_hex(), "utf-8"))
