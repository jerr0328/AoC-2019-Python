from typing import List, Tuple

import pytest
from aoc2019.intcode import ExitException, Program, decode_opcode

CMP_8_PROG = [
    3,
    21,
    1008,
    21,
    8,
    20,
    1005,
    20,
    22,
    107,
    8,
    21,
    20,
    1006,
    20,
    31,
    1106,
    0,
    36,
    98,
    0,
    0,
    1002,
    21,
    125,
    20,
    4,
    20,
    1105,
    1,
    46,
    104,
    999,
    1105,
    1,
    46,
    1101,
    1000,
    1,
    20,
    4,
    20,
    1105,
    1,
    46,
    98,
    99,
]


@pytest.mark.parametrize(
    "given,expected",
    [
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        ),
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
        ([1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99]),
    ],
)
def test_program(given: List[int], expected):
    prog = Program(given)
    prog.execute()
    assert expected == prog.program


@pytest.mark.parametrize(
    "opcode,expected",
    [
        (1102, (2, (True, True, False))),
        (1001, (1, (False, True, False))),
        (2, (2, (False, False, False))),
    ],
)
def test_decode_opcode(opcode: int, expected: Tuple[int, Tuple[bool, bool, bool]]):
    assert expected == decode_opcode(opcode)


def test_interactive_input_output(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "123")
    prog = Program([3, 0, 4, 0, 99], interactive=True)
    prog.execute()
    assert [123, 0, 4, 0, 99] == prog.program
    captured = capsys.readouterr()
    assert "123\n" == captured.out


@pytest.mark.parametrize(
    "program,given,expected",
    [
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 5, 1),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], -1, 1),
        (CMP_8_PROG, 5, 999),
        (CMP_8_PROG, 8, 1000),
        (CMP_8_PROG, 10, 1001),
    ],
)
def test_non_interactive_mode(program, given, expected):
    prog = Program(program, interactive=False, inputs=[given])
    assert [expected] == prog.execute()


def test_input_blocks():
    input_prog = [3, 0, 4, 0, 99]
    prog = Program(input_prog, interactive=False, return_on_input=True)
    prog.execute()
    assert input_prog == prog.program
    assert [] == prog.outputs
    prog.inputs.append(7)
    with pytest.raises(ExitException):
        prog.execute()
    assert [7] == prog.outputs
