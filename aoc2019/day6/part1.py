from . import Orbits


def main():
    orbits = Orbits.from_file()
    print(orbits.total_orbits())


if __name__ == "__main__":
    main()
