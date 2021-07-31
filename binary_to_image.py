from PIL import ImageEnhance
from PIL import Image
import numpy

def bit32Binary(number):
    binaryString = bin(int(number))
    length_of_string = len(binaryString)-1
    string_to_return = ""
    for i in range(0,33-length_of_string):
        string_to_return = string_to_return + "0"
    string_to_return = string_to_return + binaryString[2:len(binaryString)]
    return string_to_return

def binary_to_image(path,binary_string):
    #open image 
    image_to_read = Image.open(path)
    #print(image_to_read.size)
    #image_to_read=image_to_read.resize((10,10))
    #image_to_read.show()
    #find the length of data to be written in pairs of bits
    length_of_string_in_double_bits = len(binary_string)/2
    #convert pixels to 2-D array
    pixel_array = image_to_read.load()
    #calculate max capacity of image
    total_size = image_to_read.size[0]*image_to_read.size[1]*3
    size_of_header = 16
    if total_size < size_of_header+length_of_string_in_double_bits:
        print("->Image size insufficient!!!")
    else:
        print("->Writing data in image......")
        #make binary string to write in image
        Binary_for_header = bit32Binary(length_of_string_in_double_bits)
        Binary_to_write_in_image = Binary_for_header + binary_string
        #create a duplicate image to write in
        image_to_write = Image.new(image_to_read.mode,image_to_read.size)
        image_to_write=image_to_read
        new_pixel_array = image_to_write.load()
        cursorInBinaryString=0
        count=0
        filename = input("Enter file name OR full path for image with data in it(with .png extension):")
        image_to_write.save(filename)
        #print(image_to_write.size[0],image_to_write.size[1])
        terminate=False
        for row in range(image_to_read.size[0]):
            #print("")
            for col in range(image_to_read.size[1]):
                if cursorInBinaryString >= len(Binary_to_write_in_image):
                    new_pixel_array[row,col] = tuple(pixel_array[row,col])
                    #print(new_pixel_array[row,col][0],pixel_array[row,col][1],pixel_array[row,col][2],end="|")
                else:    
                    num1=0
                    num2=0
                    num3=0
                    if cursorInBinaryString+1 < len(Binary_to_write_in_image):
                        num1 = 2*int(Binary_to_write_in_image[cursorInBinaryString])+int(Binary_to_write_in_image[cursorInBinaryString+1])
                        #print(Binary_to_write_in_image[cursorInBinaryString]+Binary_to_write_in_image[cursorInBinaryString+1],end=" ")
                    else:
                        terminate=True
                        num1 = (pixel_array[row,col][0]%4)
                    try:
                        temp_cell1 = pixel_array[row,col][0]-(pixel_array[row,col][0]%4)+int(num1)
                    except:
                        print("Error")
                        terminate=True
                        image_to_write.save(filename)
                        break
                    if temp_cell1 < 256:
                        pass
                    else:
                        temp_cell1 = 252 + num1
                    #print(temp_cell1%4," ",temp_cell1)
                    #-------------------------------------------------------------------------------
                    if cursorInBinaryString+3 < len(Binary_to_write_in_image):
                        num2 = 2*int(Binary_to_write_in_image[cursorInBinaryString+2])+int(Binary_to_write_in_image[cursorInBinaryString+3])
                        #print(Binary_to_write_in_image[cursorInBinaryString+2]+Binary_to_write_in_image[cursorInBinaryString+3],end=" ")
                    else:
                        terminate=True
                        num2 = (pixel_array[row,col][1]%4)
                    temp_cell2 = pixel_array[row,col][1]-(pixel_array[row,col][1]%4)+int(num2)
                    if temp_cell2 < 256:
                        pass
                    else:
                        temp_cell2 = 252 + num2
                    #print(temp_cell2%4," ",temp_cell2)
                    #-------------------------------------------------------------------------------
                    if cursorInBinaryString+5 < len(Binary_to_write_in_image):
                        num3 = 2*int(Binary_to_write_in_image[cursorInBinaryString+4])+int(Binary_to_write_in_image[cursorInBinaryString+5])
                        #print(Binary_to_write_in_image[cursorInBinaryString+4]+Binary_to_write_in_image[cursorInBinaryString+5],end=" ")
                    else:
                        terminate=True
                        num3 = (pixel_array[row,col][2]%4)
                    temp_cell3 = pixel_array[row,col][2]-(pixel_array[row,col][2]%4)+int(num3)
                    if temp_cell3 < 256:
                        pass
                    else:
                        temp_cell3 = 252 + num3
                    #print(temp_cell3%4," ",temp_cell3)
                    #-------------------------------------------------------------------------------
                    #new_pixel_array[col,row] = (temp_cell1,temp_cell2,temp_cell3)
                    try:
                        new_pixel_array[row,col] = (temp_cell1,temp_cell2,temp_cell3)
                        #new_pixel_array[row,col] = (255,0,0)
                        #print(new_pixel_array[row,col][0],pixel_array[row,col][1],pixel_array[row,col][2],end="|")
                    except:
                        print("Error")
                        image_to_write.save(filename)
                        terminate=True
                    #print(pixel_array[row,col],end="")
                cursorInBinaryString += 6
                count+=1
                #print(int(count*100/(total_size/3)),"%\r",end="")
                col += 1
                if terminate: break
            if terminate: break
            row+=1
        #print("")
        #image_to_write.show()
        image_to_write.save(filename)
        print("->Data has been written in Image")
