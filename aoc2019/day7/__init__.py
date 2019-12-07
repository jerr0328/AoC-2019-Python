from typing import List, Sequence

from aoc2019.intcode import Program


def amplifiers(program: List[int], phase_seq: Sequence[int]) -> int:
    amp_input = 0
    for phase in phase_seq:
        amp_program = Program(program, interactive=False, inputs=[phase, amp_input])
        amp_output = amp_program.execute()[0]
        amp_input = amp_output
    return amp_output
