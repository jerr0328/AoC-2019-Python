import pytest
from aoc2019.day1 import calculate_fuel, calculate_fuel_with_fuel_mass


@pytest.mark.parametrize(
    "mass,expected", [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
)
def test_calculate_fuel(mass, expected):
    assert expected == calculate_fuel(mass)


@pytest.mark.parametrize("mass,expected", [(14, 2), (1969, 966), (100756, 50346)])
def test_calculate_fuel_with_fuel_mass(mass, expected):
    assert expected == calculate_fuel_with_fuel_mass(mass)
