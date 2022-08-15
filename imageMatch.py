import numpy as np
import cv2 as cv
import timeit
MIN_MATCH_COUNT = 10
FLANN_INDEX_KD_TREE = 0


def get_circle(p1, p2, p3):
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    if abs(det) < 1.0e-6:
        return None, np.inf
    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
    # Radius of circle
    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
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


def img_match(img_name, img_temp):
    sift = cv.SIFT_create()  # create SIFT detection
    kp, des = sift.detectAndCompute(img_name, None)
    kp_tem, des_tem = sift.detectAndCompute(img_temp, None)
    # Create FLANN match
    index_params = dict(algorithm=FLANN_INDEX_KD_TREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des, des_tem, k=2)
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
        print(p1_c)
        # cv.polylines(img_template_color, [np.int32(dst)], True, (0, 128, 0), 5, cv.LINE_AA)
        # cv.circle(img_template_color, [np.int32(dst_ctr)[0][0][0], np.int32(dst_ctr)[0][0][1]], 5, (255, 0, 0), 5)
    else:
        print("Not Enough matches are found")
        matches_mask = None
    draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None,
                       matchesMask=matches_mask, flags=2)


def run_app():
    start_1 = timeit.default_timer()
    img1 = cv.imread("img_1.png", cv.IMREAD_GRAYSCALE)  # Read first image
    img1 = cv.resize(img1, (0, 0), fx=0.5, fy=0.5)
    img2 = cv.imread("img_2.png", cv.IMREAD_GRAYSCALE)  # Read second image
    img2 = cv.resize(img2, (0, 0), fx=0.5, fy=0.5)
    img3 = cv.imread("img_2.png", cv.IMREAD_GRAYSCALE)  # Read third image
    img3 = cv.resize(img3, (0, 0), fx=0.5, fy=0.5)
    stop_1 = timeit.default_timer()
    start_2 = stop_1
    img_template = cv.imread("photo/test_template.jpeg", cv.IMREAD_GRAYSCALE)  # Read template image
    img_template_color = cv.imread("photo/test_template_dot.jpeg", cv.IMREAD_COLOR)
    img_match(img1, img_template)
    img_match(img2, img_template)
    img_match(img3, img_template)
    stop_2 = timeit.default_timer()
    print('Loading Time: ', stop_1 - start_1)
    print('Processing Time: ', stop_2 - start_2)

# Use this code to run img match script alone.
# run_app()

# img1 = cv.imread("server_img.jpg", cv.IMREAD_GRAYSCALE)
# show('sds', img1)



