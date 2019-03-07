"""Utils to handle data files."""
import os

import numpy as np
import pandas as pd

import cv2


def read_csv(fn)->np.array:
    return np.array(pd.read_csv(fn, dtype=np.int))


def save_csv(data, fn, cols):
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(fn, index=False)


def resize_image(src, dest, sizes=[224, 224]):
    """Resize fashion image.

    Resize rule: dilate the original image to square with all 0 filled.
    Cause all fashion image are with white background
    Then resize the image to given sizes [new_height, new_width]
    """
    img = cv2.imread(src)
    height, width, depth = img.shape
    ratio = 1.0 * height / width
    new_height = sizes[0]
    new_width = sizes[1]
    new_ratio = 1.0 * new_height / new_width
    if ratio > new_ratio:
        h = height
        w = int(height / new_ratio)
        new_image = np.zeros((h, w, depth)).astype(np.uint8)
        new_image[:] = 255
        new_p = int((w - width) / 2)
        new_image[:, new_p:new_p + width, :] = img
    else:
        h = int(new_ratio * height)
        w = width
        new_image = np.zeros((h, w, depth)).astype(np.uint8)
        new_image[:] = 255
        new_p = int((h - height) / 2)
        new_image[new_p:new_p + height, :, :] = img
    resized_img = cv2.resize(new_image, (new_width, new_height))
    cv2.imwrite(dest, resized_img)
