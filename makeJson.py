import cv2
import json
import reference_points as rp
import numpy as np
from numpy.linalg import norm as distance
from sys import exit

def whole_lwh(Left_source, Right_source):
    length, height = rp.length_height(Left_source, Right_source)
    return length, length, height

def get_len(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contour = np.array(np.where(gray == 255))
    # right_top -> right_bottom -> left bottom
    reference_points = np.zeros((3, 2), dtype=np.int32)
    diff_s = 0
    diff_b = 10000000
    for i in contour.T:
        # y = n maximum
        if 3*i[0] + i[1] >= diff_s:
            diff_s = 3*i[0]+i[1]
            reference_points[1] = i
        # y = -x + n minimum
        if i[0] + i[1] <= diff_b:
            diff_b = i[0]+i[1]
            reference_points[0] = i
    diff_s = 0
    for i in contour.T:
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            temp_point = i
    reference_points[0] += reference_points[1]-temp_point
    diff_s = 0
    diff_b = 10000000
    for i in contour.T:
        # y = x + n maximum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            reference_points[2] = i
    for i in reference_points:
        image[i[0]][i[1]] = [0, 0, 255]
    # cv2.imwrite(f"test{cnt}.png", image)
    height = distance(reference_points[0]-reference_points[1])
    length = distance(reference_points[1]-reference_points[2])
    width = rp.width(Left_source, Right_source)

    return length, width, height

def leg_offset(Left_handle, Leg):
    handle = cv2.imread(Left_handle)
    gray_handle = cv2.cvtColor(handle, cv2.COLOR_BGR2GRAY)
    handle_contour = np.array(np.where(gray_handle == 255))

    leg = cv2.imread(Leg)
    gray_leg = cv2.cvtColor(leg, cv2.COLOR_BGR2GRAY)
    leg_contour = np.array(np.where(gray_leg == 255))
    reference_points = np.zeros((2, 2), dtype=np.int32)

    diff_s = 0
    for i in leg_contour.T:
        # y = -x + n minimum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0]+i[1]
            reference_points[0] = i
    diff_s = 0
    for i in handle_contour.T:
        # y = -0.5x + n maximum
        if 0.51*i[0] + i[1] >= diff_s:
            diff_s = 0.5*i[0]+i[1]
            reference_points[1] = i

    return distance(reference_points[0]-reference_points[1])

def construct(part, ref_x, ref_y, ref_z, length, width, height):
    parts_obj = {}
    parts_obj[part] = {"type":"Box", "parameter":{"reference_point":[ref_x, ref_y, ref_z], "l_w_h":[length, width, height]}}
    return parts_obj

def create_handle(path, whole_length , whole_width, whole_height):
    length, width , height = get_len(path)
    left_obj = construct("left_handle", whole_length/2, 0, 0, length, width, height)
    right_obj = construct("right_handle", -whole_length/2, 0, 0, length, width, height)
    return length, left_obj, right_obj

def create_lower_bottom(path, whole_length , whole_width, whole_height, left_length):
    length, width , height = get_len(path)
    obj = construct("lower_bottom", 0, 0, -(whole_height-height)/2, whole_length-left_length, width, height)
    return obj, height

def create_bottom(path, whole_length , whole_width, whole_height, left_length, lower_bottom_height):
    length, width , height = get_len(path)
    obj = construct("bottom", 0, 0, -(whole_height-height)/2+lower_bottom_height, whole_length-left_length, width, height)
    return obj, height

def create_cushion(path, whole_length , whole_width, whole_height, left_length, bottom_height, lower_bottom_height):
    length, width , height = get_len(path)
    obj = construct("Cushion", 0, (whole_width-left_length)/2, -(whole_height-height)/2+bottom_height+lower_bottom_height, whole_length-left_length, left_length, height)
    return obj

def create_legs(path, whole_length , whole_width, whole_height):
    length, width , height = get_len(path)
    offset = leg_offset(Left_source, Leg_source)
    obj1 = construct("leg1", whole_length/2, whole_width/2-offset, -(whole_height+height)/2, length, length, height)
    obj2 = construct("leg2", -(whole_length/2), whole_width/2-offset, -(whole_height+height)/2, length, length, height)
    obj3 = construct("leg3", whole_length/2, -(whole_width/2-offset), -(whole_height+height)/2, length, length, height)
    obj4 = construct("leg4", -(whole_length/2), -(whole_width/2-offset), -(whole_height+height)/2, length, length, height)
    return obj1, obj2, obj3, obj4

chair = '32-1'
Left_source = f'./{chair}/part_contour/left_handle.png'
Right_source = f'./{chair}/part_contour/right_handle.png'
Bottom_source = f'./{chair}/part_contour/bottom.png'
Lower_bottom_source = f'./{chair}/part_contour/lower_bottom.png'
Cushion_source = f'./{chair}/part_contour/cushion.png'
Leg_source = f'./{chair}/part_contour/sample_leg.png'
lower_bottom_height = 0
parts_obj = {}
whole_length , whole_width, whole_height = whole_lwh(Left_source, Right_source)
left_handle_length, left_obj, right_obj= create_handle(Left_source, whole_length , whole_width, whole_height)
parts_obj["left_handle"] = left_obj["left_handle"]
parts_obj["right_handle"] = right_obj["right_handle"]

# obj, lower_bottom_height = create_lower_bottom(Bottom_source, whole_length , whole_width, whole_height, left_handle_length)
# parts_obj["lower_bottom"] = obj["lower_bottom"]

obj, bottom_height = create_bottom(Bottom_source, whole_length , whole_width, whole_height, left_handle_length, lower_bottom_height)
parts_obj["bottom"] = obj["bottom"]

obj = create_cushion(Cushion_source, whole_length , whole_width, whole_height, left_handle_length, bottom_height, lower_bottom_height)
parts_obj["Cushion"] = obj["Cushion"]

obj1, obj2, obj3, obj4 = create_legs(Leg_source, whole_length , whole_width, whole_height)
parts_obj["leg1"] = obj1["leg1"]
parts_obj["leg2"] = obj2["leg2"]
parts_obj["leg3"] = obj3["leg3"]
parts_obj["leg4"] = obj4["leg4"]

with open(f'{chair}/{chair}.json', 'w', encoding='utf-8') as f:
    json.dump(parts_obj, f, ensure_ascii=False, indent=4)