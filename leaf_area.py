import numpy as np
import cv2
from PIL import Image,ImageOps

# boundaries for green color
boundaries = [
    ([33, 80, 40], [105, 255, 255])
]

(lower, upper) = boundaries[0]
lower = np.array(lower, dtype="uint8")
upper = np.array(upper, dtype="uint8")

def remove_noises_mask(mask):
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    mask = cv2.erode(mask, element, iterations=1)
    mask = cv2.dilate(mask, element, iterations=1)
    mask = cv2.erode(mask, element)
    return mask

def extract_leaf(np_image):
    hsvIm = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvIm, lower, upper)
    mask = remove_noises_mask(mask)
    output = cv2.bitwise_and(hsvIm, hsvIm, mask=mask)

    return output, mask

from LeafCounting.utils import load_image
default_size = (240, 240)

def calculate_green_pixel(np_mask):
    green_pixel = 0
    for i in range(np_mask.shape[0]):
        for j in range(np_mask.shape[1]):
            if np_mask[i, j] != 0:
                green_pixel += 1
    return green_pixel

def calculate_leaf_area(filename, coef = 1):
    image = load_image(filename, default_size)
    output_image, output_mask = extract_leaf(image)

    green_pixel = calculate_green_pixel(output_mask)

    area = green_pixel / (default_size[0] * default_size[1]) * coef
    return area
