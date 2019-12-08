import numpy as np
import pytest
from aoc2019.day8 import check_image, flatten_image, least_zeros, parse_string


@pytest.fixture
def example_img() -> np.ndarray:
    return np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]])


def test_parse_string(example_img):
    np.testing.assert_array_equal(
        example_img, parse_string("123456789012", 3, 2),
    )


def test_least_zeros(example_img):
    np.testing.assert_array_equal(example_img[0], least_zeros(example_img))


def test_check_image(example_img):
    assert 1 == check_image(example_img)


def test_flatten_image():
    img = parse_string("0222112222120000", 2, 2)
    np.testing.assert_array_equal([[0, 1], [1, 0]], flatten_image(img))
