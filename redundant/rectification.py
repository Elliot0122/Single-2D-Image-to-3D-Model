import cv2
import numpy as np
from numpy.linalg import norm as distance
import reference_points as rp

def get_image_size(src):
    ### give the corner points of the object in the image 
    ### return the points of the scanned image

    (tl, tr, br, bl) = src
 
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = distance(br-bl)**2/abs(br[0]-bl[0])
    widthB = distance(tr-tl)**2/abs(br[0]-bl[0])
    maxWidth = max(int(widthA), int(widthB))
 
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = distance(tr-br)
    heightB = distance(tl-bl)
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]])

    for i in range(4):
        dst[i][0] += src[0][0]
        dst[i][1] += src[0][1]
    
    return np.float32(dst)

def rectification(source, target):
    left_source = './part_contour/Left_handle_cont.png'
    right_source = './part_contour/Right_handle_cont.png'
    image = cv2.imread(source)
    image = cv2.imread(target)

    # get source and destination vertices
    # left_handle_cont and right_handle_cont in rp.side and rp.facadeare are based on
    # the contour we get from chair.py which would be stored in ./part_contour
    # src = rp.facade(left_source, right_source)
    src = rp.facade(left_source, right_source)
    print(src)
    dst = get_image_size(src)

    # get transformation matrix
    R = cv2.getPerspectiveTransform(src, dst)
    
    # warp image
    image = cv2.warpPerspective(image, R, (image.shape[1], image.shape[0]))
    return image

# -------- main program -------------------------
if __name__ == "__main__":
    source = 'chair_left.jpg'
    target = 'part_contour/Left_handle_cont.png'
    image = rectification(source, source)

    # cv2.imwrite("image_test.png", image)
    # cv2.imwrite("img1_test.png", image)