import cv2
import os
import numpy as np
from numpy.linalg import norm as distance

def ref_point(left_source):
    left_handle = cv2.imread(left_source)
    left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
    l_cont = np.array(np.where(left_handle_gary == 255))

    # left_top -> right_top -> right_bottom -> left bottom
    reference_points = np.zeros((4, 2), np.float32)

    diff_s = 0
    for i in l_cont.T:
        # y = x + n maximum
        if i[0]>= diff_s:
            reference_points[3] = i
    diff_s = 0
    diff_b = 10000000
    for i in l_cont.T:
        # y = x + n maximum
        if i[0] + i[1] >= diff_s:
            diff_s = i[0] + i[1]
            reference_points[2] = i
        # y = -x + n minimum
        if i[0] - i[1] <= diff_b:
            diff_b = i[0] - i[1]
            reference_points[1] = i

    reference_points[0] = reference_points[1] + reference_points[3] - reference_points[2]

    # for i in reference_points:
    #     left_handle[int(i[0])][int(i[1])] = [0, 0, 255]
    # cv2.imwrite(f"test.png", left_handle)
    
    for i in reference_points:
        i[0], i[1] = i[1], i[0]

    return reference_points

def length_height(left_source, right_source):
    left_handle = cv2.imread(left_source)
    right_handle = cv2.imread(right_source)
    left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
    right_handle_gray = cv2.cvtColor(right_handle, cv2.COLOR_BGR2GRAY)
    l_cont = np.array(np.where(left_handle_gary == 255))
    r_cont = np.array(np.where(right_handle_gray == 255))

    # left_top -> right_top -> right_bottom -> left bottom
    reference_points = np.zeros((4, 2))

    diff_s = 0
    for i in l_cont.T:
        # y = x + n maximum
        if i[0]>= diff_s:
            reference_points[3] = i
    diff_s = 0
    diff_b = 10000000
    for i in l_cont.T:
        # y = x + n maximum
        if i[0] + i[1] >= diff_s:
            diff_s = i[0] + i[1]
            reference_points[2] = i
        # y = -x + n minimum
        if i[0] - i[1] <= diff_b:
            diff_b = i[0] - i[1]
            reference_points[1] = i
    diff_s = 0
    for i in r_cont.T:
        if i[0]>= diff_s:
            reference_points[0] = i

    for i in reference_points:
        i -= [20, 20]

    length = distance(reference_points[0]-reference_points[3])
    height = distance(reference_points[1]-reference_points[2])*1.2

    dst = np.array([
        [0, 0],
        [length, 0],
        [length, height],
        [0, height]], np.float32)

    return dst

def run_rectification(source):
    left_source = os.path.join(source,'part_contour/left_handle_irregular.png')
    left_image = os.path.join(source,'parts/left_handle_irregular.png')
    right_source = os.path.join(source, 'part_contour/right_handle_irregular.png')
    image = cv2.imread(left_image)

    # get source and destination vertices
    # left_handle_cont and right_handle_cont in rp.side and rp.facadeare are based on
    # the contour we get from chair.py which would be stored in ./part_contour
    # src = rp.facade(left_source, right_source)
    src = ref_point(left_source)
    dst = length_height(left_source, right_source)

    H = cv2.getPerspectiveTransform(src, dst)
    R = np.linalg.inv(H)
    offset = np.full((3, 1),1)
    offset = np.dot(R, offset)
    newimage = np.full((image.shape[0]+int(offset[0]), image.shape[1]+int(offset[1]), 3), 255, np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            newimage[i+int(offset[0])][j+int(offset[1])] = image[i][j]

    border_up_left = np.full((3,1), 1)
    border_lower_right = np.zeros((3,1))
    border_lower_right[0] = image.shape[0]
    border_lower_right[1] = image.shape[1]
    border_up_left = np.dot(H, border_up_left)
    border_lower_right = np.dot(H, border_lower_right)

    # print(border_up_left)
    # print(border_lower_right)
    dst = cv2.warpPerspective(newimage, H, (int(border_lower_right[1]), int(border_lower_right[0])), cv2.INTER_LINEAR)

    final_image = np.full((dst.shape[0], dst.shape[1], 3), 255, np.uint8)
    for i in range(dst.shape[0]):
        for j in range(dst.shape[1]):
            if (dst[i][j] == [230, 2, 10]).all():
                final_image[i][j] = [230, 2, 10]

    cv2.imwrite(os.path.join(source,'parts/Left_handle_irregular_rected.png'), final_image)

# -------- main program -------------------------
if __name__ == "__main__":
    source = 'chairs\\16-1'
    run_rectification(source)