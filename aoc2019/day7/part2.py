from itertools import permutations

from aoc2019.intcode import Program

from . import feedback_amps


def main():
    master_prog = Program.from_file("data/7.txt")
    highest_output = 0
    for seq in permutations(range(5, 10)):
        output = feedback_amps(master_prog.program, seq)
        if output > highest_output:
            highest_output = output

    print(highest_output)


if __name__ == "__main__":
    main()
