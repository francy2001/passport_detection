from PIL import Image, ImageFont, ImageDraw

import os
import csv

## set default paths
font_path = "fonts"
background = "background/ita_passport_bg.png"
output_path = "out"

## preparing path
font_styles = os.listdir(font_path)
font_style = os.path.join(font_path, font_styles[1])

#loading font
font_size = 12
font = ImageFont.truetype(font_style, font_size)

## color and coordinates definition
color = (0,0,0) #black

data_file = open("data/data.csv", "r", newline='')
csv_reader = csv.reader(data_file)

written_passports = 0

for passport_data in csv_reader:
    print(passport_data)

    image = Image.open(background)
    draw = ImageDraw.Draw(image)

    for i in range(7):
        coord_string = (190, 100 + 31 * i)
        draw.text(coord_string, passport_data[i], color, font=font)

    coord_luogonascita = (190 + 87, 100 + 31 * 4)
    draw.text(coord_luogonascita, passport_data[7], color, font=font)

    file_name = "forged_passport_" + str(written_passports) + ".png"
    image.save(os.path.join(output_path, file_name), quality=100)
    written_passports += 1
