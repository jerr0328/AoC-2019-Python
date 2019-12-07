from typing import List, Sequence

from aoc2019.intcode import ExitException, Program


def amplifiers(program: List[int], phase_seq: Sequence[int]) -> int:
    amp_input = 0
    for phase in phase_seq:
        amp_program = Program(
            program.copy(), interactive=False, inputs=[phase, amp_input]
        )
        amp_output = amp_program.execute()[0]
        amp_input = amp_output
    return amp_output


def feedback_amps(program: List[int], phase_seq: Sequence[int]) -> int:
    amps = [
        Program(program.copy(), interactive=False, return_on_input=True, inputs=[phase])
        for phase in phase_seq
    ]
    amp_input = 0
    loop_count = 0
    feedback = True
    while feedback:
        loop_count += 1
        for amp in amps:
            if amp_input is not None:
                amp.inputs.append(amp_input)
            try:
                amp.execute()
            except ExitException:
                feedback = False
            if amp.outputs:
                amp_output = amp.outputs.pop()
                amp_input = amp_output
            else:
                amp_input = None
    return amp_output
