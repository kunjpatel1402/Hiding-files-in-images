import base64
import random
import string

def gf_degree(a) :
    res = 0
    a >>= 1
    while (a != 0) :
        a >>= 1
        res += 1
    return res

def gf_invert(a, mod=0x1B) :
    if a==0:
        return 0
    else:
        v = mod
        g1 = 1
        g2 = 0
        j = gf_degree(a) - 8
        while (a != 1) :
            if (j < 0) :
                a, v = v, a
                g1, g2 = g2, g1
                j = -j
            a ^= v << j
            g1 ^= g2 << j
            a %= 256  
            g1 %= 256 
            j = gf_degree(a) - gf_degree(v)
        return g1

# above part taken from https://stackoverflow.com/questions/45442396/a-pure-python-way-to-calculate-the-multiplicative-inverse-in-gf28-using-pytho

def decimalToBinary(n):
    s =  bin(n).replace("0b","")
    s = "0"*(8-len(s)) + s
    return s

def left_shift(input,num):
    byte = decimalToBinary(input)
    byte = byte[num:8]+byte[0:num]
    return int(byte,2)

def forward_S_box(num):
    inverse_num = gf_invert(num)
    S_box_output = inverse_num^(left_shift(inverse_num,1))^(left_shift(inverse_num,2))^(left_shift(inverse_num,3))^(left_shift(inverse_num,4))^99
    return (S_box_output)

def reverse_S_box(num):
    inverse_S_box_output = left_shift(num,1)^left_shift(num,3)^left_shift(num,6)^5
    return (gf_invert(inverse_S_box_output))

def xor(byte1,byte2):
    return (byte1)^(byte2)

def RotWord(Word):
    e = Word[0]
    Word.remove(e)
    Word.append(e)
    return Word

def SubWord(Word):
    return [forward_S_box(Word[0]),forward_S_box(Word[1]),forward_S_box(Word[2]),forward_S_box(Word[3])]

def expand_key(key):
    rcon = [[1,0,0,0],
            [2,0,0,0],
            [4,0,0,0],
            [8,0,0,0],
            [16,0,0,0],
            [32,0,0,0],
            [64,0,0,0],
            [128,0,0,0],
            [27,0,0,0],
            [54,0,0,0]]
    #print(key,len(key))
    index=0
    k0 = [int(key[index+0:index+8],2),int(key[index+8:index+16],2),int(key[index+16:index+24],2),int(key[index+24:index+32],2)]
    index+=32
    k1 = [int(key[index+0:index+8],2),int(key[index+8:index+16],2),int(key[index+16:index+24],2),int(key[index+24:index+32],2)]
    index+=32
    k2 = [int(key[index+0:index+8],2),int(key[index+8:index+16],2),int(key[index+16:index+24],2),int(key[index+24:index+32],2)]
    index+=32
    k3 = [int(key[index+0:index+8],2),int(key[index+8:index+16],2),int(key[index+16:index+24],2),int(key[index+24:index+32],2)]
    expanded_keys=[k0,k1,k2,k3]
    for i in range(4,44):
        if (i >= 4) and (i%4 == 0):
            term1 = expanded_keys[i-4]
            term2 = SubWord(RotWord(expanded_keys[i-1]))
            term3 = rcon[(i//4)-1]
            final_term = []
            for j in range(0,4):
                final_term.append(xor(xor(term1[j],term2[j]),term3[j]))
            expanded_keys.append(final_term)
        else:
            term1=expanded_keys[i-4]
            term2=expanded_keys[i-1]
            final_term=[]
            for j in range(0,4):
                final_term.append(xor(term1[j],term2[j]))
            expanded_keys.append(final_term)
    return expanded_keys


def binary_to_matrix(key):
    index=0
    k0 = [key[index+0:index+8],key[index+8:index+16],key[index+16:index+24],key[index+24:index+32]]
    index+=32
    k1 = [key[index+0:index+8],key[index+8:index+16],key[index+16:index+24],key[index+24:index+32]]
    index+=32
    k2 = [key[index+0:index+8],key[index+8:index+16],key[index+16:index+24],key[index+24:index+32]]
    index+=32
    k3 = [key[index+0:index+8],key[index+8:index+16],key[index+16:index+24],key[index+24:index+32]]
    return [k0,k1,k2,k3]

def matrix_Xor(matrix,key):
    for i in range(0,4):
        for j in range(0,4):
            matrix[i][j] = xor(matrix[i][j],key[i][j])
    return matrix

def SubBytes(matrix):
    for i in range(0,4):
        for j in range(0,4):
            matrix[i][j] = forward_S_box(matrix[i][j])
    return matrix

def RevSubBytes(matrix):
    for i in range(0,4):
        for j in range(0,4):
            matrix[i][j] = reverse_S_box(matrix[i][j])
    return matrix

def gf_mul(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256
#gf_mul() taken from http://blog.simulacrum.me/2019/01/aes-galois/
def MixColumns(matrix):
    for i in range(0,4):
        a = (gf_mul(matrix[i][0],2))^(gf_mul(matrix[i][1],3))^(gf_mul(matrix[i][2],1))^(gf_mul(matrix[i][3],1))
        b = (gf_mul(matrix[i][0],1))^(gf_mul(matrix[i][1],2))^(gf_mul(matrix[i][2],3))^(gf_mul(matrix[i][3],1))
        c = (gf_mul(matrix[i][0],1))^(gf_mul(matrix[i][1],1))^(gf_mul(matrix[i][2],2))^(gf_mul(matrix[i][3],3))
        d = (gf_mul(matrix[i][0],3))^(gf_mul(matrix[i][1],1))^(gf_mul(matrix[i][2],1))^(gf_mul(matrix[i][3],2))
        matrix[i]=[a,b,c,d]
    return matrix

def RevMixColumns(matrix):
    for i in range(0,4):
        a = (gf_mul(matrix[i][0],14))^(gf_mul(matrix[i][1],11))^(gf_mul(matrix[i][2],13))^(gf_mul(matrix[i][3],9))
        b = (gf_mul(matrix[i][0],9))^(gf_mul(matrix[i][1],14))^(gf_mul(matrix[i][2],11))^(gf_mul(matrix[i][3],13))
        c = (gf_mul(matrix[i][0],13))^(gf_mul(matrix[i][1],9))^(gf_mul(matrix[i][2],14))^(gf_mul(matrix[i][3],11))
        d = (gf_mul(matrix[i][0],11))^(gf_mul(matrix[i][1],13))^(gf_mul(matrix[i][2],9))^(gf_mul(matrix[i][3],14))
        matrix[i]=[a,b,c,d]
    return matrix



def ShiftRows(matrix):
    temp = matrix[0][1]
    matrix[0][1] = matrix[1][1]
    matrix[1][1] = matrix[2][1]
    matrix[2][1] = matrix[3][1]
    matrix[3][1] = temp
    temp1 = matrix[0][2]
    temp2 = matrix[1][2]
    matrix[0][2] = matrix[2][2]
    matrix[1][2] = matrix[3][2]
    matrix[2][2] = temp1
    matrix[3][2] = temp2
    temp = matrix[3][3]
    matrix[3][3] = matrix[2][3]
    matrix[2][3] = matrix[1][3]
    matrix[1][3] = matrix[0][3]
    matrix[0][3] = temp
    return matrix

def RevShiftRows(matrix):
    temp = matrix[3][1]
    matrix[3][1] = matrix[2][1]
    matrix[2][1] = matrix[1][1]
    matrix[1][1] = matrix[0][1]
    matrix[0][1] = temp
    temp1 = matrix[3][2]
    temp2 = matrix[2][2]
    matrix[3][2] = matrix[1][2]
    matrix[2][2] = matrix[0][2]
    matrix[1][2] = temp1
    matrix[0][2] = temp2
    temp = matrix[0][3]
    matrix[0][3] = matrix[1][3]
    matrix[1][3] = matrix[2][3]
    matrix[2][3] = matrix[3][3]
    matrix[3][3] = temp
    return matrix

def decimal_matrix(matrix):
    for i in range(0,4):
        for j in range(0,4):
            matrix[i][j] = int(matrix[i][j],2)
    return matrix


def binary_matrix(matrix):
    for i in range(0,4):
        for j in range(0,4):
            matrix[i][j] = decimalToBinary(matrix[i][j])
    return matrix

def AES_encrypt(matrix,key):
    matrix=decimal_matrix(matrix)
    #print(key)
    #initial round
    matrix=matrix_Xor(matrix,[key[0],key[1],key[2],key[3]])
    #main round
    i = 4
    while i < 40:
        matrix = SubBytes(matrix)
        #shift rows
        matrix = ShiftRows(matrix)
        #mix columns
        matrix = MixColumns(matrix)
        #Add round key
        matrix = matrix_Xor(matrix,[key[i+0],key[i+1],key[i+2],key[i+3]])
        i += 4
    matrix = SubBytes(matrix)
    #shift rows
    matrix = ShiftRows(matrix)
    #Add round key
    matrix = matrix_Xor(matrix,[key[i+0],key[i+1],key[i+2],key[i+3]])
    #print(matrix)
    matrix=binary_matrix(matrix)
    return matrix

def AES_decrypt(matrix,key):
    matrix=decimal_matrix(matrix)
    matrix=matrix_Xor(matrix,[key[40],key[41],key[42],key[43]])
    i=36
    while i >= 4:
        #shift rows
        matrix = RevShiftRows(matrix)
        matrix = RevSubBytes(matrix)
        #Add round key
        matrix = matrix_Xor(matrix,[key[i+0],key[i+1],key[i+2],key[i+3]])
        #arrange columns
        matrix = RevMixColumns(matrix)
        i -= 4
    #shift rows
    matrix = RevShiftRows(matrix)
    matrix = RevSubBytes(matrix)
    #Add round key
    matrix = matrix_Xor(matrix,[key[i+0],key[i+1],key[i+2],key[i+3]])
    matrix=binary_matrix(matrix)
    return matrix

def matrix_to_string(matrix):
    s=""
    for i in range(0,4):
        for j in range(0,4):
            s += matrix[i][j]
    return s

def verify():
    key=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation) for _ in range(16))
    key=str(''.join(format(ord(i), '08b') for i in key))
    print(key,len(key))
    key = expand_key(key)
    #s = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation) for _ in range(16))
    #s=str(''.join(format(ord(i), '08b') for i in s))
    s="01"*64
    print(s,len(s))
    temp = s
    s = matrix_to_string(AES_encrypt(binary_to_matrix(s),key))
    print(s,len(s))
    s = matrix_to_string(AES_decrypt(binary_to_matrix(s),key))
    print(s,len(s))
    print(s==temp)

#verify()