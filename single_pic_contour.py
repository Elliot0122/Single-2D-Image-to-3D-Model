import os
import cv2
import numpy as np
from numpy.linalg import norm as distance
from sys import exit

def order_sorting(image):
    contour = np.array(np.where(image == 255)).T
    right_order = []
    ref_point = [0, 0, 0]
    while(contour.size != 0):
        ref_distance = 100000000000
        del_order = 0
        for i in range(contour.shape[0]):
            temp_distance = distance(contour[i]-ref_point[:-1])
            if temp_distance < ref_distance:
                ref_distance = temp_distance
                del_order = i
        ref_point[:-1] = contour[del_order]
        if ref_distance < 10:
            right_order.append([0, contour[del_order][1], -contour[del_order][0]])
        contour = np.delete(contour, del_order, 0)
    right_order.append(right_order[0])
    return right_order


def left_bottom_point_of_irregular_handle(final_contour):
    point = np.zeros((3))
    sum = 0
    for i in final_contour:
        temp_sum = i[0]+i[1]-i[2]
        if temp_sum > sum:
            sum = temp_sum
            point = i
    return point

def run_contour(file_path):
    path = "parts/Left_handle_irregular_rected.png"
    image = cv2.imread(os.path.join(file_path, path))
    blank = cv2.Canny(image,140,150)
    for i in range(blank.shape[0]-2):
        for j in range(blank.shape[1]-2):
            if blank[i][j] == 255:
                blank[i][j+1] = 0
                blank[i][j+2] = 0
                blank[i+1][j-1] = 0
                blank[i+1][j] = 0
                blank[i+1][j+1] = 0
                blank[i+1][j+2] = 0
                blank[i+2][j-1] = 0
                blank[i+2][j-1] = 0
                blank[i+2][j] = 0
                blank[i+2][j+1] = 0
                blank[i+2][j+2] = 0
    # cv2.imwrite(f"test.png", blank)
    final_contour = order_sorting(blank)
    # with open(os.path.join(file_path, "Left_handle_irregular.txt"), "w") as f:
    #     for i in final_contour:
    #         f.write(f'{i[0]} {i[1]}\n')
    return final_contour

if __name__ == "__main__":
    cont = run_contour('chairs\\35-1')
