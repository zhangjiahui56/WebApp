from leaf_area import extract_leaf, default_size
from LeafCounting.utils import load_image
import math
import numpy as np

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

def find_contours(np_image):
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
    max_point = ()
    for pixel in pixels:
        length = math.sqrt(coef_y*(centroid[0] - pixel[0])**2 + coef_x*(centroid[1] - pixel[1])**2)
        if length > max_length:
            max_length = length
            max_point = pixel
    return max_length, max_point

def calculate_max_length_leaf(np_image, coef_x=1, coef_y=1):
    contour_pixels = find_contours(np_image)
    centroid = find_centroid(np_image)
    if centroid[0] < 0 or centroid[1] < 0:
        return 0
    max_length_leaf,_ = calculate_max_distance(centroid, contour_pixels, coef_x, coef_y)
    return max_length_leaf

def draw_centroid2tip(np_image, coef_x=1, coef_y=1):
    draw_image = np_image.copy()
    contour_pixels = find_contours(np_image)
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


"""
the code for calculate average of length leaves, more complicated than max length
this function calculate the length of each of leaf and take average of their lengths
by using Chebyshev noise filter
"""

MIN_CONTOUR_PIXELS = 20

def find_external_contours(np_image):
    leaf_image, leaf_mask = extract_leaf(np_image)
    ret, thresh = cv2.threshold(leaf_mask, 100, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def find_good_contours(contours, threshold):
    new_contours = []
    for i in range(len(contours)):
        if len(contours[i]) >= threshold:
            new_contours.append(contours[i])

    return new_contours

def find_next(f, xs, i):
    return f(i+1)

def find_prev(f, xs, i):
    return f(i-1)

def find_extreme(f, xs):
    extreme_values = []
    extreme_xs = []
    for i in range(len(xs)):
        if f(i) > find_prev(f, xs, i) and f(i) > find_next(f, xs, i):
            extreme_values.append(f(i))
            extreme_xs.append(i)
    return extreme_values, extreme_xs

def choose_deg(length):
    return math.ceil(len(length)/100) * 10

def padding_length(ls, x):
    if x > len(ls):
        return ls
    else:
        return ls[-x:] + ls + ls[:x]


def padding_idx(ls, x):
    if x > len(ls):
        return ls
    else:
        return [i for i in range(-x, 0, 1)] + ls + [len(ls)+i for i in range(x)]


def calculate_average_length_leaf(np_image, coef_x=1, coef_y=1):
    leaf_image, leaf_mask = extract_leaf(np_image)
    centroid = find_centroid(np_image)
    contours = find_external_contours(np_image)
    contours = find_good_contours(contours, MIN_CONTOUR_PIXELS)

    lengths = []
    for contour in contours:
        lengths_of_contour = []
        for pixel in contour:
            point = tuple(pixel[0])
            length = math.sqrt((coef_x * (centroid[1] - point[0])) ** 2 + (coef_y * (centroid[0] - point[1])) ** 2)
            lengths_of_contour.append(length)
        lengths.append(lengths_of_contour)

    length_leaves = []
    for length in lengths:
        idx = [i for i in range(len(length))]
        f = np.polynomial.chebyshev.Chebyshev.fit(padding_idx(idx, len(idx) // 2),
                                                  padding_length(length, len(length) // 2), choose_deg(length))
        value, locate = find_extreme(f, idx)
        length_leaves += [length[i] for i in locate]

    if len(length_leaves) == 0:
        return 0

    length_average = sum(length_leaves) / len(length_leaves)
    return length_average

def draw_redlines(np_image, locates):
    draw_image = np_image.copy()
    for locate in locates:
        cv2.circle(draw_image, locate, 2, (255,0,0), -1)

    plt.imshow(draw_image)

def get_tip_locates(locates, contours):
    tip_locates = []

    if len(locates) != len(contours):
        return tip_locates

    for i in range(len(locates)):
        for lc in locates[i]:
            tip_locates.append(tuple(contours[i][lc][0]))
    return tip_locates


def draw_tip_leaf(np_image, coef_x=1, coef_y=1):
    leaf_image, leaf_mask = extract_leaf(np_image)
    centroid = find_centroid(np_image)
    contours = find_external_contours(np_image)
    contours = find_good_contours(contours, MIN_CONTOUR_PIXELS)

    lengths = []
    for contour in contours:
        lengths_of_contour = []
        for pixel in contour:
            point = tuple(pixel[0])
            length = math.sqrt((coef_x * (centroid[1] - point[0])) ** 2 + (coef_y * (centroid[0] - point[1])) ** 2)
            lengths_of_contour.append(length)
        lengths.append(lengths_of_contour)

    length_leaves = []
    locates = []
    for length in lengths:
        idx = [i for i in range(len(length))]
        f = np.polynomial.chebyshev.Chebyshev.fit(padding_idx(idx, len(idx) // 2),
                                                  padding_length(length, len(length) // 2), choose_deg(length))
        value, locate = find_extreme(f, idx)
        length_leaves += [length[i] for i in locate]
        locates.append(locate)

    length_average = sum(length_leaves) / len(length_leaves)

    tip_locates = get_tip_locates(locates, contours)
    draw_redlines(np_image, tip_locates)