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
sfalsati_path = os.path.join(output_path, "sfalsati") 
sovrapposti_path = os.path.join(output_path, "sovrapposti")
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

sfals_char = 0
sovrap_char = 0  
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

    # num_stagger_char numero di caratteri sfalsati da inserire nel testo --> max 32
    num_stagger_char = random.randint(5, 32)
    stagger_char_indexes = []
    for i in range(0, num_stagger_char):
        stagger_char_indexes.append(random.randint(0, length_tot - 1))
    #print("Indici dei caratteri sfalsati: ", stagger_char_indexes)

    current_char = 0    
    for i in range(len(passport_data)):
        for j in range(len(passport_data[i])):

                if current_char in stagger_char_indexes:
                    
                    # FONT CHANGE
                    c_fontstyle = font_style # it's here if we want it to dinamically change one day
                    c_fontsize = font_size + random.randint(-2, 2)
                    c_font = ImageFont.truetype(c_fontstyle, c_fontsize)

                    # CALCOLO DELLE COORDINATE
                    if i == 7: # la x per il settimo elemento è diversa (Luogo di nascita traslato di 87 pixels a destra)
                        coord_string = (190 + 87 + j * char_width + random.randint(-2,2), 100 + 31 * 4 + random.randint(-2,2))
                    else:
                        coord_string = (190 + j * char_width + random.randint(-2,2), 100 + 31 * i + random.randint(-2,2))
                
                    # Sovrapposti
                    if passport_data[i][j]=='S' or passport_data[i][j]=='P' or passport_data[i][j]=='R':

                        draw.text(coord_string, passport_data[i][j], color, font = c_font)
                        draw.text(coord_string, 'B', color, font = c_font)

                        offset_x = random.randint(2,18)
                        offset_y = random.randint(0,3)
                        im_crop = image.crop((coord_string[0]-offset_x, coord_string[1]-offset_y, coord_string[0]-offset_x+32, coord_string[1]-offset_y+32))
                        file_name = "sovr_char_"+str(sovrap_char)+".png"
                        im_crop.save(os.path.join(sovrapposti_path, file_name), quality = 95)

                        sovrap_char += 1
                    # Sfalsati
                    else:
                        draw.text(coord_string, passport_data[i][j], color, font = c_font)

                        offset_x = random.randint(2,18)
                        offset_y = random.randint(0,3)
                        im_crop = image.crop((coord_string[0]-offset_x, coord_string[1]-offset_y, coord_string[0]-offset_x+32, coord_string[1]-offset_y+32))
                        file_name = "sfals_char_"+str(sfals_char)+".png"
                        im_crop.save(os.path.join(sfalsati_path, file_name), quality = 95)

                        sfals_char += 1
                else:
                    
                    # CALCOLO DELLE COORDINATE
                    if i == 7:  # la x per il settimo elemento è diversa (Luogo di nascita traslato di 87 pixels a destra)
                        coord_string = (190 + 87 + j * char_width, 100 + 31 * 4)
                    else:
                        coord_string = (190 + j * char_width, 100 + 31 * i)
                    
                    # Sovrapposti
                    if passport_data[i][j]=='S' or passport_data[i][j]=='P' or passport_data[i][j]=='R':
                        draw.text(coord_string, passport_data[i][j], color, font = font)
                        draw.text(coord_string, 'B', color, font = font)
                        
                        offset_x = random.randint(2,18)
                        offset_y = random.randint(0,3)
                        im_crop = image.crop((coord_string[0]-offset_x, coord_string[1]-offset_y, coord_string[0]-offset_x+32, coord_string[1]-offset_y+32))
                        file_name = "sovr_char_"+str(sovrap_char)+".png"
                        im_crop.save(os.path.join(sovrapposti_path, file_name), quality = 95)

                        sovrap_char += 1

                    else: # Normale
                        draw.text(coord_string, passport_data[i][j], color, font = font)

                current_char += 1

# In alcune immagini andiamo ad inserire una minima rotazione, per evitare che gli unici passaporti leggibili siano quelli posizionati esattamente frontalmente alla telecamera (caso quasi impossibile...)
rand_sovr_to_rotate = random.randint(0, sovrap_char)
rand_sfals_to_rotate = random.randint(0, sfals_char)

for i in range(rand_sovr_to_rotate):
    
    file_name = "sovr_char_"+str(sovrap_char)+".png"
                                            
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

for i in range(rand_sfals_to_rotate):
    
    file_name = "sfals_char_"+str(sfals_char)+".png"
                                            
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