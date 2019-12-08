from itertools import product

import numpy as np


def least_zeros(img: np.ndarray) -> np.ndarray:
    lowest_zero_layer = 0
    max_nonzero_count = 0
    nonzeros = np.count_nonzero(img, axis=2)
    for layer_num, layer in enumerate(nonzeros):
        layer_nonzeros = np.sum(layer)
        if layer_nonzeros > max_nonzero_count:
            lowest_zero_layer = layer_num
            max_nonzero_count = layer_nonzeros
    return img[lowest_zero_layer]


def parse_string(img: str, width: int, height: int) -> np.ndarray:
    return np.reshape([int(i) for i in img], (-1, height, width))


def check_image(img: np.ndarray) -> int:
    least_zero_layer = least_zeros(img)
    return np.count_nonzero(least_zero_layer == 1) * np.count_nonzero(
        least_zero_layer == 2
    )


def flatten_image(img: np.ndarray) -> np.ndarray:
    flattened = np.copy(img[0])
    height, width = flattened.shape
    for layer in img[1:]:
        # break once no more transparent pixels
        if np.count_nonzero(flattened == 2) == 0:
            break
        for row, col in product(range(height), range(width)):
            if flattened[row][col] == 2:
                flattened[row][col] = layer[row][col]

    return flattened
