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

'''choice=input("1. write to image\n2. read from image\n3. anything else to break\n:")
if choice=="1":
    file_path=input("enter full path to file to be written:")
    image_path=input("enter full path to image you want to write to:")
    print("Enter 1 to use your own key(should be 32 characters long), 2 for using a randomly generated key",end="")
    ans=input(":")
    if (ans=='1'):
        key = input("key:")
    else:
        key=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation) for _ in range(32))
        print("Here's your key please remember it:",key)
    key = crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
    hide(file_path,image_path,key)
elif choice=="2":
    file_path=input("enter full file path with extention:")
    image_path=input("enter full path to image:")
    key=input("Enter key:")
    key = crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
    reveal(file_path,image_path,key)
else:
    pass
'''

'''
hide("data.zip","Screenshot (70).jpeg",key)
reveal("temp.zip","new_img.png",key)
'''
'''
binary_data = file_to_binary("data.zip")
encrypted = encrypt(binary_data,key)
binary_to_image("Screenshot (70).jpeg",encrypted)
encrypted=image_to_binary("new_img.png")
decrypted = decrypt(encrypted,key)
print(decrypted==binary_data)
binary_to_file(decrypted,"temp.zip")'''
