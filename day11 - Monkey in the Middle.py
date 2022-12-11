import numpy as np
from enum import Enum
from typing import List, Union
from queue import Queue
from math import floor

from pydantic import BaseModel

from utils import read_file


class Symbol(str, Enum):
    TIMES = '*'
    PLUS = '+'


class OldEnum(str, Enum):
    OLD = 'old'


class Operation(BaseModel):
    second_arg: Union[OldEnum, int]
    symbol: Symbol

    def __init__(self, text: str):
        words = text.split()
        super().__init__(second_arg=words[5], symbol=words[4])


class Item(BaseModel):
    worry_level: int

    def adjust_worry_level(self, operation: Operation):
        if operation.symbol == Symbol.PLUS:
            if operation.second_arg == OldEnum.OLD:
                self.worry_level *= 2
            else:
                self.worry_level += operation.second_arg
        else:
            if operation.second_arg == OldEnum.OLD:
                self.worry_level **= 2
            else:
                self.worry_level *= operation.second_arg


class Test(BaseModel):
    divisible_by: int
    true_monkey: int
    false_monkey: int

    def __init__(self, lines: List[str]):
        words = lines[0].split()
        tm, fm = lines[1].split()[5], lines[2].split()[5]
        super().__init__(divisible_by=words[3], true_monkey=tm, false_monkey=fm)


class Monkey(BaseModel):
    worry_level_divisor: int
    items: Queue
    operation: Operation
    test: Test
    inspected: int = 0

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, lines: List[str], worry_level_divisor: int):
        queue = Queue()
        [queue.put(Item(worry_level=wl)) for wl in lines[0].split(':')[1].split(',')]
        oper = Operation(text=lines[1])
        test = Test(lines=lines[2:5])
        super().__init__(worry_level_divisor=worry_level_divisor, items=queue, operation=oper, test=test)

    @property
    def worry_levels(self):
        return [self.items.queue[i] for i in range(self.items.qsize())]

    def play_with_item(self, cycle_number: int):
        self.inspected += 1
        item = self.items.get()
        item.adjust_worry_level(self.operation)
        if self.worry_level_divisor > 1:
            item.worry_level //= self.worry_level_divisor
        else:
            num_cycles = floor(item.worry_level/cycle_number)
            item.worry_level -= num_cycles * cycle_number
        target_monkey = self.test.true_monkey if self.__test(item.worry_level) else \
            self.test.false_monkey
        return target_monkey, item

    def __test(self, worry_level: int):
        return True if worry_level % self.test.divisible_by == 0 else False


class MonkeyInTheMiddle:
    LINES_PER = 7

    def __init__(self, lines: List[str], worry_level_divisor: int):
        self.num_monkeys = (len(lines) + 1)//self.LINES_PER
        self.monkeys = [Monkey(lines[self.LINES_PER*i+1:self.LINES_PER*i+self.LINES_PER-1],
                               worry_level_divisor) for
                        i in range(self.num_monkeys)]
        self.cycle_number = int(np.prod([m.test.divisible_by for m in self.monkeys]))

    @property
    def answer_pt1(self):
        return np.prod(sorted(self.monkey_activity, reverse=True)[:2])

    @property
    def monkey_activity(self):
        return [m.inspected for m in self.monkeys]

    def play_rounds(self, rounds: int):
        for i in range(rounds):
            self.play_round()

    def play_round(self):
        for num, monkey in enumerate(self.monkeys):
            while monkey.items.qsize() > 0:
                target_monkey, item = monkey.play_with_item(self.cycle_number)
                self.monkeys[target_monkey].items.put(item)


if __name__ == '__main__':
    filename = 'input/day11.txt'
    data = read_file(filename)

    monkey_in_the_middle = MonkeyInTheMiddle(data, worry_level_divisor=3)
    monkey_in_the_middle.play_rounds(rounds=20)
    print(f"The answer to Pt 1 is {monkey_in_the_middle.answer_pt1}")

    monkey_in_the_middle = MonkeyInTheMiddle(data, worry_level_divisor=1)
    monkey_in_the_middle.play_rounds(rounds=10_000)
    print(f"The answer to Pt 1 is {monkey_in_the_middle.answer_pt1}")
