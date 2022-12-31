from __future__ import annotations

from typing import List
import numpy as np
from math import lcm
from queue import Queue

from utils import read_file, XYPair


WALL = 8
SPACE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4


class Valley:
    def __init__(self, data: List[str]):
        self.height, self.width = len(data), len(data[0])
        self.walls = np.zeros((self.height, self.width), dtype=bool)
        self.right, self.left, self.up, self.down = \
            self.walls.copy(), self.walls.copy(), self.walls.copy(), self.walls.copy()
        for i, line in enumerate(data):
            for j, c in enumerate(line):
                self.walls[i, j] = True if c == '#' else SPACE
                self.right[i, j] = True if c == '>' else SPACE
                self.left[i, j] = True if c == '<' else SPACE
                self.up[i, j] = True if c == '^' else SPACE
                self.down[i, j] = True if c == 'v' else SPACE
        self.repeat = lcm(self.height - 2, self.width - 2)
        self.blizzards = self.blizzard_pattern()
        self.queue = Queue()
        self.visited = {}
        self.fixed_positions = {
            'start': XYPair((0, 1)),
            'end': XYPair((self.height-1, self.width-2))
        }

    def blocked(self, num_moves: int):
        index = num_moves % self.repeat
        return np.logical_or(self.walls, self.blizzards[index])

    def potential_moves(self, pos: XYPair, num_moves: int):
        potential_moves = []
        blocked = self.blocked(num_moves)
        if pos.x > 0 and not blocked[pos.x-1, pos.y]:
            potential_moves.append(XYPair((pos.x-1, pos.y)))
        if pos.x < self.height - 1 and not blocked[pos.x+1, pos.y]:
            potential_moves.append(XYPair((pos.x+1, pos.y)))
        if pos.y > 0 and not blocked[pos.x, pos.y+1]:
            potential_moves.append(XYPair((pos.x, pos.y+1)))
        if pos.y < self.width - 1 and not blocked[pos.x, pos.y-1]:
            potential_moves.append(XYPair((pos.x, pos.y-1)))
        if not blocked[pos.x, pos.y]:
            potential_moves.append(XYPair((pos.x, pos.y)))
        return potential_moves

    def blizzard_pattern(self):
        self.blizzards = []
        right, left, up, down = \
            self.right[1:self.height-1, 1:self.width-1], \
            self.left[1:self.height - 1, 1:self.width - 1], \
            self.up[1:self.height-1, 1:self.width-1], \
            self.down[1:self.height - 1, 1:self.width - 1]
        for i in range(self.repeat):
            self.blizzards.append(np.pad(np.logical_or(np.logical_or(np.logical_or(right, left), up), down), 1))
            right = np.roll(right, shift=1, axis=1)
            left = np.roll(left, shift=-1, axis=1)
            up = np.roll(up, shift=-1, axis=0)
            down = np.roll(down, shift=1, axis=0)
        return self.blizzards

    def bfs(self, start: str, end: str, num_moves: int):
        start_pos = self.fixed_positions[start]
        end_pos = self.fixed_positions[end]
        self.queue.put((start_pos, num_moves))
        min_moves = 1_000_000

        while self.queue.qsize() > 0:
            pos, num_moves = self.queue.get()
            num_moves += 1
            for new_pos in self.potential_moves(pos, num_moves):
                index = num_moves % self.repeat
                if new_pos == end_pos:
                    min_moves = min(min_moves, num_moves)
                    continue
                if f"{new_pos.coordinates}-{index}" not in self.visited:
                    self.queue.put((new_pos, num_moves))
                    self.visited[f"{new_pos.coordinates}-{index}"] = min_moves
        return min_moves


if __name__ == '__main__':
    filename = 'input/day24.txt'
    data = read_file(filename)

    valley = Valley(data)
    min_moves = valley.bfs('start', 'end', 0)
    print(f"The answer to Part1 is {min_moves}")

    valley = Valley(data)
    plus_moves_back = valley.bfs('end', 'start', min_moves)

    valley = Valley(data)
    total_moves = valley.bfs('start', 'end', plus_moves_back)
    print(f"The answer to Part2 is {total_moves}")
