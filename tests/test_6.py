from aoc2019.day6 import Orbits


def test_orbits():
    orbits_raw = {
        "B": "COM",
        "C": "B",
        "D": "C",
        "E": "D",
        "F": "E",
        "G": "B",
        "H": "G",
        "I": "D",
        "J": "E",
        "K": "J",
        "L": "K",
    }

    orbits = Orbits(orbits_raw)
    assert 42 == orbits.total_orbits()


def test_transfers_needed():
    orbits_raw = {
        "B": "COM",
        "C": "B",
        "D": "C",
        "E": "D",
        "F": "E",
        "G": "B",
        "H": "G",
        "I": "D",
        "J": "E",
        "K": "J",
        "L": "K",
        "YOU": "K",
        "SAN": "I",
    }

    orbits = Orbits(orbits_raw)
    assert 4 == orbits.transfers_needed("YOU", "SAN")
