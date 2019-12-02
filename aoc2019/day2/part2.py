from itertools import product

from . import Program


def main():
    target = 19690720
    orig_prog = Program.from_file("data/2.txt")
    for noun, verb in product(range(100), range(100)):
        test_prog = Program(orig_prog.program.copy())
        test_prog.program[1] = noun
        test_prog.program[2] = verb
        test_prog.execute()
        if target == test_prog.program[0]:
            print(f"{noun=}, {verb=}, solution: {(100 * noun) + verb}")
            break


if __name__ == "__main__":
    main()
