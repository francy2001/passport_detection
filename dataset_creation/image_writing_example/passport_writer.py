from PIL import Image, ImageFont, ImageDraw

import random
import os
import csv

## set default paths
font_path = "fonts"
background = "background/ita_passport_bg.png"
output_path = "out"

font_styles = os.listdir(font_path)
data_file = open("data/data.csv", "r", newline='')

def print_docs(font_styles, background, data_file):
    ## preparing path
    font_style = os.path.join(font_path, font_styles[1])

    #loading font
    font_size = 12
    font = ImageFont.truetype(font_style, font_size)

    ## color and coordinates definition
    color = (0,0,0) #black

    csv_reader = csv.reader(data_file)

    written_passports = 0

    for passport_data in csv_reader:
        print(passport_data)

        image = Image.open(background)
        draw = ImageDraw.Draw(image)

        for i in range(7):
            # def random caracter to change
            rnd_position = random.randint(0,7)
            c_fontstyle = font_style
            c_fontsize = font_size + random.randint(-2,2)
            c_font = ImageFont.truetype(c_fontstyle, c_fontsize)
            # substitution of the new character in the string
            data1 = passport_data[i].split(passport_data[i][rnd_position])[0]
            data2 = passport_data[i].split(passport_data[i][rnd_position])[1]
            coord_string = (190, 100 + 31 * i)
            draw.text(coord_string, data1, color, font=font)
            coord_string = (190+len(data1), 100 + 31 * i)
            draw.text(coord_string, passport_data[i][rnd_position], color, font=font)
            coord_string = (190+1+len(data1), 100 + 31 * i)
            draw.text(coord_string, data2, color, font=font)

        coord_luogonascita = (190 + 87, 100 + 31 * 4)
        draw.text(coord_luogonascita, passport_data[7], color, font=font)

        file_name = "forged_passport_" + str(written_passports) + ".png"
        image.save(os.path.join(output_path, file_name), quality=100)
        written_passports += 1

print_docs(font_styles, background, data_file)
