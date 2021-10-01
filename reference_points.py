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
    cv2.imwrite("test.png", image)

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
            
    # image = cv2.imread("./chairs/56-1.png")
    # for i in reference_points:
    #     image[int(i[0])-20][int(i[1])-20] = [0, 0, 255]
    # cv2.imwrite("test.png", image)

    # x and y are swapped b/c of opencv axis type => horizontal->x vertical ->y
    for i in reference_points:
        i[0], i[1] = i[1], i[0]

    return (int(distance(reference_points[0]-reference_points[1]))+int(distance(reference_points[1]-reference_points[2])))/int(distance(reference_points[0]-reference_points[1]))

if __name__== "__main__":
    left_source = './chairs/9-1/part_contour/left_handle.png'
    right_source = './chairs/9-1/part_contour/right_handle.png'
    print(whole_length_and_whole_height(left_source, right_source))
    print(left_right_length_ratio(left_source, right_source))