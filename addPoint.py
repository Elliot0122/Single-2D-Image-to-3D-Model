import copy
import math
from collections import defaultdict
import numpy as np
def distance(pointA,pointB):
    A = pointA.split(' ')
    B = pointB.split(' ')
    d = math.sqrt(math.pow(float(A[1])-float(B[1]),2) + math.pow(float(A[2])-float(B[2]),2) + math.pow(float(A[3])-float(B[3]),2))
    return d
def middle(pointA,pointB):
    A = pointA.split(' ')
    B = pointB.split(' ')
    d = 'v '
    x = str((float(A[1])+float(B[1]))/2)
    y = str((float(A[2])+float(B[2]))/2)
    z = str((float(A[3])+float(B[3]))/2)
    d = d + x + ' ' + y + ' ' + z
    return d
def classify(data,linesF,linesV):
    lines = data.split('\n')
    for r in lines:
        if(r.split(' ')[0] == 'f'):
            linesF.append(r)
        else:
            linesV.append(r)
    linesV.pop()
def findneighbor(data):
    linesF = []
    linesV = []
    Add_point = []
    
    classify(data,linesF,linesV)
    now_line = len(linesV)
    dict = defaultdict(list)
    for r in range(len(linesV)):
        dict[r + 1] = []
    for r in linesF:
        point = r.split(' ')
        temp = len(point)
        while(temp > 1):
            temp -= 2
            if(temp == 1):
                if(point[len(point) - 1] not in dict[int(point[temp])]):
                    dict[int(point[temp])].append(point[len(point) - 1])
                if(point[temp + 1] not in dict[int(point[temp])]):
                    dict[int(point[temp])].append(point[temp + 1])
            else:
                if(point[temp - 1] not in dict[int(point[temp])]):
                    dict[int(point[temp])].append(point[temp - 1])
                if(point[temp + 1] not in dict[int(point[temp])]):
                    dict[int(point[temp])].append(point[temp + 1])
    for r in dict.keys():
        for i in dict[r]:
            i = int(i)
            d = distance(linesV[r-1],linesV[i-1])
            l = ''
            if(d > 5):
                l = middle(linesV[r-1],linesV[i-1])
                add_point = []
                add_point.append(now_line + 1)
                now_line+=1
                add_point.append(l)
                add_point.append(r)
                add_point.append(i)
                Add_point.append(add_point)
    for r in Add_point:
        linesV.append(r[1])
    linesF_update = []
    for r in linesF:
        pointF = r.split(' ')
        line = 'f'
        for i in Add_point:
            if(str(i[2]) in pointF and str(i[3]) in pointF):
                
                temp = 0
                pos = []
                for j in pointF:
                    if(str(i[2]) == j):
                        pos.append(temp)
                    if(str(i[3]) == j):
                        pos.append(temp)
                    temp+=1
                pos.sort()
                if(len(pos) > 2):
                    pass
                else:
                    if(pos[0] == 1 and pos[1] == len(pointF) - 1):
                        pointF.append(str(i[0]))
                    else:
                        for j in range(len(pointF)):
                            if(pos[0] == j and pos[1] == j + 1):
                                pointF.insert(pos[0] + 1,str(i[0]))
        for i in pointF[1:]:
            line += ' ' + i
        
        linesF_update.append(line)
    return linesV + linesF_update
def run(file_path):
    postfix = file_path.split("\\")[1]
    prefix = file_path.split("\\")[0]
    data = []
    file_name = f'{prefix}/{postfix}.obj'
    with open(f"{prefix}/{postfix}.obj",'r+') as f:
        data = f.read()
        data = findneighbor(data)
    with open(f"{prefix}/{postfix}_new.obj",'w+') as f:
        for r in data:
            f.write(r + '\n')


if __name__ == "__main__":
    run('addPointtest\\test')