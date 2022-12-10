from enum import Enum
from typing import List, Optional

import math
from pydantic import BaseModel

from utils import read_file


class InstType(str, Enum):
    ADDX = 'addx'
    NOOP = 'noop'


class Instruction(BaseModel):
    inst_type: InstType
    value: Optional[int]

    def __init__(self, text: str):
        words = text.split()
        super().__init__(inst_type=words[0],
                         value=words[1] if len(words) == 2 else None)


class CPU:
    NOOP_CYCLES = 1
    ADDX_CYCLES = 2
    DOT = '.'
    HASH = '#'
    CRT_WIDTH = 40
    CRT_HEIGHT = 6
    CYCLES = [20, 60, 100, 140, 180, 220]

    def __init__(self, instructions: List[str]):
        self.instructions = [Instruction(line) for line in instructions]
        self.crt = []
        self.register = [1]
        self.__draw_pixel()

    @property
    def cycle(self):
        return len(self.register)

    @property
    def current_value(self):
        return self.register[-1]

    @property
    def sprite_pos(self):
        return range(self.current_value - 1, self.current_value + 2)

    def get_signal_strength(self, cycle: int):
        return cycle * self.register[cycle - 1]

    @property
    def answer_pt1(self):
        return sum([self.get_signal_strength(cycle) for cycle in self.CYCLES])

    def __get_crt_row(self, row: int):
        return "".join([self.crt[i + row * self.CRT_WIDTH] for i in range(self.CRT_WIDTH)])

    def draw_crt(self):
        [print(self.__get_crt_row(row)) for row in range(self.CRT_HEIGHT)]

    def __get_row_and_col(self, cycle):
        row = math.floor((cycle - 1) // self.CRT_WIDTH)
        mod = cycle % self.CRT_WIDTH
        col = mod - 1 if mod != 0 else self.CRT_WIDTH - 1
        return row, col

    def __draw_pixel(self):
        row, col = self.__get_row_and_col(self.cycle)
        self.crt.append(self.HASH if col in self.sprite_pos else self.DOT)

    def process_instructions(self):
        for instruction in self.instructions:
            if instruction.inst_type == InstType.NOOP:
                for _ in range(self.NOOP_CYCLES):
                    self.register.append(self.current_value)
                    self.__draw_pixel()
            else:
                for i in range(self.ADDX_CYCLES):
                    self.register.append(self.current_value if i < self.ADDX_CYCLES - 1 else
                                         self.current_value + instruction.value)
                    self.__draw_pixel()


if __name__ == '__main__':
    filename = 'input/day10.txt'
    data = read_file(filename)

    cpu = CPU(data)
    cpu.process_instructions()
    print(f"The answer to Pt 1 is {cpu.answer_pt1}")

    print(f"\nThe answer to Pt 2 is:")
    cpu.draw_crt()
