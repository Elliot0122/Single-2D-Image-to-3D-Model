import json
import math
from operator import itemgetter
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from add_curve import add_curve
# Line = 1
def combine(obj_data):
    vertices = []
    faces = []
    point_num = 0
    tmp_p = 0
    switch = False
    for r in obj_data:
        tmp = r.strip().split(' ')
        if tmp[0]=="v":
            if switch:
                point_num = tmp_p
                switch = False
            tmp_p+=1
            tmp = list(map(float, tmp[1:]))
            vertices.append(tmp)
            
        else: 
            face_num = point_num
            tmp = list(map(int, tmp[1:]))
            for r in range(len(tmp)):
                tmp[r] = tmp[r] + face_num
            faces.append(tmp)
            switch = True
    return vertices, faces
    
    

def read_Json(file_path):
    with open(file_path, "r") as f:
        d = json.load(f)
    
    return d
# def record_Line(line):
#     global Line
#     Line = line
def link_contour(line,length,obj_data):
    half_len = int(length/2)
    for r in range(half_len - 1):
        if(r == 0):
            str = 'f {0} {1} {2} {3}\n'.format(r + line, r + line + half_len - 1, r + line + length - 1, r + line + half_len)
            obj_data.append(str)
        str = 'f {0} {1} {2} {3}\n'.format(r + line, r + line + 1, r + line + half_len + 1, r + line + half_len)
        obj_data.append(str)
            
def link_topandbottom(line,length,obj_data):
    str = ''
    half_len = int(length/2)
    str+='f'
    for r in range(half_len):
        str+=' {0}'.format(r + line)
    str+='\n'
    obj_data.append(str)
    str = ''
    str+='f'
    for r in range(half_len):
        str+=' {0}'.format(r + line + half_len)
    str+='\n'
    obj_data.append(str)

def link_topandbottom_irregular(line,length,points,obj_data, thick,up_n):
    int_stack_down = []
    int_stack_up = []
    for r in range(up_n):
        for i in range(up_n, length//2):
            if(points[i][0] == points[r][0]) and (points[i][1] == points[r][1]):
                int_stack_up.append(i)
                break
        int_stack_down.append(r)
    for r in range(length//2, up_n + length//2):
        for i in range(up_n + length//2, length):
            if(points[i][0] == points[r][0]) and (points[i][1] == points[r][1]):
                int_stack_up.append(i)
                break
        int_stack_down.append(r)
    length = len(int_stack_down)     
    for r in range(length-1):
        obj_data.append('f {0} {1} {2} {3}\n'.format(line + int_stack_down[r], line + int_stack_up[r], line + int_stack_up[r + 1], line + int_stack_down[r + 1]))
def create_sphere_circle(types, parameter,obj_data):
    obj_data.append(f'rs.Add{types}({parameter["reference_point"]}, {parameter["radius"]})\n')

def create_cylinder_cone(types, parameter,obj_data):
    obj_cone = []
    PI = math.pi
    angle = PI / 180
    points = []
    now_Line = 1
    ref_point = parameter["reference_point"]
    het = parameter["height"]
    radius = parameter["radius"]
    cap = parameter["cap"]
    for r in range(0,360,15):
        point = [ref_point[0]+radius*math.cos(r * angle),ref_point[1] + radius*math.sin(r * angle),ref_point[2] + het]
        points.append(point)
    for r in range(0,360,15):
        point = [ref_point[0]+radius*math.cos(r * angle),ref_point[1] + radius*math.sin(r * angle),ref_point[2]]
        points.append(point)
    for r in points:
        str = 'v {0} {1} {2}\n'.format(r[0],r[2],r[1])
        obj_cone.append(str)
    length = int(len(points))
    link_topandbottom(now_Line,length,obj_cone)
    link_contour(now_Line,length,obj_cone)
    for r in obj_cone:
        obj_data.append(''.join(r))
    #record_Line(line)


def create_point(types, parameter,obj_data):
    obj_point = []
    ref_point = parameter["points"]
    now_Line = 1
    for r in ref_point:
        str = 'v {0} {1} {2}\n'.format(r[0],r[2],r[1])
        obj_point.append(str)
    length = int(len(ref_point))
    link_topandbottom(now_Line,length,obj_point)
    link_contour(now_Line,length,obj_point)
    for p in obj_point:
        obj_data.append(''.join(p))
    #record_Line(line)
def create_box(types, parameter,obj_data):
    obj_box = []
    print('create box')
    corner_index = [1,2,3,4,5,6,7,8]
    curvature = 0.3
    #curvature = float(input('please input curvature (0-1): '))
    #corner_index = map(int,input('please input corner (1-8): ').split())
    refer_point = parameter["reference_point"]
    len_wid_hei = parameter["l_w_h"]
    now_Line = 1
    corner = [
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2],
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]-len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]-len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]+len_wid_hei[2]/2],
        [refer_point[0]+len_wid_hei[0]/2, refer_point[1]+len_wid_hei[1]/2, refer_point[2]-len_wid_hei[2]/2]]
    for r in corner:
        s = 'v {0} {1} {2}\n'.format(r[0],r[2],r[1])
        obj_box.append(s)
    length = int(len(corner))
    link_topandbottom(now_Line,length,obj_box)
    link_contour(now_Line,length,obj_box)
    #record_Line(line)
    vertices = []
    faces = []
    for line in obj_box:
        tmp = line.strip().split(' ')
        if tmp[0]=="v":
            tmp = list(map(float, tmp[1:]))
            vertices.append(tmp)
        else: 
            tmp = list(map(int, tmp[1:]))
            faces.append(tmp)
    v, faces = add_curve(vertices, faces, curvature, corner_index)
    
    for r in v:
        r = list(map(str, r))
        obj_data.append('v ' + ' '.join(r) + '\n')
    for f in faces:
        f = list(map(str, f))
        obj_data.append('f ' + ' '.join(f) + '\n')
def create_box_with_points(types, parameter, obj_data):
    str = f'rs.Add{types}({parameter["points"]})\n'
    obj_data.append(str)
def cross(o,a,b):
    return (a[1] - o[1]) * (b[2] - o[2]) - (a[2] - o[2]) * (b[1] - o[1])
def compare(a):
    return (a[1],a[2])
def Andrew_monotone_chain(points):
    CH = []
    CH_up = []
    CH_down = []
    points.sort(key = compare)
    m = 0
    for i in range(len(points)):
        while m >= 2 and cross(CH[m-2],CH[m-1],points[i]) <= 0:
            m-=1
            CH.pop()
        CH.append(points[i])
        m+=1
    t = m+1
    CH_up = CH.copy()
    for i in range(len(points) - 2, -1, -1):
        
        while(m >= t and cross(CH[m-2],CH[m-1],points[i]) <= 0):
            m-=1
            CH.pop()
            CH_down.pop()
        CH.append(points[i])
        CH_down.append(points[i])
        m+=1
    m-=1
    for r in range(1, len(CH_up)):
        for i in range(len(CH_down)):
            if CH_up[r][1] == CH_down[i][1]:
                break
            elif CH_up[r][1] > CH_down[i][1]:
                if i == 0:
                    CH_down.insert(0,CH_up[r])
                else:
                    k = (CH_down[i - 1][2] - CH_down[i][2])/(CH_down[i - 1][1] - CH_down[i][1])
                    b = CH_down[i][2] - CH_down[i][1] * k
                    p = CH_up[r].copy()
                    p[2] = CH_up[r][1] * k + b
                    CH_down.insert(i,p)
                break
    CH = CH_up + CH_down
    return CH,len(CH_up)
def create_extrude_plane(types, parameter, obj_data):
    obj_plane = []
    ref_point = parameter["points"]
    thick = parameter["thickness"]
    now_Line = 1
    points = []
    ref_point,up_n = Andrew_monotone_chain(ref_point)
    for r in ref_point:
        point = [r[0]+thick,r[1],r[2]]
        points.append(point)
        
    ref_point += points
    for r in ref_point:
        str = 'v {0} {1} {2}\n'.format(r[0],r[2],r[1])
        obj_plane.append(str)
    length = int(len(ref_point))
    link_topandbottom_irregular(now_Line,length,ref_point,obj_plane, thick, up_n)
    link_contour(now_Line,length,obj_plane)
    for r in obj_plane:
        obj_data.append(''.join(obj_plane))
    #record_Line(line)
    #drawpic(f,types,parameter,line)
    

def create_object(types, parameter, obj_data):
    objects = {
        "Sphere": create_sphere_circle,
        "Circle": create_sphere_circle,
        "Cone": create_cylinder_cone,
        "Cylinder": create_cylinder_cone,
        "Point": create_point,
        "Box": create_box,
        "Box_with_points": create_box_with_points,
        "Plane_extrue": create_extrude_plane
    }
    
    return objects[types](types, parameter, obj_data)
# def drawpic(f, types, parameter, line):
#     ref_point = parameter["points"]
#     width = 2000
#     height = 2000
#     img_black = Image.new(mode = 'RGB',size = (width,height),color = (0,0,0))
#     # img_black = np.array(img_black, dtype=np.uint8)
#     # img_black.setflags(write=1)
#     for r in ref_point:
#         # img_black[r[1],r[2]] = (0,0,0)
#         img_black.putpixel((int(r[1]),int(r[2])),(255,255,255))
#     img_black.show()
def run(file_path):
    #record_Line(1)
    postfix = file_path.split("\\")[1]
    prefix = file_path.split("\\")[0]
    file_name = f'{prefix}/{postfix}/{postfix}.json'
    obj_data = []
    # with open(f"{prefix}/{postfix}.obj",'w+') as f:
    #     data = read_Json(file_name)
    #     for element in data:
    #         create_object(f, data[element]["type"], data[element]["parameter"], line = Line)
    data = read_Json(file_name)
    for element in data:
        create_object(data[element]["type"], data[element]["parameter"], obj_data)
    vertices, faces = combine(obj_data)
    with open(f"{prefix}/{postfix}.obj",'w+') as f:
        for vertice in vertices:
            vertice = list(map(str, vertice))
            f.write('v ' + ' '.join(vertice) + '\n')
        for face in faces:
            face = list(map(str, face))
            f.write('f ' + ' '.join(face) + '\n')
    

if __name__ == "__main__":
    run('chairs\\2-1')