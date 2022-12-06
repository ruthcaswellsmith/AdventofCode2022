from itertools import groupby
from queue import LifoQueue
from typing import List

from utils import read_file, Part


class Instruction:
    def __init__(self, text: str):
        self.split_text = text.split()

    @property
    def num_to_move(self):
        return int(self.split_text[1])

    @property
    def from_stack(self):
        return int(self.split_text[3])

    @property
    def to_stack(self):
        return int(self.split_text[5])


class SupplyStacks:
    def __init__(self, data: List[str]):
        split_data = [list(sub) for ele, sub in groupby(data, key=bool) if ele]
        self.drawing = split_data[0]
        self.instructions = [Instruction(line) for line in split_data[1]]
        self.stacks = self.__create_stacks()

    @property
    def max_height(self):
        return len(self.drawing) - 1

    @property
    def num_stacks(self):
        return len(self.drawing[self.max_height].split())

    @staticmethod
    def __get_stack_col(stack_num):
        return 4 * stack_num + 1

    def __create_stacks(self):
        stacks = [LifoQueue() for i in range(self.num_stacks)]
        for height in range(self.max_height-1, -1, -1):
            [stacks[stack].put(char) for stack in range(self.num_stacks) if
             (char := data[height][self.__get_stack_col(stack)]).isalpha()]
        return stacks

    def process_instructions(self, part: Part):
        for instruction in self.instructions:
            if part == Part.PT1:
                for crate_num in range(instruction.num_to_move):
                    crate = self.stacks[instruction.from_stack - 1].get()
                    self.stacks[instruction.to_stack - 1].put(crate)
            else:
                held_by_crane = LifoQueue()
                for crate_num in range(instruction.num_to_move):
                    held_by_crane.put(self.stacks[instruction.from_stack - 1].get())
                for crate_num in range(instruction.num_to_move):
                    self.stacks[instruction.to_stack - 1].put(held_by_crane.get())

    @property
    def answer(self):
        return "".join([self.stacks[stack_num].get() for stack_num in range(self.num_stacks)])


if __name__ == '__main__':
    filename = 'input/Day5.txt'
    data = read_file(filename)

    supply_stacks = SupplyStacks(data)
    supply_stacks.process_instructions(Part.PT1)
    print(f"The answer to part 1 is {supply_stacks.answer}")
    supply_stacks = SupplyStacks(data)
    supply_stacks.process_instructions(Part.PT2)
    print(f"The answer to part 1 is {supply_stacks.answer}")
