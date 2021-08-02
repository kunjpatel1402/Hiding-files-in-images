import read_file
import random
import string


choice=input("1. write to image\n2. read from image\n3. anything else to break\n:")
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
    key = read_file.crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
    read_file.hide(file_path,image_path,key)
elif choice=="2":
    file_path=input("enter full file path with extention:")
    image_path=input("enter full path to image:")
    key=input("Enter key:")
    key = read_file.crypto.expand_key(str(''.join(format(ord(i), '08b') for i in key)))
    read_file.reveal(file_path,image_path,key)
else:
    pass