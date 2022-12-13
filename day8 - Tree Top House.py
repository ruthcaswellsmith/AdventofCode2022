from typing import List

import numpy as np

from utils import read_file, Direction


class Map:
    def __init__(self, tree_data: List[str]):
        self.trees = np.array([[int(c) for c in line] for line in tree_data])
        self.visibility = np.ones((self.rows, self.cols), dtype=bool)
        self.scenic_scores = 2 * np.ones((self.rows, self.cols), dtype=int)

    @property
    def rows(self):
        return self.trees.shape[0]

    @property
    def cols(self):
        return self.trees.shape[1]

    @property
    def visible_trees(self):
        return sum(sum(self.visibility))

    @property
    def max_scenic_score(self):
        return np.amax(self.scenic_scores)

    def process(self):
        for row in range(1, self.rows - 1):
            for col in range(1, self.cols - 1):
                self.visibility[row, col] = any([self.__is_visible(row, col, direction) for direction in Direction])
                self.scenic_scores[row, col] = \
                    np.prod([self.__get_num_trees(row, col, direction) for direction in Direction])

    def __get_trees(self, x, y, direction: Direction):
        if direction == Direction.LEFT:
            return np.flip(self.trees[x, 0:y])
        elif direction == Direction.RIGHT:
            return self.trees[x, y + 1:]
        elif direction == Direction.UP:
            return np.flip(self.trees[0:x, y])
        else:
            return self.trees[x + 1:, y]

    def __get_tree_info(self, x: int, y: int, direction: Direction):
        return self.trees[x, y], self.__get_trees(x, y, direction)

    def __is_visible(self, x: int, y: int, direction: Direction):
        height, trees = self.__get_tree_info(x, y, direction)
        return max(trees) < height

    def __get_num_trees(self, x: int, y: int, direction: Direction):
        height, trees = self.__get_tree_info(x, y, direction)
        return next((pos + 1 for pos, t in enumerate(trees) if t >= height), len(trees))


if __name__ == '__main__':
    filename = 'input/day8.txt'
    data = read_file(filename)

    map = Map(data)
    map.process()
    print(f"The answer to Pt 1 is {map.visible_trees}")
    print(f"The answer to Pt 2 is {map.max_scenic_score}")
