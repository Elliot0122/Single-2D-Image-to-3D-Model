import cv2
import numpy as np
from numpy.linalg import norm as distance

def length_height(left_source, right_source):
    left_handle = cv2.imread(left_source)
    right_handle = cv2.imread(right_source)
    left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
    right_handle_gray = cv2.cvtColor(right_handle, cv2.COLOR_BGR2GRAY)
    l_cont = np.array(np.where(left_handle_gary == 255))
    r_cont = np.array(np.where(right_handle_gray == 255))

    # left_top -> right_top -> right_bottom -> left bottom
    reference_points = np.zeros((4, 2))

    diff_s = 0
    diff_b = 10000000
    for i in r_cont.T:
        # y = x + n maximum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            reference_points[3] = i
        # y = -x + n minimum
        if i[0] + i[1] <= diff_b:
            diff_b = i[0] + i[1]
            reference_points[0] = i
    diff_s = 0
    diff_b = 10000000
    for i in l_cont.T:
        # y = x + n maximum
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            reference_points[2] = i
        # y = -x + n minimum
        if i[0] + i[1] <= diff_b:
            diff_b = i[0] + i[1]
            reference_points[1] = i

    # x and y are swapped b/c of opencv axis type => horizontal->x vertical ->y
    for i in reference_points:
        i[0], i[1] = i[1], i[0]

    return int(distance(reference_points[2]-reference_points[3])), int(distance(reference_points[1]-reference_points[2]))

def front_back_height_ratio(left_source):
    left_handle = cv2.imread(left_source)
    left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
    l_cont = np.array(np.where(left_handle_gary == 255))
    
    # left_top(B) -> right_top(C) -> right_bottom(C') -> left bottom(B')
    reference_points = np.zeros((4, 2))
    temp_point = [0, 0]
    diff_s = 0
    diff_b = 10000000
    for i in l_cont.T:
        # y = n maximum
        if 3*i[0] + i[1] >= diff_s:
            diff_s = 3*i[0]+i[1]
            reference_points[3] = i
        # y = -x + n minimum
        if i[0] + i[1] <= diff_b:
            diff_b = i[0]+i[1]
            reference_points[0] = i
    diff_s = 0
    diff_b = 10000000
    for i in l_cont.T:
        # y = x + n maximum
        if i[0] - i[1] <= diff_b:
            diff_b = i[0] - i[1]
            reference_points[1] = i
        # y = -0.5x + n maximum
        if 0.5*i[0] + i[1] >= diff_s:
            diff_s = 0.5*i[0]+i[1]
            reference_points[2] = i

    # getting the offset of the reference point
    diff_s = 0
    for i in l_cont.T:
        if i[0] - i[1] >= diff_s:
            diff_s = i[0] - i[1]
            temp_point = i
    reference_points[0] += reference_points[3]-temp_point
    # image = cv2.imread("32-1.png")
    # for i in reference_points:
    #     print(i)
    #     image[int(i[0])-20][int(i[1])-20] = [0, 0, 255]
    # cv2.imwrite("test.png", image)
    
    return distance(reference_points[0]-reference_points[3])/distance(reference_points[1]-reference_points[2])

# def width(left_source, right_source):
#     left_handle = cv2.imread(left_source)
#     right_handle = cv2.imread(right_source)
#     left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
#     l_cont = np.array(np.where(left_handle_gary == 255))
    
#     # left_top(B) -> right_top(C) -> right_bottom(C') -> left bottom(B') -> A -> A'
#     reference_points = np.zeros((6, 2))
#     temp_point = [0, 0]
#     diff_s = 0
#     diff_b = 10000000
#     for i in l_cont.T:
#         # y = n maximum
#         if 3*i[0] + i[1] >= diff_s:
#             diff_s = 3*i[0]+i[1]
#             reference_points[3] = i
#         # y = -x + n minimum
#         if i[0] + i[1] <= diff_b:
#             diff_b = i[0]+i[1]
#             reference_points[0] = i
#     diff_s = 0
#     diff_b = 10000000
#     for i in l_cont.T:
#         # y = x + n maximum
#         if i[0] - i[1] <= diff_b:
#             diff_b = i[0] - i[1]
#             reference_points[1] = i
#         # y = -0.5x + n maximum
#         if 0.5*i[0] + i[1] >= diff_s:
#             diff_s = 0.5*i[0]+i[1]
#             reference_points[2] = i

#     # getting the offset of the reference point
#     diff_s = 0
#     for i in l_cont.T:
#         if i[0] - i[1] >= diff_s:
#             diff_s = i[0] - i[1]
#             temp_point = i
#     reference_points[0] += reference_points[3]-temp_point

#     BBp = distance(reference_points[0]-reference_points[3])
#     CCp = distance(reference_points[1]-reference_points[2])
#     upper = np.linalg.solve([[reference_points[0][1], 1], [reference_points[1][1], 1]], [[reference_points[0][0]], [reference_points[1][0]]])
#     lower = np.linalg.solve([[reference_points[2][1], 1], [reference_points[3][1], 1]], [[reference_points[2][0]], [reference_points[3][0]]])
#     temp_point[1] -= 29
#     A = np.array([upper[0][0]*temp_point[1]+upper[1][0], temp_point[1]])
#     Ap = np.array([lower[0][0]*temp_point[1]+lower[1][0], temp_point[1]])
#     AAp = distance(A-Ap)
#     d = distance(Ap-reference_points[3])
#     A = [[-1, 0, AAp],
#          [-1, 0, BBp],
#          [-1, CCp, CCp]]
#     B = [[AAp*d],
#          [0],
#          [0]]
#     x = np.linalg.solve(A, B)

#     return int(x[1])

if __name__== "__main__":
    left_source = './32-1/part_contour/left_handle.png'
    right_source = './32-1/part_contour/right_handle.png'
    print(length_height(left_source, right_source))
    print(front_back_height_ratio(left_source))