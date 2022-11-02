import json
import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
def cross(o,a,b):
    return (a[1] - o[1]) * (b[2] - o[2]) - (a[2] - o[2]) * (b[1] - o[1])
def compare(a,b):
    return (a[1] < b[1]) or (a[1] == b[1] and a[2] < b[2])
def Andrew_monotone_chain(points):
    sorted(points, points + len(points), compare)
    l,u=0,0
    for i in range(len(points)):
        
def link_topandbottom_irregular(f,line,length,points,Line, thick):
    
    int_stack_down = []
    int_stack_up = []

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
            