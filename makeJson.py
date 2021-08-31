import cv2
import json
import os
import reference_points as rp
import numpy as np
from numpy.linalg import norm as distance
from sys import exit
from rectification import run_rectification
from single_pic_contour import run_contour, left_bottom

def whole_lwh(Left_source, Right_source):
    length, height = rp.length_height(Left_source, Right_source)
    height_ratio = rp.front_back_height_ratio(Left_source)
    
    return length, length, height, height_ratio

def get_parameter(path):
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
    temp_point = [0, 0]
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
    # for i in reference_points:
    #     image[i[0]][i[1]] = [0, 0, 255]
    # cv2.imwrite(f"test{cnt}.png", image)
    height = distance(reference_points[0]-reference_points[1])
    length = distance(reference_points[1]-reference_points[2])

    return length, length, height

def cushion_offset(cushion_path, back_cushion_path):
    cushion = cv2.imread(cushion_path)
    back_cushion = cv2.imread(back_cushion_path)
    cushion_height = 0
    back_cushion_height = 0
    for i in range(cushion.shape[0]):
        for j in range(cushion.shape[1]):
            if (cushion[i][j] == [255, 255, 255]).all():
                cushion_height = i
                break
        if cushion_height != 0:
            break
    for i in range(back_cushion.shape[0]):
        for j in range(back_cushion.shape[1]):
            if (back_cushion[i][j] == [255, 255, 255]).all():
                back_cushion_height = i
                break
        if back_cushion_height != 0:
            break

    return back_cushion_height - cushion_height

def construct_box(part, ref_x, ref_y, ref_z, length, width, height):
    obj = {}
    obj[part] = {"type":"Box", "parameter":{"reference_point":[ref_x, ref_y, ref_z], "l_w_h":[length, width, height]}}
    
    return obj

def construct_cylinder(part, ref_x, ref_y, ref_z, length, width, height):
    obj = {}
    obj[part] = {"type":"Cylinder", "parameter":{"reference_point":[ref_x, ref_y, ref_z], "height":height, "radius": length/2, "cap": True}}
    
    return obj

def create_handle(path, whole_length , whole_width, whole_height):
    length, width , height = get_parameter(path)
    left_obj = construct_box("left_handle", whole_length/2, 0, 0, length, whole_width, height)
    right_obj = construct_box("right_handle", -whole_length/2, 0, 0, length, whole_width, height)
    
    return length, left_obj, right_obj

def create_lower_bottom(path, whole_length , whole_width, whole_height, left_length):
    length, width , height = get_parameter(path)
    obj = construct_box("lower_bottom", 0, 0, -(whole_height-height)/2, whole_length-left_length, whole_width, height)
    
    return obj, height

def create_bottom(path, whole_length , whole_width, whole_height, left_length, lower_bottom_height):
    length, width , height = get_parameter(path)
    obj = construct_box("bottom", 0, 0, -(whole_height-height)/2+lower_bottom_height, whole_length-left_length, whole_width, height)
    
    return obj, height

def create_back_cushion(path, whole_length , whole_width, whole_height, height_ratio, left_length, offset):
    obj = construct_box("back_cushion", 0, (whole_width-left_length)/2, offset/2, whole_length-left_length, left_length, whole_height+offset)
    
    return obj, left_length

def create_cushion(path, whole_length , whole_width, whole_height, height_ratio, left_length, bottom_height, lower_bottom_height, back_cushion_offset):
    length, width , height = get_parameter(path)
    obj = construct_box("cushion", 0, (whole_width-left_length)/2-back_cushion_offset, -(whole_height-height)/2+bottom_height+lower_bottom_height, whole_length-left_length, left_length, height*height_ratio)
    
    return obj

def create_box_legs(path, whole_length , whole_width, whole_height):
    length, width , height = get_parameter(path)
    obj1 = construct_box("leg1", whole_length/2, whole_length/2-length, -(whole_height+height)/2, length, length, height)
    obj2 = construct_box("leg2", -whole_length/2, whole_length/2-length, -(whole_height+height)/2, length, length, height)
    obj3 = construct_box("leg3", whole_length/2, -whole_length/2+length, -(whole_height+height)/2, length, length, height)
    obj4 = construct_box("leg4", -whole_length/2, -whole_length/2+length, -(whole_height+height)/2, length, length, height)
    
    return obj1, obj2, obj3, obj4

def create_cylinder_legs(path, whole_length , whole_width, whole_height):
    length, width , height = get_parameter(path)
    obj1 = construct_cylinder("leg1", whole_length/2, whole_length/2-length, -whole_height/2-height, length, length, height)
    obj2 = construct_cylinder("leg2", -whole_length/2, whole_length/2-length, -whole_height/2-height, length, length, height)
    obj3 = construct_cylinder("leg3", whole_length/2, -whole_length/2+length, -whole_height/2-height, length, length, height)
    obj4 = construct_cylinder("leg4", -whole_length/2, -whole_length/2+length, -whole_height/2-height, length, length, height)
    
    return obj1, obj2, obj3, obj4

def create_irregular_handles(path, whole_length, whole_width, whole_height, left_length):
    obj = {}
    run_rectification(path)
    contour_points = run_contour(path)
    lebo = left_bottom(contour_points)
    left_points = []
    right_points = []
    for i in contour_points:
        temp = []
        temp.append(i[0] + whole_length/2)
        temp.append(i[1] - lebo[1] + whole_width/2)
        temp.append(i[2] - lebo[2] - whole_height/2)
        left_points.append(temp)
    for i in contour_points:
        temp = []
        temp.append(i[0] - whole_length/2)
        temp.append(i[1] - lebo[1] + whole_width/2)
        temp.append(i[2] - lebo[2] - whole_height/2)
        right_points.append(temp)
    obj["left_handle_irregular"] = {"type":"Plane_extrue", "parameter":{"points":left_points, "thickness":-left_length}}
    obj["right_handle_irregular"] = {"type":"Plane_extrue", "parameter":{"points":right_points, "thickness":+left_length}}
    return obj

def run(file_path):
    irregular_flag = False
    Left_source = f'./{file_path}/part_contour/left_handle.png'
    Right_source = f'./{file_path}/part_contour/right_handle.png'
    Bottom_source = f'./{file_path}/part_contour/bottom.png'
    Lower_bottom_source = f'./{file_path}/part_contour/lower_bottom.png'
    Cushion_source = f'./{file_path}/part_contour/cushion.png'
    Back_cushion_source = f'./{file_path}/part_contour/back_cushion.png'
    Box_leg_source = f'./{file_path}/part_contour/box_leg.png'
    Cylinder_leg_source = f'./{file_path}/part_contour/cylinder_leg.png'
    Left_irregular_source = f'./{file_path}/part_contour/left_handle_irregular.png'
    Right_irregular_source = f'./{file_path}/part_contour/right_handle_irregular.png'
    lower_bottom_height = 0
    back_cushion_offset = 0
    parts_obj = {}
    if os.path.isfile(Left_source):
        pass
    elif os.path.isfile(Left_irregular_source):
        Left_source = Left_irregular_source
        Right_source = Right_irregular_source
        irregular_flag = True
    else:
        exit()
    whole_length , whole_width, whole_height, height_ratio = whole_lwh(Left_source, Right_source)

    if os.path.isfile(Left_source):
        left_handle_length, left_obj, right_obj= create_handle(Left_source, whole_length , whole_width, whole_height)
        if not irregular_flag:
            parts_obj["left_handle"] = left_obj["left_handle"]
            parts_obj["right_handle"] = right_obj["right_handle"]

    if os.path.isfile(Lower_bottom_source):
        obj, lower_bottom_height = create_lower_bottom(Lower_bottom_source, whole_length , whole_width, whole_height, left_handle_length)
        parts_obj["lower_bottom"] = obj["lower_bottom"]

    if os.path.isfile(Bottom_source):
        obj, bottom_height = create_bottom(Bottom_source, whole_length , whole_width, whole_height, left_handle_length, lower_bottom_height)
        parts_obj["bottom"] = obj["bottom"]

    if os.path.isfile(Back_cushion_source):
        offset = cushion_offset(Cushion_source, Back_cushion_source)
        obj, back_cushion_offset = create_back_cushion(Back_cushion_source, whole_length, whole_width, whole_height, height_ratio, left_handle_length, offset)
        parts_obj["back_cushion"] = obj["back_cushion"]

    if os.path.isfile(Cushion_source):
        obj = create_cushion(Cushion_source, whole_length , whole_width, whole_height, height_ratio, left_handle_length, bottom_height, lower_bottom_height, back_cushion_offset)
        parts_obj["cushion"] = obj["cushion"]

    if os.path.isfile(Box_leg_source):
        obj1, obj2, obj3, obj4 = create_box_legs(Box_leg_source, whole_length, whole_width, whole_height)
        parts_obj["leg1"] = obj1["leg1"]
        parts_obj["leg2"] = obj2["leg2"]
        parts_obj["leg3"] = obj3["leg3"]
        parts_obj["leg4"] = obj4["leg4"]

    if os.path.isfile(Cylinder_leg_source):
        obj1, obj2, obj3, obj4 = create_cylinder_legs(Cylinder_leg_source, whole_length, whole_width, whole_height)
        parts_obj["leg1"] = obj1["leg1"]
        parts_obj["leg2"] = obj2["leg2"]
        parts_obj["leg3"] = obj3["leg3"]
        parts_obj["leg4"] = obj4["leg4"]
    
    if os.path.isfile(Left_irregular_source) and irregular_flag:
        obj = create_irregular_handles(file_path, whole_length, whole_width, whole_height, left_handle_length)
        parts_obj["left_handle_irregular"] = obj["left_handle_irregular"]
        parts_obj["right_handle_irregular"] = obj["right_handle_irregular"]

    postfix = file_path.split("\\")[1]
    with open(f'{file_path}/{postfix}.json', 'w', encoding='utf-8') as f:
        json.dump(parts_obj, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run('chairs\\7-1')