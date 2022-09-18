import math
import numpy as np
import cv2 as cv
import timeit

MIN_MATCH_COUNT = 10
FLANN_INDEX_KD_TREE = 0


def get_angle_length(cam_pos, target_pos, p1_point):
    distance = math.sqrt(((cam_pos[0] - target_pos[0]) ** 2) + ((cam_pos[1] - target_pos[1]) ** 2))
    length_1 = math.sqrt(((cam_pos[0] - p1_point[0]) ** 2) + ((cam_pos[1] - p1_point[1]) ** 2))
    length_2 = math.sqrt(((p1_point[0] - target_pos[0]) ** 2) + ((p1_point[1] - target_pos[1]) ** 2))
    angle = math.degrees(math.acos((distance * distance + length_1 * length_1 - length_2 * length_2) /
                                   (2 * distance * length_1)))
    real_angle = angle + 90
    real_distance = distance * 0.28442
    # temp = round(real_distance / 5)
    # real_distance = temp * 5
    return real_distance, real_angle


def get_circle(p1, p2, p3):
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    if abs(det) < 1.0e-6:
        return None, np.inf
    # Center of circle
    cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
    # Radius of circle
    radius = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
    return (cx, cy), radius


def show(window, img):
    while True:  # Will repeatedly show the image in given window.
        cv.imshow(window, img)
        k = cv.waitKey(1) & 0xFF  # Capture the code of the pressed key.
        # Stop the loop when the user clicks on GUI close button [x].
        if not cv.getWindowProperty(window, cv.WND_PROP_VISIBLE):
            print("Operation Cancelled")
            break
        if k == 27:  # Key code for ESC
            break


def img_match(img_name, img_temp, img_template_color):
    sift = cv.SIFT_create()  # create SIFT detection
    kp, des = sift.detectAndCompute(img_name, None)
    kp_tem, des_tem = sift.detectAndCompute(img_temp, None)
    # Create FLANN match
    index_params = dict(algorithm=FLANN_INDEX_KD_TREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des, des_tem, k=2)
    #BF match
    # bf = cv.BFMatcher()
    # matches = bf.knnMatch(des, des_tem, k=2)
    good = []
    # Filter results
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_tem[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        m, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 10.0)
        matches_mask = mask.ravel().tolist()
        h, w = img_name.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        pts_ctr_x = (w - 1) / 2
        pts_ctr_y = (h - 1) / 2
        pts_ctr = np.float32([pts_ctr_x, pts_ctr_y]).reshape(-1, 1, 2)
        dst = cv.perspectiveTransform(pts, m)
        dst_ctr = cv.perspectiveTransform(pts_ctr, m)
        p1_c = [dst_ctr[0][0][0], dst_ctr[0][0][1]]
        print("Image center point: ", p1_c)
        cv.polylines(img_template_color, [np.int32(dst)], True, (0, 128, 0), 5, cv.LINE_AA)
        cv.circle(img_template_color, [np.int32(dst_ctr)[0][0][0], np.int32(dst_ctr)[0][0][1]], 5, (255, 0, 0), 5)
        return p1_c

    else:
        print("Not Enough matches are found")
        matches_mask = None
        return None
    draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None,
                       matchesMask=matches_mask, flags=2)


def run_app():
    start_1 = timeit.default_timer()
    img_template = cv.imread("photo/test.png", cv.IMREAD_GRAYSCALE)  # Read template image
    img_template = cv.resize(img_template, (0, 0), fx=1, fy=1)
    img_template_color = cv.imread("photo/test.png", cv.IMREAD_COLOR)
    img1 = cv.imread("test_images/test_1.jpg", cv.IMREAD_GRAYSCALE)  # Read first image
    img1 = cv.resize(img1, (0, 0), fx=0.5, fy=0.5)
    p1 = img_match(img1, img_template, img_template_color)
    img2 = cv.imread("test_images/test_2.jpg", cv.IMREAD_GRAYSCALE)  # Read second image
    img2 = cv.resize(img2, (0, 0), fx=0.5, fy=0.5)
    p2 = img_match(img2, img_template, img_template_color)
    img3 = cv.imread("test_images/test_3.jpg", cv.IMREAD_GRAYSCALE)  # Read third image
    img3 = cv.resize(img3, (0, 0), fx=0.5, fy=0.5)
    p3 = img_match(img3, img_template, img_template_color)
    stop_1 = timeit.default_timer()
    print('Processing Time: ', stop_1 - start_1)
    if p1 is not None and p2 is not None and p3 is not None:
        center, r = get_circle(p1, p2, p3)
        # OpenCV evaluation code, comment below if needs run
        d_1, a_1 = get_angle_length(center, [320, 900], p1)
        print("distance_1: ", d_1)
        print("angle_1: ", a_1)
    else:
        center = 0

    # -----show result----------------------------------------------------------
    print("Camera position: ", center)
    # print("Radius: ", r)
    cv.circle(img_template_color, (int(p1[0]), int(p1[1])), 5, (255, 0, 0), 5)
    cv.circle(img_template_color, (int(p2[0]), int(p2[1])), 5, (255, 0, 0), 5)
    cv.circle(img_template_color, (int(p3[0]), int(p3[1])), 5, (255, 0, 0), 5)
    cv.circle(img_template_color, (int(center[0]), int(center[1])), 5, (0, 255, 0), 5)
    # cv.circle(img_template_color, (320, 900), 5, (0, 0, 255), 5)
    show("show", img_template_color)


# Use this code to run img match script alone.
run_app()

