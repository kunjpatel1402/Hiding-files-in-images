import sys
from binary_to_image import binary_to_image
from image_to_binary import image_to_binary
import crypto


def encrypt(binary_data,key):
    i = 0
    print("->Ecrypting data....")
    s=""
    while i < ((len(binary_data)//128)*128):
        s+=crypto.matrix_to_string(crypto.AES_encrypt(crypto.binary_to_matrix(binary_data[i:i+128]),key))
        i+=128
    s+=binary_data[i:i+(len(binary_data)%128)]
    binary_data=s
    return binary_data

def decrypt(binary_data,key):
    i = 0
    s=""
    print("->Decrypting data....")
    while i < ((len(binary_data)//128)*128):
        s+=crypto.matrix_to_string(crypto.AES_decrypt(crypto.binary_to_matrix(binary_data[i:i+128]),key))
        i+=128
    s+=binary_data[i:i+(len(binary_data)%128)]
    binary_data=s
    return binary_data


def file_to_binary(file_path):
    binary_data = ""
    print("->Reading data....")
    with open(file_path,"rb") as file:
        byte = file.read(1)
        count=0
        while byte:
            s='{0:08b}'.format(int.from_bytes(byte, byteorder=sys.byteorder))
            binary_data += s
            byte=file.read(1)
            count+=1
        file.close()
    return binary_data
    
def binary_to_file(binary_data,file_name):
    with open(file_name,"wb") as file:
        print("->Writing to file....")
        i = 0
        while i < len(binary_data):
            s=binary_data[i:i+8]
            try:
                file.write(int(s, 2).to_bytes(len(s) // 8, byteorder='little'))
            except:
                print(s)
                break
            i+=8
        print("->File is ready....")
        file.close()

def hide(file_path,image_path,key):
    binary_data = file_to_binary(file_path)
    encrypted = encrypt(binary_data,key)
    binary_to_image(image_path,encrypted)

def reveal(file_path,image_path,key):
    encrypted=image_to_binary(image_path)
    decrypted = decrypt(encrypted,key)
    binary_to_file(decrypted,file_path)

