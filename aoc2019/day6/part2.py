from . import Orbits


def main():
    orbits = Orbits.from_file()
    print(orbits.transfers_needed("YOU", "SAN"))


if __name__ == "__main__":
    main()
