import sys
import read_file
import random
import string

arguements = list(sys.argv)
arguements=arguements[1:]

if len(arguements)==4:
    file_path=arguements[0]
    key=arguements[1]
    image_path=arguements[2]
    output_image_path=arguements[3]
    if key=='r':
        key=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation) for _ in range(16))
        print("Here's your key please remember it:",key)
        key = read_file.crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
        read_file.hide(file_path,image_path,key,output_image_path)
    elif len(key)==16:
        key=read_file.crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
        read_file.hide(file_path,image_path,key,output_image_path)
    else:
        print("Wrong arguement in key field (arg 2)")
elif len(arguements)==3:
    image_path=arguements[0]
    key=read_file.crypto.expand_key(str(''.join(format(ord(i), '08b') for i in arguements[1])))
    output_file=arguements[2]
    read_file.reveal(output_file,image_path,key)
else:
    print("no such command found")

