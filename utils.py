from __future__ import annotations
from enum import Enum, auto
from typing import Tuple


def read_file(file):
    with open(file, 'r') as f:
        return f.read().rstrip('\n').split('\n')


class Part(str, Enum):
    PT1 = auto()
    PT2 = auto()


class Direction(str, Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


class XYPair:
    def __init__(self, xypair: Tuple[int, int]):
        self.x = xypair[0]
        self.y = xypair[1]

    @property
    def coordinates(self):
        return self.x, self.y

    def update(self, xypair: XYPair):
        self.x = xypair.x
        self.y = xypair.y

    def swap(self):
        temp = self.x
        self.x = self.y
        self.y = temp
        return self

    @property
    def id(self):
        return f'{self.x}-{self.y}'

    def move(self, direction: Direction):
        self.x += 1 if direction == Direction.RIGHT else -1 if direction == Direction.LEFT else 0
        self.y += 1 if direction == Direction.DOWN else -1 if direction == Direction.UP else 0

    def get_neighbor(self, direction: Direction) -> XYPair:
        return XYPair((self.x - 1, self.y)) if direction == Direction.LEFT else \
            XYPair((self.x + 1, self.y)) if direction == Direction.RIGHT else \
            XYPair((self.x, self.y - 1)) if direction == Direction.UP else \
            XYPair((self.x, self.y + 1))

    def get_inclusive_points_to(self, other: XYPair):
        if not( self.x == other.x or self.y == other.y):
            raise ValueError('Points are not vertically or horizontally aligned')
        if self.x == other.x:
            r = self.__get_inclusive_range(self.y, other.y)
            return [XYPair((self.x, y)) for y in r]
        r = self.__get_inclusive_range(self.x, other.x)
        return [XYPair((x, self.y)) for x in r]

    @staticmethod
    def __get_inclusive_range(x1: int, x2: int):
        return range(x1, x2 + 1) if x1 < x2 else range(x2, x1 + 1)

    def __sub__(self, other):
        return XYPair((self.x - other.x, self.y - other.y))

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False
