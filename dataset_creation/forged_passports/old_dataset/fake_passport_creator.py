from PIL import Image, ImageFont, ImageDraw

import matplotlib.pyplot as plt
import random
import os
import csv
import json


## set default paths
font_path = "fonts"
background = "background/ita_passport_bg.png"
output_path = "out"

font_styles = os.listdir(font_path)
print(font_styles)
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

written_passports = 0
pos_dict_list = []

for passport_data in csv_reader:
    print(passport_data)

    image = Image.open(background)
    draw = ImageDraw.Draw(image)

    color_facsimile = (255, 0, 0)
    draw.text((10,0), "FACSIMILE    ", color_facsimile, font = font)

    # n randomico caratteri "falsi"
    length_tot = 0
    for i in range(len(passport_data)):
        #print(len(passport_data[i]))
        length_tot += len(passport_data[i])
    print(length_tot)
    # poniamo che ci siano massimo 5 caratteri falsi per passaporto
    # num_false_chars indicates how many wrong characters will show up in the forged passport
    num_false_chars = random.randint(1, 5)
    false_char_indexes = []
    for i in range(0, num_false_chars):
        false_char_indexes.append(random.randint(0, length_tot - 1))
    print(false_char_indexes)

    file_name = "forged_passport_mod_" + str(written_passports) + ".png"
    current_char = 0
    for i in range(len(passport_data)):
        for j in range(len(passport_data[i])):
                if current_char in false_char_indexes:
                    c_fontstyle = font_style # it's here if we want it to dinamically change one day
                    c_fontsize = font_size + random.randint(-2, 2)
                    c_font = ImageFont.truetype(c_fontstyle, c_fontsize)
                    if i == 7:
                        coord_string = (190 + 87 + j * char_width + random.randint(-2,2), 100 + 31 * 4 + random.randint(-2,2))
                    else:
                        coord_string = (190 + j * char_width + random.randint(-2,2), 100 + 31 * i + random.randint(-2,2))
                    #print(coord_string)
                    draw.text(coord_string, passport_data[i][j], color, font = c_font)
                    pos = draw.textbbox(coord_string,  passport_data[i][j], font = c_font) #(left, top, right, bottom) bounding box
                    #draw.rectangle(pos, outline = 'blue')
                    pos_dict_list.append({'path':file_name, 'bbox':pos})
                else:
                    if i == 7:
                        coord_string = (190 + 87 + j * char_width, 100 + 31 * 4)
                    else:
                        coord_string = (190 + j * char_width, 100 + 31 * i)
                    #print(coord_string)
                    draw.text(coord_string, passport_data[i][j], color, font=font)
                current_char += 1

    image.save(os.path.join(output_path, file_name), quality=100)

    written_passports += 1
    with open(os.path.join(output_path, "annotation.json"),"w") as f :
        json.dump(pos_dict_list, f)