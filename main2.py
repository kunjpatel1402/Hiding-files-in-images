import sys
import read_file
import random
import string
'''
key should be exactly 16 characters long
format for hiding files - main2.py <file to hide> <key/r for random key generation> <image you want to hide file in> <ouput image with file hidden in it>
format to recover file - main2.py <image with file in it> <key> <ouput file with same extension as file hidden in image>
'''
arguements = list(sys.argv)
arguements=arguements[1:]

if len(arguements)==4:
    file_path=arguements[0]
    key=arguements[1]
    image_path=arguements[2]
    output_image_path=arguements[3]
    if key=='r':
        key=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
        print("Here's your key please remember it:",key)
        key = read_file.crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
        read_file.hide(file_path,image_path,key,output_image_path)
    elif len(key)==16:
        key=read_file.crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
        read_file.hide(file_path,image_path,key,output_image_path)
    else:
        print("Wrong arguement in key field (arg 2)")
elif len(arguements)==3:
    if (len(arguements[1])==16):
        image_path=arguements[0]
        #print(len(arguements[1]))
        key=read_file.crypto.expand_key(str(''.join(format(ord(arguements[1][i]), '08b') for i in range(0,16))))
        #print(key)
        output_file=arguements[2]
        read_file.reveal(output_file,image_path,key)
    else:
        print("Key should be 16 characters long")
else:
    print("no such command found")

