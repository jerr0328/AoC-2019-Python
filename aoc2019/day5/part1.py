from aoc2019.intcode import Program


def main():
    prog = Program.from_file("data/5.txt")
    prog.execute()


if __name__ == "__main__":
    main()