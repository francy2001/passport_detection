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
data_file = open("data/data.csv", "r", newline='')

## preparing path
normal_path = os.path.join(output_path, "normali") 
font_styles = os.listdir(font_path)
font_style = os.path.join(font_path, font_styles[2])

# loading font
font_size = 12
font = ImageFont.truetype(font_style, font_size)
char_width = 7

## color coordinates definition
color = (0,0,0) #black

## csv reader definition
csv_reader = csv.reader(data_file)

real_char = 0
for passport_data in csv_reader:

    real_chars = []

    ## image initialization
    image = Image.open(base)
    draw = ImageDraw.Draw(image)

    # counting total chars number
    length_tot = 0
    for i in range(len(passport_data)):
        length_tot += len(passport_data[i])
    
    current_char = 0    
    for i in range(len(passport_data)):
        for j in range(len(passport_data[i])):
                
            ## calculation of coordinates
            if i == 7:  # the x for the seventh element is different (place of birth shifted 87 pixels to the right)
                coord_string = (190 + 87 + j * char_width, 100 + 31 * 4)
            else:
                coord_string = (190 + j * char_width, 100 + 31 * i)

            draw.text(coord_string, passport_data[i][j], color, font = font)
            real_chars.append(coord_string)
            
            current_char += 1

    ## actual creation of images for the dataset
    for coord in real_chars:
        if real_char%10 == 0:
            offset_x = random.randint(2,15)
            offset_y = random.randint(-8,4)
            im_crop = image.crop((coord[0]-offset_x, coord[1]-offset_y, coord[0]-offset_x+32, coord[1]-offset_y+32))
            file_name = "real_"+str(real_char)+".png"
            im_crop.save(os.path.join(normal_path, file_name), quality = 95)
        real_char += 1

