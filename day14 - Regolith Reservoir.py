from __future__ import annotations
from enum import Enum
from typing import List, Union
import numpy as np
import pandas as pd

from utils import read_file, XYPair, Part

SIZE = 1000
DELIMITER = ' -> '


class Occupant(str, Enum):
    ROCK = 8
    SAND = 0


class Sand:
    def __init__(self, xypair: XYPair):
        self.pos = xypair

    def __get_occupants(self, grid: np.array):
        return [grid[self.pos.x+1, y] for y in range(self.pos.y-1, self.pos.y+2)]

    def is_blocked(self, grid: np.array) -> bool:
        occupants = self.__get_occupants(grid)
        return sum([pd.isna(occupant) for occupant in occupants]) == 0

    def get_new_pos(self, grid: np.array) -> Union[None, XYPair]:
        options = [XYPair((self.pos.x+1, y)) for y in range(self.pos.y-1, self.pos.y+2)]
        occupants = self.__get_occupants(grid)
        return options[1] if pd.isna(occupants[1]) else \
            options[0] if pd.isna(occupants[0]) else \
            options[2] if pd.isna(occupants[2]) else \
            None


class Reservoir:
    def __init__(self, data: List[str], part: Part):
        self.part = part
        self.data = data
        self.sand = Sand(XYPair((0, 500)))
        self.segments = self.__get_segments()
        self.max_depth = max([segment[0].x for segment in self.segments])
        if part == Part.PT2:
            self.segments.append((XYPair((self.max_depth + 2, 0)),
                                  XYPair((self.max_depth + 2, SIZE - 1))))
            self.max_depth += 2
        self.grid = np.nan*np.zeros((self.max_depth + 1, SIZE))
        self.__add_rocks()

    @property
    def answer(self):
        if self.part == Part.PT1:
            return np.count_nonzero(self.grid == 0) - 1
        else:
            return np.count_nonzero(self.grid == 0) + 1

    def process(self):
        falling_into_abyss = False
        self.sand = Sand(XYPair((0, 500)))
        while not falling_into_abyss and not self.sand.is_blocked(self.grid):
            falling_into_abyss = self.fall()
            self.sand = Sand(XYPair((0, 500)))

    def fall(self):
        new_pos = self.sand.get_new_pos(self.grid)
        while new_pos and self.sand.pos.x < self.max_depth - 1:
            self.sand.pos.update(new_pos)
            new_pos = self.sand.get_new_pos(self.grid)
        self.grid[self.sand.pos.x, self.sand.pos.y] = Occupant.SAND
        return True if new_pos else False

    def __add_rocks(self):
        for segment in self.segments:
            rocks = segment[0].get_inclusive_points_to(segment[1])
            for rock in rocks:
                self.grid[rock.x, rock.y] = Occupant.ROCK

    def __get_segments(self):
        segments = []
        for line in self.data:
            points = [XYPair(eval(point)).swap() for point in line.split(DELIMITER)]
            segments.extend([(points[i], points[i+1]) for i in range(len(points)-1)])
        return segments


if __name__ == '__main__':
    filename = 'input/day14.txt'
    data = read_file(filename)

    reservoir = Reservoir(data, Part.PT1)
    reservoir.process()
    print(f"The answer to Pt 1 is {reservoir.answer}")

    reservoir = Reservoir(data, Part.PT2)
    reservoir.process()
    print(f"The answer to Pt 2 is {reservoir.answer}")
