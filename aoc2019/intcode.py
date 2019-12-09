from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple, Union

OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LT = 7
OP_EQ = 8
OP_ADJUST_REL_BASE = 9
OP_EXIT = 99


class IllegalInstructionException(Exception):
    pass


class ExitException(Exception):
    pass


class ModeEnum(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


Flags = Tuple[ModeEnum, ModeEnum, ModeEnum]


def decode_opcode(opcode: int) -> Tuple[int, Flags]:
    op = int(opcode % 100)

    first = ModeEnum(int(opcode / 100 % 10))
    second = ModeEnum(int(opcode / 1000 % 10))
    third = ModeEnum(int(opcode / 10000 % 10))

    return op, (first, second, third)


class Program:
    def __init__(
        self,
        program: Union[List[int], Dict[int, int]],
        interactive: bool = True,
        inputs: Optional[List[int]] = None,
        return_on_input: bool = False,
    ):
        self.program: Dict[int, int] = defaultdict(
            int, enumerate(program)
        ) if isinstance(program, list) else program
        self.program_counter = 0
        self.interactive = interactive
        self.outputs = []
        self.inputs = inputs or []
        self.return_on_input = return_on_input
        self.relative_base = 0
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
                if self.return_on_input and not len(self.inputs):
                    break
                self._input(flags)
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
            elif op == OP_ADJUST_REL_BASE:
                self._adjust_rel_base(flags)
            else:
                raise IllegalInstructionException(
                    f"Illegal instruction: {op} ({flags=}, {self.program_counter=})"
                )
            op, flags = decode_opcode(self.program[self.program_counter])
        if self.return_on_input and op == OP_EXIT:
            raise ExitException()
        return self.outputs

    def _calc(self, func: Callable[[int, int], int], flags: Flags):
        a_pos = self.program_counter + 1
        b_pos = self.program_counter + 2
        dst_pos = self.program_counter + 3
        self.program_counter += 4

        self._store(
            dst_pos,
            func(self._load(a_pos, flags[0]), self._load(b_pos, flags[1])),
            flags[2],
        )

    def _adjust_rel_base(self, flags: Flags):
        self.relative_base += self._load(self.program_counter + 1, flags[0])
        self.program_counter += 2

    def _input(self, flags: Flags):
        dst_pos = self.program_counter + 1
        self._store(dst_pos, self._input_func(), flags[0])
        self.program_counter += 2

    def _output(self, flags: Flags):
        src_pos = self.program_counter + 1
        self._output_func(self._load(src_pos, flags[0]))
        self.program_counter += 2

    def _jump(self, when: bool, flags: Flags):
        test_pos = self.program_counter + 1
        dst_pos = self.program_counter + 2

        if bool(self._load(test_pos, flags[0])) is when:
            self.program_counter = self._load(dst_pos, flags[1])
        else:
            self.program_counter += 3

    def _load(self, address: int, mode: ModeEnum) -> int:
        if mode == ModeEnum.IMMEDIATE:
            return self.program[address]
        elif mode == ModeEnum.POSITION:
            return self.program[self.program[address]]
        elif mode == ModeEnum.RELATIVE:
            return self.program[self.relative_base + self.program[address]]

    def _store(self, address: int, value: int, mode: ModeEnum):
        if mode == ModeEnum.POSITION:
            dst = self.program[address]
        elif mode == ModeEnum.RELATIVE:
            dst = self.relative_base + self.program[address]
        else:
            raise IllegalInstructionException(
                f"Cannot store using address {address} in immediate mode"
            )
        self.program[dst] = value

    @classmethod
    def from_file(cls, path: str):
        with open(path, "r") as f:
            return cls([int(item) for item in f.read().split(",")])
