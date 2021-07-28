import json

def read_Json(file_name):
    with open(file_name, "r") as f:
        d = json.load(f)
    return d
def create_sphere_circle(types, parameter):
    f.write(f'rs.Add{types}({parameter["reference_point"]}, {parameter["radius"]})\n')
def create_cylinder_cone(types, parameter):
    f.write(f'rs.Add{types}({parameter["reference_point"]}, {parameter["height"]}, {parameter["radius"]}, {parameter["cap"]})\n')
def create_point(types, parameter):
    f.write(f'rs.Add{types}({parameter["reference_point"]})\n')
def create_box(types, parameter):
    refer_point = parameter["reference_point"]
    len_wid_hei = parameter["l_w_h"]
    corner = [
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2],
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2]]
    f.write(f'rs.Add{types}({corner})\n')
def create_box_with_points(types, parameter):
    f.write(f'rs.Add{types}({parameter})\n')
def create_object(types, parameter):
    objects = {
        "Sphere": create_sphere_circle,
        "Circle": create_sphere_circle,
        "Cone": create_cylinder_cone,
        "Cylinder": create_cylinder_cone,
        "Point": create_point,
        "Box": create_box,
        "Box_with_points": create_box_with_points
    }
    return objects[types](types, parameter)

if __name__ == "__main__":
    chair = '32-1'
    file_name = f"{chair}/{chair}.json"
    f = open(f"{file_name.split('.')[0]}_rhino.py", 'w')
    f.write("import rhinoscriptsyntax as rs\n")
    data = read_Json(file_name)
    for element in data:
        create_object(data[element]["type"], data[element]["parameter"])
    f.close()