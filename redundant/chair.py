import numpy as np
import cv2
from sys import exit

def part_contour(parts, height, length):
    contour = np.zeros((height, length))
    for i in range(height):
        for j in range(length):
            if (parts[i][j] == [0, 0, 0]).all():
                for k in range(j, -1, -1):
                    if edges[i][k] == 255:
                        contour[i][k] = 255
                        break
                for k in range(j, length):
                    if edges[i][k] == 255:
                        contour[i][k] = 255
                        break
                for k in range(i, -1, -1):
                    if edges[k][j] == 255:
                        contour[k][j] = 255
                        break
                for k in range(i, height):
                    if edges[k][j] == 255:
                        contour[k][j] = 255
                        break
    return contour

file_path = "chair_left.jpg"
image = cv2.imread(file_path)
height = image.shape[0]
length = image.shape[1]

edges = cv2.Canny(image,140,150)
cv2.imwrite("edges.png",edges)

try:
    Cushion = cv2.imread('parts/Cushion.png', cv2.IMREAD_GRAYSCALE)
    Left_handle = cv2.imread('parts/Left_handle.png', cv2.IMREAD_GRAYSCALE)
    Right_handle = cv2.imread('parts/Right_handle.png', cv2.IMREAD_GRAYSCALE)
    Bottom_part = cv2.imread('parts/Bottom_part.png', cv2.IMREAD_GRAYSCALE)
    Sample_leg = cv2.imread('parts/Sample_leg.png', cv2.IMREAD_GRAYSCALE)
    if ((Cushion.all()!=None)and(Left_handle.all()!=None)and(Right_handle.all()!=None)and(Bottom_part.all()!=None)and(Sample_leg.all() != None)):
        print("Separate file exist!")
except:
    print("Separate file not exist!")
    box = [[76, 111, 14], [3, 4, 8], [122, 110, 86], [202, 203, 201], 
           [69, 197, 240],[26, 2, 228], [89, 108, 235], [159, 165, 4], 
           [123, 147, 165], [160, 82, 95]]
    box_exist = []
    for i in box:
        if np.argwhere((image == i).all(axis=2)).size!=0:
            box_exist.append(i)
    image_part = np.full((len(box_exist), height, length, 3), 255)
    for i in range(height):
        for j in range(length):
            if (image[i][j] == [255, 255, 255]).all():
                continue
            else:
                sim = 0
                col = -1
                for k in range(len(box_exist)):
                    if (image[i][j] == box_exist[k]).all():
                        image_part[k][i][j] = [0, 0, 0]
    for i in range(len(box_exist)):
        cv2.imwrite(f"parts/{i}.png", image_part[i])
    # Cushion = np.full((height, length), 255)
    # Left_handle = np.full((height, length), 255)
    # Right_handle = np.full((height, length), 255)
    # Bottom_part = np.full((height, length), 255)
    # Sample_leg = np.full((height, length), 255)
    # for i in range(height):
    #     for j in range(length):
    #         #Cushion
    #         if image[i][j][0] == 202 and image[i][j][1] == 203 and image[i][j][2] == 201:
    #             Cushion[i][j] = 0
    #         #Left_handle
    #         elif image[i][j][0] == 122 and image[i][j][1] == 110 and image[i][j][2] == 86:
    #             Left_handle[i][j] = 0
    #         #Right_handle
    #         elif image[i][j][0] == 76 and image[i][j][1] == 111 and image[i][j][2] == 14:
    #             Right_handle[i][j] = 0
    #         #Bottom_part
    #         elif image[i][j][0] == 3 and image[i][j][1] == 4 and image[i][j][2] == 8:
    #             Bottom_part[i][j] = 0
    #         #Sample_leg
    #         elif image[i][j][0] > 17 and image[i][j][0] < 33 and image[i][j][1] >= 0 and image[i][j][1] < 16 and image[i][j][2] > 196 and image[i][j][2] < 236:
    #             Sample_leg[i][j] = 0
    # cv2.imwrite("parts/Cushion.png", Cushion)
    # cv2.imwrite("parts/Left_handle.png", Left_handle)
    # cv2.imwrite("parts/Right_handle.png", Right_handle)
    # cv2.imwrite("parts/Bottom_part.png", Bottom_part)
    # cv2.imwrite("parts/Sample_leg.png", Sample_leg)    
        
for i in range(len(box_exist)):
    cv2.imwrite(f"part_contour/{i}.png", part_contour(image_part[i], height, length))
# Cushion_cont = part_contour(Cushion, height, length)
# Left_handle_cont = part_contour(Left_handle, height, length)
# Right_handle = part_contour(Right_handle, height, length)
# Bottom_part = part_contour(Bottom_part, height, length) 
# Sample_leg = part_contour(Sample_leg, height, length)

# cv2.imwrite("part_contour/Cushion_cont.png", Cushion_cont)
# cv2.imwrite("part_contour/Left_handle_cont.png", Left_handle_cont)
# cv2.imwrite("part_contour/Right_handle_cont.png", Right_handle)
# cv2.imwrite("part_contour/Bottom_part_cont.png", Bottom_part)
# cv2.imwrite("part_contour/Sample_leg_cont.png", Sample_leg)