import json

def read_Json(file_path):
    with open(file_path, "r") as f:
        d = json.load(f)
    
    return d

def create_sphere_circle(f, types, parameter):
    f.write(f'rs.Add{types}({parameter["reference_point"]}, {parameter["radius"]})\n')

def create_cylinder_cone(f, types, parameter):
    f.write(f'rs.Add{types}({parameter["reference_point"]}, {parameter["height"]}, {parameter["radius"]}, {parameter["cap"]})\n')

def create_point(f, types, parameter):
    f.write(f'rs.Add{types}({parameter["reference_point"]})\n')
    
def create_box(f, types, parameter):
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

def create_box_with_points(f, types, parameter):
    f.write(f'rs.Add{types}({parameter})\n')

def create_object(f, types, parameter):
    objects = {
        "Sphere": create_sphere_circle,
        "Circle": create_sphere_circle,
        "Cone": create_cylinder_cone,
        "Cylinder": create_cylinder_cone,
        "Point": create_point,
        "Box": create_box,
        "Box_with_points": create_box_with_points
    }
    
    return objects[types](f, types, parameter)

def run(file_path):
    postfix = file_path.split("\\")[1]
    file_name = f'{file_path}/{postfix}.json'
    f = open(f"{file_name}_rhino.py", 'w')
    f.write("import rhinoscriptsyntax as rs\n")
    data = read_Json(file_name)
    for element in data:
        create_object(f, data[element]["type"], data[element]["parameter"])
    f.close()

if __name__ == "__main__":
    run('chairs\\1-1')