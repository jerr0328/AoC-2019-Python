from typing import List

OP_ADD = 1
OP_MUL = 2
OP_EXIT = 99
PC_INCR = 4


class Program:
    def __init__(self, program: List[int]):
        self.program: List[int] = program

    def execute(self):
        program_counter = 0
        opcode = self.program[program_counter]
        while opcode != OP_EXIT:
            if opcode == OP_ADD:
                self._add(program_counter)
            elif opcode == OP_MUL:
                self._mul(program_counter)
            else:
                break
            program_counter += PC_INCR
            opcode = self.program[program_counter]

    def _add(self, program_counter: int):
        self.program[self.program[program_counter + 3]] = (
            self.program[self.program[program_counter + 1]]
            + self.program[self.program[program_counter + 2]]
        )

    def _mul(self, program_counter: int):
        self.program[self.program[program_counter + 3]] = (
            self.program[self.program[program_counter + 1]]
            * self.program[self.program[program_counter + 2]]
        )

    @classmethod
    def from_file(cls, path: str):
        with open(path, "r") as f:
            return cls([int(item) for item in f.read().split(",") if item.isdigit()])
