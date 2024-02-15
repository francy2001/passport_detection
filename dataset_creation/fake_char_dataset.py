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
output_path = "dataset"
font_styles = os.listdir(font_path)
data_file = open("data/creation_dataset.csv", "r", newline='')

## preparing path
font_style = os.path.join(font_path, font_styles[2])
sfalsati_path = os.path.join(output_path, "sfalsati") 
sovrapposti_path = os.path.join(output_path, "sovrapposti")

# loading font
font_size = 12
font = ImageFont.truetype(font_style, font_size)
char_width = 7

## color definition
color = (0,0,0) #black

## csv reader definition
csv_reader = csv.reader(data_file)

sovrap_char = 0
sfals_char = 0 
for passport_data in csv_reader:

    sfals_chars = []
    sovrap_chars = [] 
    
    ## image initialization
    image = Image.open(base)
    draw = ImageDraw.Draw(image)

    # counting total chars number
    length_tot = 0
    for i in range(len(passport_data)):
        length_tot += len(passport_data[i])

    num_stagger_char = random.randint(5, 8) # number of staggered characters to insert into the text
    stagger_char_indexes = []
    for i in range(0, num_stagger_char):
        stagger_char_indexes.append(random.randint(0, length_tot - 1))

    current_char = 0    
    for i in range(len(passport_data)):
        for j in range(len(passport_data[i])):

                if current_char in stagger_char_indexes and passport_data[i][j] != ' ':
                    
                    ## font change
                    c_fontstyle = font_style # it's here if we want it to dinamically change one day
                    offset_size = random.randint(-2, 2)
                    while offset_size == 0: # to avoid that there is no offset, therefore that the character is not false
                        offset_size = random.randint(-2, 2)
                    c_fontsize = font_size + offset_size
                    c_font = ImageFont.truetype(c_fontstyle, c_fontsize)

                    ## calculation of coordinates
                    offset_coord_collector = [-3.5,-3.0,-2.8, -2.5, 2.5, 2.8, 3.0, 3.5]
                    offset_coord = offset_coord_collector[random.randint(0,len(offset_coord_collector)-1)]
                    if i == 7: # the x for the seventh element is different (place of birth shifted 87 pixels to the right)
                        coord_string = (190 + 87 + j * char_width + offset_coord, 100 + 31 * 4 + offset_coord)
                    else:
                        coord_string = (190 + j * char_width + offset_coord, 100 + 31 * i + offset_coord)
                
                    ## overlapping characters
                    if (passport_data[i][j] == 'P' or passport_data[i][j] == 'R' or passport_data[i][j] == 'S'):

                        draw.text(coord_string, passport_data[i][j], color, font = c_font)
                        offsets_sovr_char = [-1,1,1.5,-1.5]
                        coord_sovrapp = (coord_string[0] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)], coord_string[1] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)])
                        draw.text(coord_sovrapp, 'B', color, font = c_font)

                        sovrap_chars.append(coord_string)

                    elif (passport_data[i][j] == 'C'):

                        draw.text(coord_string, passport_data[i][j], color, font = c_font)
                        offsets_sovr_char = [-1,1,1.5,-1.5]
                        coord_sovrapp = (coord_string[0] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)], coord_string[1] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)])
                        draw.text(coord_sovrapp, 'D', color, font = c_font)

                        sovrap_chars.append(coord_string)

                    elif (passport_data[i][j] == 'G'):

                        draw.text(coord_string, passport_data[i][j], color, font = c_font)
                        offsets_sovr_char = [-1,1,1.5,-1.5]
                        coord_sovrapp = (coord_string[0] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)], coord_string[1] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)])
                        draw.text(coord_sovrapp, 'O', color, font = c_font)

                        sovrap_chars.append(coord_string)

                    ## staggered characters
                    else:
                        draw.text(coord_string, passport_data[i][j], color, font = c_font)

                        sfals_chars.append(coord_string)

                else:
                    
                    ## calculation of coordinates
                    if i == 7:  # the x for the seventh element is different (place of birth shifted 87 pixels to the right)
                        coord_string = (190 + 87 + j * char_width, 100 + 31 * 4)
                    else:
                        coord_string = (190 + j * char_width, 100 + 31 * i)
                    
                    ## overlapping characters
                    if passport_data[i][j] == 'P' or passport_data[i][j] == 'R' or passport_data[i][j] == 'S' and passport_data[i][j] != ' ':

                        draw.text(coord_string, passport_data[i][j], color, font = font)
                        offsets_sovr_char = [-1,1,1.5,-1.5]
                        coord_sovrapp = (coord_string[0] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)], coord_string[1] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)])
                        draw.text(coord_sovrapp, 'B', color, font = font)
                        
                        sovrap_chars.append(coord_string)
                    
                    elif (passport_data[i][j] == 'C'):
                    
                        draw.text(coord_string, passport_data[i][j], color, font = font)
                        offsets_sovr_char = [-1,1,1.5,-1.5]
                        coord_sovrapp = (coord_string[0] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)], coord_string[1] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)])
                        draw.text(coord_sovrapp, 'D', color, font = font)
                        
                        sovrap_chars.append(coord_string)

                    elif (passport_data[i][j] == 'G'):

                        draw.text(coord_string, passport_data[i][j], color, font = font)
                        offsets_sovr_char = [-1,1,1.5,-1.5]
                        coord_sovrapp = (coord_string[0] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)], coord_string[1] + offsets_sovr_char[random.randint(0, len(offsets_sovr_char)-1)])
                        draw.text(coord_sovrapp, 'O', color, font = font)

                        sovrap_chars.append(coord_string)

                    else:

                        draw.text(coord_string, passport_data[i][j], color, font = font)

                current_char += 1

    ## actual creation of images for the dataset
    for coord in sovrap_chars:
        offset_x = random.randint(2,15)
        offset_y = random.randint(-5,5)
        im_crop = image.crop((coord[0]-offset_x, coord[1]-offset_y, coord[0]-offset_x+32, coord[1]-offset_y+32))
        file_name = "sovr_"+str(sovrap_char)+".png"
        im_crop.save(os.path.join(sovrapposti_path, file_name), quality = 95)
        sovrap_char += 1

    for coord in sfals_chars:
        offset_x = random.randint(2,15)
        offset_y = random.randint(-2,2)
        im_crop = image.crop((coord[0]-offset_x, coord[1]-offset_y, coord[0]-offset_x+32, coord[1]-offset_y+32))
        file_name = "sfals_"+str(sfals_char)+".png"
        im_crop.save(os.path.join(sfalsati_path, file_name), quality = 95)
        sfals_char += 1
