import os
import cv2
import numpy as np
from numpy.linalg import norm as distance

def whole_length_and_whole_height(left_source, right_source):
    left_handle = cv2.imread(left_source)
    right_handle = cv2.imread(right_source)
    left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
    right_handle_gray = cv2.cvtColor(right_handle, cv2.COLOR_BGR2GRAY)
    l_cont = np.array(np.where(left_handle_gary == 255))
    r_cont = np.array(np.where(right_handle_gray == 255))

    # right_top -> left_top -> left_bottom -> right_bottom
    reference_points = np.zeros((4, 2))

    diff_s = 0
    diff_b = 10000000
    for i in r_cont.T:
        # y = x + n maximum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            reference_points[3] = i
        # y = -x + n minimum
        if i[0] + i[1] <= diff_b:
            diff_b = i[0] + i[1]
            reference_points[0] = i
    diff_s = 0
    diff_b = 10000000
    for i in l_cont.T:
        # y = -x + n minimum
        if 2*i[0] + i[1] <= diff_b:
            diff_b = 2*i[0] + i[1]
            reference_points[1] = i
        # y = x + n maximum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            reference_points[2] = i
    
    image = cv2.imread(left_source)
    for i in reference_points:
        image[int(i[0])][int(i[1])] = [0, 0, 255]
    image[int(i[0])][int(i[1])] = [0, 0, 255]
    # cv2.imwrite("test.png", image)

    # x and y are swapped b/c of opencv axis type => horizontal->x vertical ->y
    for i in reference_points:
        i[0], i[1] = i[1], i[0]

    return int(distance(reference_points[2]-reference_points[3])), int(distance(reference_points[1]-reference_points[2]))

def left_right_length_ratio(left_source, right_source):
    left_handle = cv2.imread(left_source)
    right_handle = cv2.imread(right_source)
    left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
    right_handle_gray = cv2.cvtColor(right_handle, cv2.COLOR_BGR2GRAY)
    l_cont = np.array(np.where(left_handle_gary == 255))
    r_cont = np.array(np.where(right_handle_gray == 255))

    #right(handle)_bottom -> mid(handle)_bottom -> left(handle)_bottom
    reference_points = np.zeros((3, 2))

    diff_s = 0
    for i in r_cont.T:
        # y = x + n maximum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            reference_points[0] = i

    diff_s1 = 0
    diff_s2 = 0
    for i in l_cont.T:
        # y = x + n maximum
        if i[0] - i[1] >= diff_s1:
            diff_s1 = i[0] - i[1]
            reference_points[1] = i
        if i[0] + i[1] >= diff_s2:
            diff_s2 = i[0] + i[1]
            reference_points[2] = i

    # x and y are swapped b/c of opencv axis type => horizontal->x vertical ->y
    for i in reference_points:
        i[0], i[1] = i[1], i[0]

    return (int(distance(reference_points[0]-reference_points[1]))+int(distance(reference_points[1]-reference_points[2])))/int(distance(reference_points[0]-reference_points[1]))

def whole_length_and_whole_height_without_handles(Cushion_source):
    cushion = cv2.imread(Cushion_source)
    cushion_gary = cv2.cvtColor(cushion, cv2.COLOR_BGR2GRAY)
    c_cont = np.array(np.where(cushion_gary == 255))

    # right_bottom -> right_top -> left_top -> left_bottom
    reference_points = np.zeros((4, 2))

    diff_s = 0
    diff_b = 10000000
    for i in c_cont.T:
        # y = x + n maximum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            reference_points[0] = i
        # y = -x + n minimum
        if i[0] + i[1] <= diff_b:
            diff_b = i[0] + i[1]
            reference_points[1] = i
    diff_s = 0
    diff_b = 10000000
    for i in c_cont.T:
        # y = -x + n minimum
        if i[0] - i[1] <= diff_b:
            diff_b = i[0] - i[1]
            reference_points[2] = i
        # y = x + n maximum
        if i[0] + i[1] >= diff_s:
            diff_s = i[0] + i[1]
            reference_points[3] = i
    
    height1 = distance(reference_points[0] - reference_points[1])
    height2 = distance(reference_points[2] - reference_points[3])
    length1 = distance(reference_points[0] - reference_points[3])
    length2 = distance(reference_points[1] - reference_points[2])
    if height1 > height2:
        height = height1
    else:
        height = height2
    if length1 > length2:
        length = length1
    else:
        length = length2

    return length, height

def whole_lwh(Left_source, Right_source):
    length, height = whole_length_and_whole_height(Left_source, Right_source)
    left_right_ratio = left_right_length_ratio(Left_source, Right_source)
    return length, length, height, left_right_ratio

def whole_lwh_without_handles(Cushion_source):
    length, height = whole_length_and_whole_height_without_handles(Cushion_source)
    return length, length, height, 1.5

def get_parameter(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contour = np.array(np.where(gray == 255))
    # right_top -> right_bottom -> left bottom
    reference_points = np.zeros((3, 2), dtype=np.int32)
    diff_s = -10000000
    diff_b = 10000000
    reference_points[2][1] = 10000000
    for i in contour.T:
        # y = -x + n minimum
        if i[0] + 2*i[1] <= diff_b:
            diff_b = i[0]+2*i[1]
            reference_points[0] = i
        # y = n maximum
        if 9*i[0] + i[1] >= diff_s:
            diff_s = 9*i[0]+i[1]
            reference_points[1] = i
    diff_b = -10000000
    for i in contour.T:
        if i[0]-i[1] >= diff_b:
            diff_b = i[0]-i[1]
            reference_points[2] = i
    reference_points[0] += reference_points[1]-reference_points[2]
    height = distance(reference_points[0]-reference_points[1])
    length = np.float64(reference_points[1][1]-reference_points[2][1])

    return length, length, height

def cushion_height(right_path, cushion_path, whole_height, lower_bottom_height, bottom_height):
    right_height = 1000000
    cushion_height = 1000000
    if os.path.isfile(right_path):
        right_image = cv2.imread(right_path)
        right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)
    cushion_image = cv2.imread(cushion_path)
    cushion_image = cv2.cvtColor(cushion_image, cv2.COLOR_BGR2GRAY)
    for i in np.array(np.where(right_image == 255)).T:
        if i[0] < right_height:
            right_height = i[0]
    for i in np.array(np.where(cushion_image == 255)).T:
        if i[0] < cushion_height:
            cushion_height = i[0]
          #(whole_height-lower_bottom_height-bottom_height) - (cushion_height - left_height) - (left_height-right_height)
    return (whole_height-lower_bottom_height-bottom_height) - cushion_height + right_height


if __name__== "__main__":
    left_source = './chairs/9-1/part_contour/left_handle.png'
    right_source = './chairs/9-1/part_contour/right_handle.png'
    print(whole_length_and_whole_height(left_source, right_source))
    print(left_right_length_ratio(left_source, right_source))