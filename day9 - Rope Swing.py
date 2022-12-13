from __future__ import annotations
from typing import List

import numpy as np

from utils import read_file, XYPair, Direction


class Rope:
    SIZE = 1000
    START = (500, 500)

    def __init__(self, knots: int = 2):
        self.knots = [XYPair(self.START) for _ in range(knots)]
        self.grid = np.zeros((self.SIZE, self.SIZE), dtype=bool)

    @property
    def answer(self):
        return sum(sum(self.grid))

    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[len(self.knots) - 1]

    def move_head(self, direction: Direction):
        self.head.move(direction)

    def move_knots(self):
        for i in range(len(self.knots) - 1):
            current_knot, next_knot = self.knots[i], self.knots[i+1]
            deltas = current_knot - next_knot
            if abs(deltas.x) == 2:
                next_knot.move(Direction.RIGHT) if deltas.x > 0 else next_knot.move(Direction.LEFT)
                if abs(deltas.y) == 1:
                    next_knot.move(Direction.DOWN) if deltas.y > 0 else next_knot.move(Direction.UP)
            if abs(deltas.y) == 2:
                next_knot.move(Direction.DOWN) if deltas.y > 0 else next_knot.move(Direction.UP)
                if abs(deltas.x) == 1:
                    next_knot.move(Direction.RIGHT) if deltas.x > 0 else next_knot.move(Direction.LEFT)

    def simulate_motions(self, motions: List[Motion]):
        for motion in motions:
            self.__process_motion(motion)

    def __process_motion(self, motion: Motion):
        for step in range(motion.steps):
            self.move_head(motion.direction)
            self.move_knots()
            self.grid[self.tail.x, self.tail.y] = True


class Motion:
    DIR_DICT = {'R': Direction.RIGHT, 'L': Direction.LEFT, 'U': Direction.UP, 'D': Direction.DOWN}

    def __init__(self, text: str):
        self.text = text

    @property
    def direction(self) -> Direction:
        return self.DIR_DICT[self.text[0]]

    @property
    def steps(self):
        return int(self.text.split()[1])


if __name__ == '__main__':
    filename = 'input/day9.txt'
    data = read_file(filename)

    rope = Rope(2)
    rope.simulate_motions([Motion(line) for line in data])
    print(f"The answer to Pt 1 is {rope.answer}")

    rope = Rope(10)
    rope.simulate_motions([Motion(line) for line in data])
    print(f"The answer to Pt 2 is {rope.answer}")
