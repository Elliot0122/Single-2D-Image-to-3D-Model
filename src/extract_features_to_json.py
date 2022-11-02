import json
import os
import numpy as np
import functional.create_parts as cp
from functional.reference_points import whole_lwh, whole_lwh_without_handles, cushion_height

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
    if os.path.isfile(Left_source):
        whole_length , whole_width, whole_height, left_right_ratio= whole_lwh(Left_source, Right_source)
    elif os.path.isfile(Cushion_source):
        whole_length, whole_width, whole_height, left_right_ratio = whole_lwh_without_handles(Cushion_source)
    left_right_ratio-=0.5

    if os.path.isfile(Left_source):
        if not irregular_flag:
            left_handle_length, whole_height, left_obj, right_obj= cp.create_handle(Left_source, whole_length , whole_width, whole_height, left_right_ratio)
            parts_obj["left_handle"] = left_obj["left_handle"]
            parts_obj["right_handle"] = right_obj["right_handle"]
        else:
            obj, left_handle_length= cp.create_irregular_handles(file_path, whole_length, whole_width, whole_height)
            parts_obj["left_handle_irregular"] = obj["left_handle_irregular"]
            parts_obj["right_handle_irregular"] = obj["right_handle_irregular"]
    else:
        left_handle_length = 0

    if os.path.isfile(Lower_bottom_source):
        obj, lower_bottom_height = cp.create_lower_bottom(Lower_bottom_source, whole_length , whole_width, whole_height, left_handle_length)
        parts_obj["lower_bottom"] = obj["lower_bottom"]

    if os.path.isfile(Bottom_source):
        obj, bottom_height = cp.create_bottom(Bottom_source, whole_length , whole_width, whole_height, left_handle_length, lower_bottom_height)
        parts_obj["bottom"] = obj["bottom"]

    if os.path.isfile(Back_cushion_source):
        if os.path.isfile(Right_source):
            cush_h = cushion_height(Right_source, Back_cushion_source, whole_height, lower_bottom_height, bottom_height)
        else:
            cush_h = whole_height
            left_handle_length = bottom_height
        obj, back_cushion_offset = cp.create_back_cushion(Back_cushion_source, whole_length, whole_width, whole_height, left_handle_length, bottom_height, lower_bottom_height, cush_h)
        parts_obj["back_cushion"] = obj["back_cushion"]

    if os.path.isfile(Cushion_source):
        if os.path.isfile(Right_source):
            cush_h = cushion_height(Right_source, Cushion_source, whole_height, lower_bottom_height, bottom_height)
        else:
            cush_h = whole_height
            left_handle_length = bottom_height
        obj = cp.create_cushion(Cushion_source, whole_length , whole_width, whole_height, left_handle_length, bottom_height, lower_bottom_height, back_cushion_offset, cush_h)
        parts_obj["cushion"] = obj["cushion"]

    if os.path.isfile(Box_leg_source):
        obj1, obj2, obj3, obj4 = cp.create_box_legs(Box_leg_source, whole_length, whole_width, whole_height)
        parts_obj["leg1"] = obj1["leg1"]
        parts_obj["leg2"] = obj2["leg2"]
        parts_obj["leg3"] = obj3["leg3"]
        parts_obj["leg4"] = obj4["leg4"]

    if os.path.isfile(Cylinder_leg_source):
        obj1, obj2, obj3, obj4 = cp.create_cylinder_legs(Cylinder_leg_source, whole_length, whole_width, whole_height)
        parts_obj["leg1"] = obj1["leg1"]
        parts_obj["leg2"] = obj2["leg2"]
        parts_obj["leg3"] = obj3["leg3"]
        parts_obj["leg4"] = obj4["leg4"]

    postfix = file_path.split("\\")[3]
    with open(f'{file_path}/{postfix}.json', 'w', encoding='utf-8') as f:
        json.dump(parts_obj, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run('.\\..\\data\\1-1')
