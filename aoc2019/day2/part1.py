from . import Program


def main():
    prog = Program.from_file("data/2.txt")
    prog.execute()
    print(prog.program[0])


if __name__ == "__main__":
    main()
