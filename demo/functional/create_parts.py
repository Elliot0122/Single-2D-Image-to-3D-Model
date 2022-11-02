from functional.reference_points import get_parameter
from functional.rectification import run_rectification
from functional.construct_primitives import construct_box, construct_cylinder
from functional.make_contour import run_contour, left_bottom_point_of_irregular_handle

def create_handle(path, whole_length , whole_width, whole_height, left_right_ratio):
    length, width , height = get_parameter(path)
    left_obj = construct_box("left_handle", whole_length/2, 0, 0, length/left_right_ratio, whole_width, height)
    right_obj = construct_box("right_handle", -whole_length/2, 0, 0, length/left_right_ratio, whole_width, height)
    
    return length/left_right_ratio, height, left_obj, right_obj

def create_lower_bottom(path, whole_length , whole_width, whole_height, left_length):
    length, width , height = get_parameter(path)
    obj = construct_box("lower_bottom", 0, 0, -(whole_height-height)/2, whole_length-left_length, whole_width, height)
    
    return obj, height

def create_bottom(path, whole_length , whole_width, whole_height, left_length, lower_bottom_height):
    length, width , height = get_parameter(path)
    obj = construct_box("bottom", 0, 0, -(whole_height-height)/2+lower_bottom_height, whole_length-left_length, whole_width, height)
    
    return obj, height

def create_back_cushion(path, whole_length , whole_width, whole_height, left_length, bottom_height, lower_bottom_height, cush_h):
    obj = construct_box("back_cushion", 0, (whole_width-left_length)/2, -(whole_height-cush_h)/2+bottom_height+lower_bottom_height, whole_length-left_length, left_length, cush_h)

    return obj, left_length

def create_cushion(path, whole_length , whole_width, whole_height, left_length, bottom_height, lower_bottom_height, back_cushion_offset, cush_h):
    obj = construct_box("cushion", 0, (whole_width-left_length)/2-back_cushion_offset, -(whole_height-cush_h)/2+bottom_height+lower_bottom_height, whole_length-left_length, left_length, cush_h)
    
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

def create_irregular_handles(path, whole_length, whole_width, whole_height):
    obj = {}
    thickness = run_rectification(path, whole_length, whole_height)
    contour_points = run_contour(path)
    lebo = left_bottom_point_of_irregular_handle(contour_points)
    left_points = []
    right_points = []
    for i in contour_points:
        temp = []
        temp.append(i[0] + (whole_length+thickness)/2)
        temp.append(i[1] - lebo[1] + whole_width/2)
        temp.append(i[2] - lebo[2] - whole_height/2)
        left_points.append(temp)
    for i in contour_points:
        temp = []
        temp.append(i[0] - (whole_length+thickness)/2)
        temp.append(i[1] - lebo[1] + whole_width/2)
        temp.append(i[2] - lebo[2] - whole_height/2)
        right_points.append(temp)
    obj["left_handle_irregular"] = {"type":"Plane_extrue", "parameter":{"points":left_points, "thickness":-thickness}}
    obj["right_handle_irregular"] = {"type":"Plane_extrue", "parameter":{"points":right_points, "thickness":+thickness}}
    return obj, thickness