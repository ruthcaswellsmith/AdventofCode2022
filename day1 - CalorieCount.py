from typing import List
from itertools import groupby
from pydantic import BaseModel
from utils import read_file


class Elf(BaseModel):
    items: List[int] = []

    @property
    def total_calories(self):
        return sum(self.items)


if __name__ == '__main__':
    filename = 'input/day1.txt'
    data = read_file(filename)

    elves = [Elf(items=list(group)) for not_blank, group in groupby(data, key=bool) if not_blank]
    sorted_calorie_counts = sorted([elf.total_calories for elf in elves], reverse=True)

    print(f"The answer to part 1 is {sorted_calorie_counts[0]}")
    print(f"The answer to part 2 is {sum(sorted_calorie_counts[:3])}")
