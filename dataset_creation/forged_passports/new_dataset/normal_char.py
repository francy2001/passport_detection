from PIL import Image, ImageFont, ImageDraw, ImageFilter

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import random
import os
import csv
import json
import cv2
import numpy as np

## set default paths
font_path = "fonts"
base = "ita_passport_bg.png"
output_path = "out"
normal_path = os.path.join(output_path, "normali") 
font_styles = os.listdir(font_path)
#print(font_styles)
data_file = open("data/data.csv", "r", newline='')

## preparing path
font_style = os.path.join(font_path, font_styles[2])

#loading font
font_size = 12
font = ImageFont.truetype(font_style, font_size)
char_width = 7

## color and coordinates definition
color = (0,0,0) #black

csv_reader = csv.reader(data_file)

real_char = 0

for passport_data in csv_reader:
    #print("Passport Data: ", passport_data)

    image = Image.open(base)

    draw = ImageDraw.Draw(image)

    color_facsimile = (255, 0, 0)
    draw.text((10,0), "FACSIMILE    ", color_facsimile, font = font)

    # numero totale di caratteri di passport data
    length_tot = 0
    for i in range(len(passport_data)):
        length_tot += len(passport_data[i])
    #print("Numero di caratteri totali: ", length_tot)

    current_char = 0    
    for i in range(len(passport_data)):
        for j in range(len(passport_data[i])):
                
            # CALCOLO DELLE COORDINATE
            if i == 7:  # la x per il settimo elemento è diversa (Luogo di nascita traslato di 87 pixels a destra)
                coord_string = (190 + 87 + j * char_width, 100 + 31 * 4)
            else:
                coord_string = (190 + j * char_width, 100 + 31 * i)

            draw.text(coord_string, passport_data[i][j], color, font = font)
            if current_char%10 == 0:
                offset_x = random.randint(0,28)
                offset_y = random.randint(0,char_width)
                im_crop = image.crop((coord_string[0]-offset_x, coord_string[1]-offset_y, coord_string[0]-offset_x+32, coord_string[1]-offset_y+32))
                file_name = "real_char_"+str(real_char)+".png"
                im_crop.save(os.path.join(normal_path, file_name), quality = 95)
                real_char += 1

            current_char += 1

# In alcune immagini andiamo ad inserire una minima rotazione, per evitare che gli unici passaporti leggibili siano quelli posizionati esattamente frontalmente alla telecamera (caso quasi impossibile...)
rand_norm_to_rotate = random.randint(0, real_char)

for i in range(rand_norm_to_rotate):
    
    file_name = "real_char_"+str(real_char)+".png"
                                            
    image = cv2.imread(os.path.join(output_path, file_name), cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    
    angle = random.randint(1,5)
    #print("Angolo di rotazione: ", angle)

    # grab the dimensions of the image and then determine the centre
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    image = cv2.warpAffine(image, M, (nW, nH))
        
    cv2.imwrite(os.path.join(output_path, file_name), image)