import numpy as np
import cv2
import os
from sys import exit

file_path = "1-1.png"
image = cv2.imread(file_path)
height = image.shape[0]
length = image.shape[1]

left_handle = [115, 1, 1]
right_handle = [5, 5, 1]
cushion = [1, 115, 1]
bottom = [24, 24, 1]
lower_bottom = [5, 115, 1]
box = {
    "left_handle" : [115, 1, 1],
    "right_handle" : [5, 5, 1],
    "cushion" : [1, 115, 1],
    "bottom" : [24, 24, 1],
    "lower_bottom" : [5, 115, 1],
    "sample_leg" : [1, 1, 24]
    }
box_exist = []
for key, ele in box.items():
    if np.argwhere((image == ele).all(axis=2)).size!=0:
        box_exist.append(key)
image_part = {}
for i in box_exist:
    image_part[i] = np.full((height+40, length+40, 3), 255)
for i in range(height):
    for j in range(length):
        if (image[i][j] == [255, 255, 255]).all():
            continue
        else:
            for k in box_exist:
                if (image[i][j] == box[k]).all():
                    image_part[k][i+20][j+20] = image[i][j]
for i in box_exist:
    front = os.path.splitext(file_path)[0]
    try:
        os.mkdir(f"{front}")
        os.mkdir(f"{front}/parts")
        os.mkdir(f"{front}/part_contour")
    except:
        pass
    cv2.imwrite(f"{front}/parts/{i}.png", image_part[i])
    image = cv2.imread(f"{front}/parts/{i}.png")
    edges = cv2.Canny(image,140,150)
    cv2.imwrite(f"{front}/part_contour/{i}.png", edges)