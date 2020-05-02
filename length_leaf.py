from leaf_area import extract_leaf, default_size
from LeafCounting.utils import load_image

def find_green_fixels(np_image):
    leaf_image, leaf_mask = extract_leaf(np_image)
    green_pixels = []
    for i in range(leaf_mask.shape[0]):
        for j in range(leaf_mask.shape[1]):
            if leaf_mask[i, j] != 0:
                green_pixels.append((i, j))
    return green_pixels

def find_centroid(np_image):
    green_pixels = find_green_fixels(np_image)
    if len(green_pixels) == 0:
        return (-1, -1)
    x = (int)(sum([pixel[0] for pixel in green_pixels])/len(green_pixels))
    y = (int)(sum([pixel[1] for pixel in green_pixels])/len(green_pixels))
    return (x, y)

import cv2
import matplotlib.pyplot as plt
def draw_centroid(np_image):
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    (cy, cx) = find_centroid(np_image)
    if cx >= 0 and cy >= 0:
        cv2.circle(gray_image, (cx, cy), 2, (255, 255, 255), -1)
        cv2.putText(gray_image, "centroid", (cx - 25, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        plt.imshow(gray_image)
    else:
        print('Invalid image!')

def find_countor(np_image):
    leaf_image, leaf_mask = extract_leaf(np_image)
    edges = cv2.Canny(leaf_mask, 100, 1200)
    edges_pixels = []
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i, j] != 0:
                edges_pixels.append((i, j))
    return edges_pixels

def calculate_max_distance(centroid, pixels, coef_x=1, coef_y=1):
    import math
    max_length = 0
    tip = ()
    for pixel in pixels:
        length = math.sqrt(coef_y*(centroid[0] - pixel[0])**2 + coef_x*(centroid[1] - pixel[1])**2)
        if length > max_length:
            max_length = length
            tip = pixel
    return max_length, tip

def calculate_max_length_leaf(np_image, coef_x=1, coef_y=1):
    contour_pixels = find_countor(np_image)
    centroid = find_centroid(np_image)
    if centroid[0] < 0 or centroid[1] < 0:
        return 0
    max_length_leaf,_ = calculate_max_distance(centroid, contour_pixels, coef_x, coef_y)
    return max_length_leaf

def draw_centroid2tip(np_image, coef_x=1, coef_y=1):
    draw_image = np_image.copy()
    contour_pixels = find_countor(np_image)
    centroid = find_centroid(np_image)
    max_length_leaf, tip = calculate_max_distance(centroid, contour_pixels, coef_x, coef_y)
    if centroid[0] >= 0 and centroid[1] >= 0:
        cv2.line(draw_image, tuple(reversed(centroid)), tuple(reversed(tip)), (0, 255, 0), 2)
        import matplotlib.pyplot as plt
        plt.imshow(draw_image)
    else:
        print('Invalid image!')

def length_leaf(filename, coef_x=1, coef_y=1):
    image = load_image(filename, default_size)
    max_length_leaf = calculate_max_length_leaf(image, coef_x, coef_y)
    return max_length_leaf

def draw_length_leaf(filename, coef_x=1, coef_y=1):
    image = load_image(filename, default_size)
    draw_centroid2tip(image, coef_x, coef_y)