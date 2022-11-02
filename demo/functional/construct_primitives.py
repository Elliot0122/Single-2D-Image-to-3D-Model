def construct_box(part, ref_x, ref_y, ref_z, length, width, height):
    obj = {}
    obj[part] = {"type":"Box", "parameter":{"reference_point":[ref_x, ref_y, ref_z], "l_w_h":[length, width, height]}}
    
    return obj

def construct_cylinder(part, ref_x, ref_y, ref_z, length, width, height):
    obj = {}
    obj[part] = {"type":"Cylinder", "parameter":{"reference_point":[ref_x, ref_y, ref_z], "height":height, "radius": length/2, "cap": True}}
    
    return obj