import numpy as np
import cv2
import os
from sys import exit

def run(file_path):
    image = cv2.imread(f"{file_path}.png")
    height = image.shape[0]
    length = image.shape[1]

    box = {
        "left_handle" : [115, 1, 1],
        "right_handle" : [5, 5, 1],
        "cushion" : [1, 115, 1],
        "back_cushion" : [115, 115, 1],
        "bottom" : [24, 24, 1],
        "lower_bottom" : [5, 115, 1],
        "cylinder_leg" : [1, 1, 24],
        "box_leg": [1, 24, 24]
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
        try:
            os.mkdir(f"{file_path}")
            os.mkdir(f"{file_path}/parts")
            os.mkdir(f"{file_path}/part_contour")
        except:
            pass
        cv2.imwrite(f"{file_path}/parts/{i}.png", image_part[i])
        image = cv2.imread(f"{file_path}/parts/{i}.png")
        edges = cv2.Canny(image,140,150)
        cv2.imwrite(f"{file_path}/part_contour/{i}.png", edges)

if __name__ == "__main__":
    run('chairs\\1-1')