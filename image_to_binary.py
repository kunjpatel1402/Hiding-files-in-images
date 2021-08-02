
from PIL import ImageEnhance
from PIL import Image
import numpy


def decide(num):
    if num==0:
        return "00"
    elif num==1:
        return "01"
    elif num==2:
        return "10"
    else:
        return "11"


def binaryToDecimal(n):
    return int(n,2)

def image_to_binary(path):
    #open image

    s=""
    s2=""
    image_to_read = Image.open(path)
    pixel_array = image_to_read.load()
    #print(pixel_array.size)
    #print(pixel_array.size)
    print("->Extracting data from image....")
    row1=0
    count=0
    lim=0
    terminate=False
    for r in range(0,image_to_read.size[0]):
        col1=0
        #print("")
        for c in range(0,image_to_read.size[1]):
            row=r
            col=c
            num1=0
            if row==0 and col<5:
                #print(pixel_array[row,col][0],pixel_array[row,col][1],pixel_array[row,col][2],end="|")
                for i in range(0,3):
                    num1 = (pixel_array[row, col][i] % 4)
                    s = s + decide(num1)
            
            elif row==0 and col==5:
                #print(pixel_array[row,col][0],pixel_array[row,col][1],pixel_array[row,col][2],end="|")
                num1 = (pixel_array[row, col][0] % 4)
                s = s + decide(num1)
                lim = binaryToDecimal(s)
                count = 0
                if count<=lim:
                    num2 = (pixel_array[row, col][1] % 4)
                    s2 = s2 + decide(num2)
                    count+=1
                if count<=lim:
                    num3 = (pixel_array[row, col][2] % 4)
                    s2 = s2 + decide(num3)
                    count+=1
            else:
                #print(pixel_array[row,col][0],pixel_array[row,col][1],pixel_array[row,col][2],end="|")
                for i in range(0,3):
                    if count>lim:
                        terminate=True
                        break
                    num1 = (pixel_array[row, col][i] % 4)
                    s2 = s2 + decide(num1)
                    count+=1
            if terminate: break
        if terminate: break
    return s2[0:-2]
