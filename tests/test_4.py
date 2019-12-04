import pytest
from aoc2019.day4 import valid_password


@pytest.mark.parametrize(
    "password,expected",
    [(122345, True), (111123, True), (111111, True), (223450, False), (123789, False)],
)
def test_valid_password(password, expected):
    assert expected == valid_password(password)
