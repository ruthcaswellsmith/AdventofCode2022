from __future__ import annotations
from enum import Enum, auto
from typing import List, Tuple, TypeVar, Union
from functools import total_ordering

T = TypeVar('T')


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


class Node:
    def __init__(self, id: int, value: T):
        self.id = id
        self.value = value
        self.next = None


class CircularLinkedList:
    def __init__(self, elements: Union[str, List[T]]):
        self.nodes = [Node(i, ele) for i, ele in enumerate(elements)]
        self.head = self.nodes[0]
        self.current = self.head
        for i in range(len(self.nodes)):
            self.current.next = self.nodes[i + 1] if i < len(self.nodes) - 1 else self.head
            self.current = self.current.next

    def get_next(self):
        val = self.current.value
        self.current = self.current.next
        return val


@total_ordering
class EnhancedRange:
    def __init__(self, r: range):
        self.r = r

    def contains(self, other):
        return True if self.r[0] <= other.r[0] and self.r[-1] >= other.r[-1] else False

    def overlaps(self, other):
        rs = [self.r, other.r]
        rs.sort(key=lambda r: r[0])
        return True if rs[0][-1] >= rs[1][0] else False

    def combine(self, other):
        if not self.overlaps(other):
            raise ValueError('ranges do not overlap')
        return EnhancedRange(range(min([self.r[0], other.r[0]]), max([self.r[-1]+1, other.r[-1]+1])))

    def __lt__(self, other):
        return True if self.r[0] < other.r[0] or self.r[0] == other.r[0] and self.r[-1] < other.r[-1] else False

    def __eq__(self, other):
        return self.r[0] == other.r[0] and self.r[-1] == other.r[-1]


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

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

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
