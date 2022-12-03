from abc import ABC, abstractmethod
from typing import List

from utils import read_file

NUM_PER_GROUP = 3


class Base(ABC):
    CAP_DIFF = 38
    LOWER_DIFF = 96

    @property
    @abstractmethod
    def common_item_type(self):
        raise NotImplementedError

    @property
    def priority(self):
        val = ord(self.common_item_type)
        return val - self.CAP_DIFF if ord('A') <= val <= ord('Z') else val - self.LOWER_DIFF


class Rucksack(Base):
    def __init__(self, contents: str):
        self.contents = contents
        self.first_compartment = contents[0:len(contents)//2]
        self.second_compartment = contents[len(contents)//2:]

    @property
    def common_item_type(self) -> str:
        return set(self.first_compartment).intersection(set(self.second_compartment)).pop()


class Group(Base):
    def __init__(self, rucksacks: List[Rucksack]):
        self.rucksacks = rucksacks

    @property
    def common_item_type(self) -> str:
        common = set(self.rucksacks[0].contents)
        for i in range(1, NUM_PER_GROUP):
            common = common.intersection(self.rucksacks[i].contents)
        return common.pop()


if __name__ == '__main__':
    filename = 'input/day3.txt'
    data = read_file(filename)

    rucksacks = [Rucksack(line) for line in data]
    print(f"The answer to part 1 is {sum([rucksack.priority for rucksack in rucksacks])}")

    groups = [Group(r) for r in [rucksacks[num:num+NUM_PER_GROUP] for num in range(0, len(rucksacks), NUM_PER_GROUP)]]
    print(f"The answer to part 2 is {sum([group.priority for group in groups])}")
