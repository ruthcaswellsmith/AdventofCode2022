from __future__ import annotations

import numpy as np
from typing import List, Tuple
from itertools import product
from utils import read_file, Part, XYPair, MapDirection, CircularLinkedList

SIZE = 1000
ELF = 8
NORTH = 1000
SOUTH = 2000
WEST = 3000
EAST = 4000
EMPTY = 6000

MOVING_ELF_VALUES = {
    MapDirection.NORTH: SOUTH,
    MapDirection.SOUTH: NORTH,
    MapDirection.WEST: EAST,
    MapDirection.EAST: WEST
}


class Spot(XYPair):
    def __init__(self, coordinates: Tuple[int, int]):
        super().__init__(coordinates)

    def get_neighboring_coordinates(self, dir: MapDirection):
        return Spot((self.x-1, self.y)) if dir == MapDirection.NORTH else\
            Spot((self.x+1, self.y)) if dir == MapDirection.SOUTH else \
            Spot((self.x, self.y-1)) if dir == MapDirection.WEST else \
            Spot((self.x, self.y+1))


class Grove:
    def __init__(self, data: List[str], part: Part):
        self.part = part
        self.grid = EMPTY * np.ones((SIZE, SIZE), dtype=int)
        self.offset = SIZE // 2
        self.origin = Spot((self.offset, self.offset))
        for i, line in enumerate(data):
            for j, c in enumerate(line):
                self.__set_grid(i, j, EMPTY if c == '.' else ELF)
        self.directions = CircularLinkedList([MapDirection.NORTH,
                                              MapDirection.SOUTH,
                                              MapDirection.WEST,
                                              MapDirection.EAST])
        self.first_halves: List[np.array] = []
        self.second_halves: List[np.array] = []

    @property
    def rectangle(self):
        elves = np.nonzero(self.grid == ELF)
        xmin, xmax = min(elves[0]), max(elves[0])
        ymin, ymax = min(elves[1]), max(elves[1])
        return self.grid[xmin:xmax+1, ymin:ymax+1]

    @property
    def answer(self):
        return np.count_nonzero(self.rectangle == 6000)

    @staticmethod
    def nan_equal(a, b):
        try:
            np.testing.assert_equal(a, b)
        except AssertionError:
            return False
        return True

    def process(self, num: int = None):
        if self.part == Part.PT1:
            for _ in range(num):
                directions = [self.directions.get_next() for _ in range(4)]
                first_half = self.first_half(directions)
                self.first_halves.append(first_half)
                self.second_half(first_half)
                self.second_halves.append(self.grid)
                self.directions.head = self.directions.head.next
                self.directions.current = self.directions.head
            return None
        else:
            done = False
            rounds = 0
            while not done:
                directions = [self.directions.get_next() for _ in range(4)]
                first_half = self.first_half(directions)
                self.first_halves.append(first_half)
                self.second_half(first_half)
                self.second_halves.append(self.grid.copy())
                self.directions.head = self.directions.head.next
                self.directions.current = self.directions.head
                rounds += 1
                if len(self.second_halves) > 1:
                    if np.array_equal(self.second_halves[-1], self.second_halves[-2]):
                        done = True
            return rounds

    def first_half(self, directions: List[MapDirection]):
        elves = np.nonzero(self.grid == ELF)
        first_half = EMPTY * np.zeros(self.grid.shape)
        for i in range(len(elves[0])):
            elf = Spot((elves[0][i], elves[1][i]))
            if not self.__stay_put(elf):
                dir_to_move = self.__dir_to_move(elf, directions)
                if dir_to_move:
                    spot_to_move = elf.get_neighboring_coordinates(dir_to_move)
                    first_half[elf.x, elf.y] = NORTH if dir_to_move == MapDirection.NORTH else\
                        SOUTH if dir_to_move == MapDirection.SOUTH else\
                        WEST if dir_to_move == MapDirection.WEST else \
                        EAST
                    val = first_half[spot_to_move.coordinates]
                    first_half[spot_to_move.coordinates] = 1 if val == EMPTY else val + 1
        return first_half

    def second_half(self, first_half: np.array):
        spots_to_move_to = np.nonzero(first_half == 1)
        num = len(spots_to_move_to[0]) if spots_to_move_to[0].size > 0 else 0
        for i in range(num):
            spot = Spot((spots_to_move_to[0][i], spots_to_move_to[1][i]))
            self.__move_elf(spot, first_half)

    def __move_elf(self, spot: Spot, first_half: np.array):
        for dir in MOVING_ELF_VALUES.keys():
            val = first_half[spot.get_neighboring_coordinates(dir).coordinates]
            self.grid[spot.x, spot.y] = ELF
            if MOVING_ELF_VALUES[dir] == val:
                self.__remove_elf(spot, dir)

    def __remove_elf(self, spot: Spot, dir: MapDirection):
        if dir == MapDirection.SOUTH:
            self.grid[spot.x + 1, spot.y] = EMPTY
        elif dir == MapDirection.NORTH:
            self.grid[spot.x - 1, spot.y] = EMPTY
        elif dir == MapDirection.WEST:
            self.grid[spot.x, spot.y - 1] = EMPTY
        else:
            self.grid[spot.x, spot.y + 1] = EMPTY

    def __set_grid(self, i: int, j: int, val: int):
        self.grid[self.offset + i, self.offset + j] = val

    def __stay_put(self, elf: Spot):
        neighbors = self.__get_all_neighbors(elf)
        return self.__are_free(neighbors)

    def __dir_to_move(self, elf: Spot, directions: List[MapDirection]) -> MapDirection:
        return next(iter([dir for dir in directions if self.__can_move(elf, dir)]), None)

    def __can_move(self, elf: Spot, dir: MapDirection):
        neighbors = self.__get_neighbors(elf, dir)
        return self.__are_free(neighbors)

    def __neighbor(self, spot: XYPair, offset: Tuple[int, int]):
        return self.grid[spot.x + offset[0], spot.y + offset[1]]

    def __get_all_neighbors(self, spot: XYPair):
        offsets = [i for i in product([1, 0, -1], repeat=2) if i != (0, 0)]
        return [self.__neighbor(spot, offset) for offset in offsets]

    def __get_neighbors(self, spot: XYPair, dir: MapDirection):
        offsets = [(-1, -1), (-1, 0), (-1, 1)] if dir == MapDirection.NORTH else \
            [(1, -1), (1, 0), (1, 1)] if dir == MapDirection.SOUTH else \
            [(-1, -1), (0, -1), (1, -1)] if dir == MapDirection.WEST else \
            [(-1, 1), (0, 1), (1, 1)]
        return [self.__neighbor(spot, offset) for offset in offsets]

    @staticmethod
    def __are_free(neighbors: List[int]):
        return all([n != ELF for n in neighbors])


if __name__ == '__main__':
    filename = 'input/day23.txt'
    data = read_file(filename)

    grove = Grove(data, Part.PT1)
    grove.process(10)
    print(f'The answer to Pt 1 is {grove.answer}')

    grove = Grove(data, Part.PT2)
    rounds = grove.process()
    print(f'The answer to Pt 2 is {rounds}')
