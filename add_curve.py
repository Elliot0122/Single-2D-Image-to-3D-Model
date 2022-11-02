import numpy as np

def read_obj(in_path):
    vertices = []
    faces = []

    f = open(in_path)
    for line in f.readlines():
        tmp = line.strip().split(' ')
        if tmp[0]=="v":
            tmp = list(map(float, tmp[1:]))
            vertices.append(tmp)
        elif tmp[0] =='f': 
            tmp = list(map(int, tmp[1:]))
            faces.append(tmp)
        else:
            continue
    f.close

    if not len(faces) or not len(vertices):
        return None, None

    return vertices, faces


def write_obj(vertices, faces, out_path):
    f = open(out_path, 'w')
    for vertice in vertices:
        vertice = list(map(str, vertice))
        f.write('v ' + ' '.join(vertice) + '\n')
    for face in faces:
        face = list(map(str, face))
        f.write('f ' + ' '.join(face) + '\n')
    f.close


def delete_multiple_element(list_object, indices):
    indices = sorted(indices, reverse=True)
    for idx in indices:
        list_object.pop(idx)


def add_curve(v, f, curvature = 0.0, corner=[1,2,3,4,5,6,7,8]):
    '''
    v: list of n vertices
    f: list of faces (on vertices 1 to n)
    corner: list, 8 vertex numbers which form 2 corners, [corner 1, corner 2]
    '''
    corner = [c - 1 for c in corner]
    # width: list of length 3
    # vertices of corner 1 + width = vertices of corner 2
    width = [v[corner[5]][i] - v[corner[1]][i] for i in range(3)]
    
    # ----- create bezier curve points on corner 1 -----
    # three 3d points for defining bezier curve
    P1 = np.array(v[corner[1]])
    dP1 = [(v[corner[0]][i] - v[corner[1]][i])*curvature for i in range(3)]
    dP2 = [(v[corner[2]][i] - v[corner[1]][i])*curvature for i in range(3)]
    P0, P2 = P1 + np.array(dP2), P1 + np.array(dP1)

    # define bezier curve 
    P = lambda t: (1 - t)**2 * P0 + 2 * t * (1 - t) * P1 + t**2 * P2 

    # evaluate the curve on [0, 1] sliced in n points
    n = 30
    curve_points = [P(t).tolist() for t in np.linspace(0, 1, n)]

    # ----- use curve_points to modify vertices and faces -----
    # delete 2 corner vertices
    idx = [corner[1], corner[5]]
    delete_multiple_element(v, idx)
    
    # delete 2 corner vertex numbers
    corner = [c + 1 for c in corner]
    d1, d2 = min(corner[1], corner[5]), max(corner[1], corner[5])
    c = []
    for x in corner:
        if x < d1:
            c.append(x)
        elif d1 < x < d2: 
            c.append(x - 1)
        elif x > d2:
            c.append(x - 2)
        else:   #x == d1 or x == d2
            pass

    # add curve_points to vertices
    for point in curve_points:
        v.append(point)
        v.append([point[i] + width[i] for i in range(3)])

    # create new faces
    faces = []
    faces.append([c[0], c[2], c[5], c[3]])
    faces.append([c[1], c[2], c[5], c[4]])
    faces.append([7, c[1], c[4], 8])
    x = 9
    for i in range(29):
        faces.append([x, x-2, x-1, x+1])
        x += 2
    faces.append([c[0], 65, 66, c[3]])

    left_face_points, right_face_points = [i for i in range(7, 66, 2)], [i for i in range(66, 7, -2)]
    left_face_points.extend([c[0], c[2], c[1]])
    right_face_points.extend([c[4], c[5], c[3]])
    faces.append(left_face_points)
    faces.append(right_face_points)
    
    return v, faces


if __name__ == '__main__':
    vt, faces = read_obj('014200.obj')
    v, faces = add_curve(vt, faces, 0.2, [1,2,3,4,5,6,7,8])
    # v, faces = add_curve(vt, faces, 0.2, [5,6,2,1,8,7,3,4])
    # v, faces = add_curve(vt, faces, 0.2, [6,2,1,5,7,3,4,8])
    write_obj(v, faces, './out_curve.obj')