from typing import List, Tuple

Flags = Tuple[bool, bool, bool]

OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_EXIT = 99
PC_INCR = 4


class IllegalInstruction(Exception):
    pass


def decode_opcode(opcode: int) -> Tuple[int, Flags]:
    op = int(opcode % 100)

    first = bool(int(opcode / 100 % 10))
    second = bool(int(opcode / 1000 % 10))
    third = bool(int(opcode / 10000 % 10))

    return op, (first, second, third)


class Program:
    def __init__(self, program: List[int]):
        self.program: List[int] = program
        self.program_counter = 0

    def execute(self):
        op, flags = decode_opcode(self.program[self.program_counter])
        while op != OP_EXIT:
            if op == OP_ADD:
                self._add(flags)
            elif op == OP_MUL:
                self._mul(flags)
            elif op == OP_INPUT:
                self._input()
            elif op == OP_OUTPUT:
                self._output(flags)
            else:
                raise IllegalInstruction(
                    f"Illegal instruction: {op} ({flags=}, {self.program_counter=})"
                )
            op, flags = decode_opcode(self.program[self.program_counter])

    def _add(self, flags: Flags):
        a_pos = self.program_counter + 1
        b_pos = self.program_counter + 2
        dst_pos = self.program_counter + 3
        self.program_counter += 4

        a = self.program[a_pos] if flags[0] else self.program[self.program[a_pos]]
        b = self.program[b_pos] if flags[1] else self.program[self.program[b_pos]]
        dst = self.program[dst_pos]
        self.program[dst] = a + b

    def _mul(self, flags: Flags):
        a_pos = self.program_counter + 1
        b_pos = self.program_counter + 2
        dst_pos = self.program_counter + 3
        self.program_counter += 4

        a = self.program[a_pos] if flags[0] else self.program[self.program[a_pos]]
        b = self.program[b_pos] if flags[1] else self.program[self.program[b_pos]]
        dst = self.program[dst_pos]
        self.program[dst] = a * b

    def _input(self):
        dst_pos = self.program_counter + 1
        self.program[self.program[dst_pos]] = int(input("> "))
        self.program_counter += 2

    def _output(self, flags):
        src_pos = self.program_counter + 1
        src = self.program[src_pos] if flags[0] else self.program[self.program[src_pos]]
        print(src)
        self.program_counter += 2

    @classmethod
    def from_file(cls, path: str):
        with open(path, "r") as f:
            return cls([int(item) for item in f.read().split(",")])
