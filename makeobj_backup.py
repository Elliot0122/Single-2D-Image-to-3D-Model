import json
import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
Line = 1
def read_Json(file_path):
    with open(file_path, "r") as f:
        d = json.load(f)
    
    return d
def record_Line(line):
    global Line
    Line = line
def link_contour(f,line,length):
    half_len = int(length/2)
    for r in range(half_len - 1):
        if(r == 0):
            f.write('f {0} {1} {2} {3}\n'.format(r + line, r + line + half_len - 1, r + line + length - 1, r + line + half_len))
        f.write('f {0} {1} {2} {3}\n'.format(r + line, r + line + 1, r + line + half_len + 1, r + line + half_len))
            
def link_topandbottom(f, line,length):
    half_len = int(length/2)
    f.write('f')
    for r in range(half_len):
        f.write(' {0}'.format(r + line))
    f.write('\n')
    f.write('f')
    for r in range(half_len):
        f.write(' {0}'.format(r + line + half_len))
    f.write('\n')

def link_topandbottom_irregular(f,line,length,points,Line, thick):
    int_stack_down = []
    int_stack_up = []
    throw_stack = []
    minus = []
    for r in range(length):
        
        
        in_stack = False
        if r not in int_stack_down and r not in int_stack_up:
            for i in range(length):
                
                if(points[i][0] == points[r][0]) and (points[i][1] == points[r][1]) and (i not in int_stack_up) and (points[r] != points[i]):
                    if(in_stack == False):
                        int_stack_up.append(i)
                        in_stack = True
                    
            if(in_stack):
                int_stack_down.append(r)
        
        
    
    
    
    length = len(int_stack_down)
    cnt = 0
    for r in range(1,length):
        cnt += 1
        if(cnt == length):break
        if(points[int_stack_down[cnt]][1] == points[int_stack_down[cnt - 1]][1]):
            int_stack_down.pop(cnt)
            int_stack_up.pop(cnt)
            length-=1
            cnt -= 1

        if(points[int_stack_up[cnt]][1] == points[int_stack_up[cnt - 1]][1]):
            int_stack_down.pop(cnt)
            int_stack_up.pop(cnt)
            length-=1
            cnt -= 1
    length = len(int_stack_down)        
    cnt = 0
    for r in range(1,length):
        cnt += 1
        if cnt == length: break
        if abs(points[int_stack_up[cnt]][2] - points[int_stack_down[cnt]][2]) < 0.1:
            int_stack_down.pop(cnt)
            int_stack_up.pop(cnt)
            length-=1
            cnt-=1


    for r in range(length-1):
        f.write('f {0} {1} {2} {3}\n'.format(line + int_stack_down[r], line + int_stack_up[r], line + int_stack_up[r + 1], line + int_stack_down[r + 1]))
            
    
    return Line
def create_sphere_circle(f, types, parameter,line):
    f.write(f'rs.Add{types}({parameter["reference_point"]}, {parameter["radius"]})\n')

def create_cylinder_cone(f, types, parameter,line):
    PI = math.pi
    angle = PI / 180
    points = []
    now_Line = line
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
        f.write('v {0} {1} {2}\n'.format(r[0],r[2],r[1]))
        line+=1
    length = int(len(points))
    link_topandbottom(f,now_Line,length)
    link_contour(f,now_Line,length)
    record_Line(line)
    

def create_point(f, types, parameter,line):
    ref_point = parameter["points"]
    now_Line = line
    for r in ref_point:
        f.write('v {0} {1} {2}\n'.format(r[0],r[2],r[1]))
        line+=1
    length = int(len(ref_point))
    link_topandbottom(f,now_Line,length)
    link_contour(f,now_Line,length)
    record_Line(line)
def create_box(f, types, parameter,line):
    refer_point = parameter["reference_point"]
    len_wid_hei = parameter["l_w_h"]
    now_Line = line
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
        f.write('v {0} {1} {2}\n'.format(r[0],r[2],r[1]))
        line+=1
    length = int(len(corner))
    link_topandbottom(f,now_Line,length)
    link_contour(f,now_Line,length)
    record_Line(line)
def create_box_with_points(f, types, parameter, line):
    f.write(f'rs.Add{types}({parameter["points"]})\n')

def create_extrude_plane(f, types, parameter, line):
    ref_point = parameter["points"]
    thick = parameter["thickness"]
    now_Line = line
    points = []
    for r in ref_point:
        point = [r[0]+thick,r[1],r[2]]
        points.append(point)
    ref_point += points
    
    # ref_point_add = ref_point.copy()
    # cnt = 0
    # for r in range(len(ref_point_add) - 1):
    #     cnt+=1
    #     quot = ref_point_add[r + 1][1] - ref_point_add[r][1]
    #     mid_p  = ref_point_add[r].copy()
    #     for i in range(49):
    #         mid_p[1] += quot/50
    #         temp = mid_p.copy()
            
    #         ref_point.insert(cnt,temp)
    #         cnt+=1

    for r in ref_point:
        f.write('v {0} {1} {2}\n'.format(r[0],r[2],r[1]))
        line+=1
    length = int(len(ref_point))
    line = link_topandbottom_irregular(f,now_Line,length,ref_point,line, thick)
    link_contour(f,now_Line,length)
    record_Line(line)
    #drawpic(f,types,parameter,line)
    

def create_object(f, types, parameter, line):
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
    
    return objects[types](f, types, parameter, line)
def drawpic(f, types, parameter, line):
    ref_point = parameter["points"]
    width = 2000
    height = 2000
    img_black = Image.new(mode = 'RGB',size = (width,height),color = (0,0,0))
    # img_black = np.array(img_black, dtype=np.uint8)
    # img_black.setflags(write=1)
    for r in ref_point:
        # img_black[r[1],r[2]] = (0,0,0)
        img_black.putpixel((int(r[1]),int(r[2])),(255,255,255))
    img_black.show()
def run(file_path):
    record_Line(1)
    postfix = file_path.split("\\")[1]
    prefix = file_path.split("\\")[0]
    file_name = f'{prefix}/{postfix}/{postfix}.json'
    with open(f"{prefix}/{postfix}.obj",'w+') as f:
        data = read_Json(file_name)
        for element in data:
            create_object(f, data[element]["type"], data[element]["parameter"], line = Line)
    

if __name__ == "__main__":
    run('chairs\\16-1')