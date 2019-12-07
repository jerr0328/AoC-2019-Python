from itertools import permutations

from aoc2019.intcode import Program

from . import amplifiers


def main():
    master_prog = Program.from_file("data/7.txt")
    highest_output = 0
    for seq in permutations(range(5)):
        output = amplifiers(master_prog.program, seq)
        if output > highest_output:
            highest_output = output

    print(highest_output)


if __name__ == "__main__":
    main()
