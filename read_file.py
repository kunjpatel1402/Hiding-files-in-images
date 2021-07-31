import sys
from binary_to_image import binary_to_image
from image_to_binary import image_to_binary
'''
binary_data = ""
with open(r"","rb") as file:
    byte = file.read(2)
    count=0
    while byte:
        s='{0:016b}'.format(int.from_bytes(byte, byteorder=sys.byteorder))
        #print(byte,int(s, 2).to_bytes(len(s) // 8, byteorder='little'))
        binary_data += s
        byte=file.read(2)
        count+=1
    file.close()

binary_to_image(r"",binary_data)
print(image_to_binary(r"")==binary_data)

with open(r"    ","wb") as file:
    i = 0
    while i < len(binary_data):
        s=binary_data[i:i+16]
        try:
            file.write(int(s, 2).to_bytes(len(s) // 8, byteorder='little'))
        except:
            print(s)
            break
        i+=16
    file.close()
'''

def file_to_binary(file_path):
    binary_data = ""
    with open(file_path,"rb") as file:
        byte = file.read(2)
        count=0
        while byte:
            s='{0:016b}'.format(int.from_bytes(byte, byteorder=sys.byteorder))
            #print(byte,int(s, 2).to_bytes(len(s) // 8, byteorder='little'))
            binary_data += s
            byte=file.read(2)
            count+=1
        file.close()
    return binary_data

def binary_to_file(binary_data,file_name):
    with open(file_name,"wb") as file:
        i = 0
        while i < len(binary_data):
            s=binary_data[i:i+16]
            try:
                file.write(int(s, 2).to_bytes(len(s) // 8, byteorder='little'))
            except:
                print(s)
                break
            i+=16
        file.close()


choice=input("1. write to image\n2. read from image\n3. anything else to break\n:")
if choice=="1":
    file_path=input("enter full path to file to be written:")
    image_path=input("enter full path to image you want to write to:")
    binary_to_image(image_path,file_to_binary(file_path))

elif choice=="2":
    file_path=input("enter full file path with extention:")
    image_path=input("enter full path to image:")
    binary_to_file(image_to_binary(image_path),file_path)
    print("data written to file")
else:
    pass