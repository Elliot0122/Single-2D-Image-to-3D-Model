import cv2
import os
import numpy as np

def ref_point_of_original_image(left_source):
    left_handle = cv2.imread(left_source)
    left_handle_gary = cv2.cvtColor(left_handle, cv2.COLOR_BGR2GRAY)
    l_cont = np.array(np.where(left_handle_gary == 255))

    # left_top -> right_top -> right_bottom -> left bottom
    reference_points = np.zeros((4, 2), np.float32)

    diff_s = 0
    for i in l_cont.T:
        # y = x + n maximum
        if i[0]>= diff_s:
            diff_s = i[0]
            reference_points[3] = i
    diff_s = 0
    diff_b = 10000000
    thickness = 0
    for i in l_cont.T:
        # y = x + n maximum
        if i[0] + 3*i[1] >= diff_s:
            diff_s = i[0] + 3*i[1]
            reference_points[2] = i
        # y = -x + n minimum
        if i[0] - i[1] <= diff_b:
            diff_b = i[0] - i[1]
            reference_points[1] = i
        if reference_points[3][1] - i[1] > thickness:
            thickness = reference_points[3][1] - i[1]

    reference_points[0] = reference_points[1] + reference_points[3] - reference_points[2]

    # for i in reference_points:
    #     left_handle[int(i[0])][int(i[1])] = [0, 0, 255]
    # left_handle[int(reference_points[3][0])][int(reference_points[3][1])] = [0, 255, 0]
    # cv2.imwrite(f"test.png", left_handle)

    for i in reference_points:
        i[0], i[1] = i[1], i[0]

    return reference_points, thickness

def run_rectification(source, whole_length, whole_height):
    left_source = os.path.join(source,'part_contour/left_handle_irregular.png')
    left_image = os.path.join(source,'parts/left_handle_irregular.png')
    image = cv2.imread(left_image)

    src, thickness = ref_point_of_original_image(left_source)
    dst = np.array([
        [0, 0],
        [whole_length, 0],
        [whole_length, whole_height],
        [0, whole_height]], np.float32)
    H = cv2.getPerspectiveTransform(src, dst)
    R = np.linalg.inv(H)
    offset = np.full((3, 1),1)
    offset = np.dot(R, offset)
    newimage = np.full((image.shape[0]+int(offset[0]), image.shape[1]+int(offset[1]), 3), 255, np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            newimage[i+int(offset[0])][j+int(offset[1])] = image[i][j]

    border_up_left = np.full((3,1), 1)
    border_lower_right = np.zeros((3,1))
    border_lower_right[0] = newimage.shape[0]
    border_lower_right[1] = newimage.shape[1]
    border_up_left = np.dot(H, border_up_left)
    border_lower_right = np.dot(H, border_lower_right)

    dst = cv2.warpPerspective(newimage, H, (int(border_lower_right[0]), int(border_lower_right[1])), cv2.INTER_LINEAR)

    final_image = np.full((dst.shape[0], dst.shape[1], 3), 255, np.uint8)
    for i in range(dst.shape[0]):
        for j in range(dst.shape[1]):
            if (dst[i][j] == [230, 2, 10]).all():
                final_image[i][j] = [230, 2, 10]

    cv2.imwrite(os.path.join(source,'parts/Left_handle_irregular_rected.png'), final_image)
    return thickness

# -------- main program -------------------------
if __name__ == "__main__":
    source = 'chairs\\51-1'
    # thickness = run_rectification(source)