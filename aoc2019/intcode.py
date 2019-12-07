from typing import Callable, List, Optional, Tuple

Flags = Tuple[bool, bool, bool]

OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LT = 7
OP_EQ = 8
OP_EXIT = 99


class IllegalInstruction(Exception):
    pass


def decode_opcode(opcode: int) -> Tuple[int, Flags]:
    op = int(opcode % 100)

    first = bool(int(opcode / 100 % 10))
    second = bool(int(opcode / 1000 % 10))
    third = bool(int(opcode / 10000 % 10))

    return op, (first, second, third)


class Program:
    def __init__(
        self,
        program: List[int],
        interactive: bool = True,
        inputs: Optional[List[int]] = None,
    ):
        self.program: List[int] = program
        self.program_counter = 0
        self.interactive = interactive
        self.outputs = []
        self.inputs = inputs
        if interactive:
            self._output_func = print
            self._input_func = lambda: int(input("> "))
        else:
            self._output_func = lambda x: self.outputs.append(x)
            self._input_func = lambda: self.inputs.pop(0)

    def execute(self):
        op, flags = decode_opcode(self.program[self.program_counter])
        while op != OP_EXIT:
            if op == OP_ADD:
                self._calc(lambda a, b: a + b, flags)
            elif op == OP_MUL:
                self._calc(lambda a, b: a * b, flags)
            elif op == OP_INPUT:
                self._input()
            elif op == OP_OUTPUT:
                self._output(flags)
            elif op == OP_JUMP_IF_TRUE:
                self._jump(True, flags)
            elif op == OP_JUMP_IF_FALSE:
                self._jump(False, flags)
            elif op == OP_LT:
                self._calc(lambda a, b: 1 if a < b else 0, flags)
            elif op == OP_EQ:
                self._calc(lambda a, b: 1 if a == b else 0, flags)
            else:
                raise IllegalInstruction(
                    f"Illegal instruction: {op} ({flags=}, {self.program_counter=})"
                )
            op, flags = decode_opcode(self.program[self.program_counter])
        return self.outputs

    def _calc(self, func: Callable[[int, int], int], flags: Flags):
        a_pos = self.program_counter + 1
        b_pos = self.program_counter + 2
        dst_pos = self.program_counter + 3
        self.program_counter += 4

        a = self.program[a_pos] if flags[0] else self.program[self.program[a_pos]]
        b = self.program[b_pos] if flags[1] else self.program[self.program[b_pos]]
        dst = self.program[dst_pos]
        self.program[dst] = func(a, b)

    def _input(self):
        dst_pos = self.program_counter + 1
        self.program[self.program[dst_pos]] = self._input_func()
        self.program_counter += 2

    def _output(self, flags: Flags):
        src_pos = self.program_counter + 1
        src = self.program[src_pos] if flags[0] else self.program[self.program[src_pos]]
        self._output_func(src)
        self.program_counter += 2

    def _jump(self, when: bool, flags: Flags):
        test_pos = self.program_counter + 1
        dst_pos = self.program_counter + 2

        test = (
            self.program[test_pos] if flags[0] else self.program[self.program[test_pos]]
        )
        dst = self.program[dst_pos] if flags[1] else self.program[self.program[dst_pos]]

        if bool(test) is when:
            self.program_counter = dst
        else:
            self.program_counter += 3

    @classmethod
    def from_file(cls, path: str):
        with open(path, "r") as f:
            return cls([int(item) for item in f.read().split(",")])
