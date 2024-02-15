from PIL import Image, ImageFont, ImageDraw, ImageFilter

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import random
import os
import csv
import json
import cv2
import numpy as np
import pathlib
from PIL import Image
from itertools import product

## set default paths
font_path = "fonts"
font_styles = os.listdir(font_path)
base = "ita_passport_bg.png"
output_path = "dataset/background"

name, ext = os.path.splitext(base)
img = Image.open(base)
draw = ImageDraw.Draw(img)
color_facsimile = (255, 0, 0)
font_style = os.path.join(font_path, font_styles[2])
font_size = 12
font = ImageFont.truetype(font_style, font_size)

w, h = img.size
d = 32

frame = 0
grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
for i, j in grid:
    box = (j, i, j+d, i+d)
    file_name = 'background_'+str(frame)+'.png'
    out = os.path.join(output_path, file_name)
    img.crop(box).save(out)
    frame += 1

# In alcune immagini andiamo ad inserire una minima rotazione, per evitare che gli unici passaporti leggibili siano quelli posizionati esattamente frontalmente alla telecamera (caso quasi impossibile...)
output_dir = pathlib.Path(output_path)
num = len(list(output_dir.glob('*.png')))
for i in range(3):
    for j in range(num):

        file_name = "rounded_char_"+str(j+i*num)+".png"
        old_file_name = "background_"+str(j)+".png"
        image = cv2.imread(os.path.join(output_path, old_file_name), cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        
        angle = random.randint(-5,5)
        print("Angolo di rotazione: ", angle)

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
