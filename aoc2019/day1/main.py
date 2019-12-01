from . import calculate_fuel_with_fuel_mass


def main():
    print("Start")
    with open("data/1.txt") as f:
        fuel = sum(map(calculate_fuel_with_fuel_mass, (int(line) for line in f)))
    print(f"Fuel needed: {fuel}")


if __name__ == "__main__":
    main()
