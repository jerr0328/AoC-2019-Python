from typing import List, Tuple

import pytest
from aoc2019.intcode import Program, decode_opcode


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


def test_simple_input_output(capsys, monkeypatch):
    with monkeypatch.context() as m:
        m.setattr("builtins.input", lambda _: "123")
        prog = Program([3, 0, 4, 0, 99])
        prog.execute()
        assert [123, 0, 4, 0, 99] == prog.program
        captured = capsys.readouterr()
        assert "123\n" == captured.out
