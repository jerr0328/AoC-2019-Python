def calculate_fuel(mass: int) -> int:
    return int(mass / 3) - 2


def calculate_fuel_with_fuel_mass(mass: int) -> int:
    total_fuel = calculate_fuel(mass)
    extra_fuel = calculate_fuel(total_fuel)

    while extra_fuel > 0:
        total_fuel += extra_fuel
        extra_fuel = calculate_fuel(extra_fuel)

    return total_fuel
