import numpy as np
from typing import List, Union

from utils import read_file, Direction, XYPair, Part


class Neighbor:
    def __init__(self, pos: XYPair):
        self.pos = pos
        self.cost = 0

    def update_cost(self, cost: int):
        self.cost = cost


class HillClimb:
    LARGE = 1_000_000
    ME = 1111
    SIGNAL = 2222
    ORD_A = 97

    def __init__(self, data: List[str], part: Part):
        self.part = part
        self.grid = np.array([[self.__translate(c) for c in line] for line in data], dtype=int)
        self.size = XYPair(self.grid.shape)
        self.num_nodes = self.size.x * self.size.y
        self.visited = np.zeros(self.size.coordinates, dtype=bool)
        self.costs = self.LARGE * np.ones(self.grid.shape, dtype=int)
        if self.part == Part.PT1:
            self.start = self.__find_location(self.ME)
            self.grid[self.start.coordinates] = self.__translate('a')
            self.end = self.__find_location(self.SIGNAL)
            self.grid[self.end.coordinates] = self.__translate('z')
        else:
            self.start = self.__find_location(self.SIGNAL)
            self.grid[self.start.coordinates] = self.__translate('z')
            self.end = self.__find_location(self.ME)
            self.grid[self.end.coordinates] = self.__translate('a')
        self.current = self.start
        self.costs[self.current.coordinates] = 0

    def process(self):
        done = False
        while not done:
            neighbors = self.__get_unvisited_neighbors()
            self.__update_costs_for_neighbors(neighbors)
            self.visited[self.current.coordinates] = True
            if not sum(sum(self.visited)) == self.num_nodes:
                self.__update_current()
            else:
                done = True

    def __update_costs_for_neighbors(self, neighbors: List[Neighbor]):
        for neighbor in neighbors:
            current_cost = self.costs[neighbor.pos.coordinates]
            self.costs[neighbor.pos.coordinates] = min(self.costs[self.current.coordinates] + neighbor.cost,
                                                       current_cost)

    def __update_current(self):
        min_cost = np.min(self.costs[~self.visited])
        min_locations = np.logical_and(self.costs == min_cost, ~self.visited)
        location = np.argwhere(min_locations)[0]
        self.current = XYPair((location[0], location[1]))

    @property
    def answer_pt1(self):
        return self.costs[self.end.coordinates]

    @property
    def answer_pt2(self):
        return min(self.costs[self.grid == 0])

    def __translate(self, char: str):
        return self.ME if char == 'S' else self.SIGNAL if char == 'E' else ord(char) - self.ORD_A

    def __find_location(self, val: int) -> XYPair:
        return XYPair(tuple(np.argwhere(self.grid == val)[0]))

    def __get_unvisited_neighbors(self) -> List[Neighbor]:
        return [neighbor for direction in Direction if (neighbor := self.__get_neighbor(direction))]

    def __get_neighbor(self, direction: Direction) -> Union[None, Neighbor]:
        if self.is_on_edge(direction):
            return None
        neighbor = Neighbor(self.current.get_neighbor(direction))
        if self.visited[neighbor.pos.coordinates]:
            return None
        diff_elev = self.grid[neighbor.pos.coordinates] - self.grid[self.current.coordinates]
        if self.part == Part.PT1 and diff_elev > 1 or self.part == Part.PT2 and diff_elev < -1:
            return None
        neighbor.update_cost(1)
        return neighbor

    def is_on_edge(self, direction: Direction):
        return True if direction == Direction.LEFT and self.current.x == 0 or \
                       direction == Direction.RIGHT and (self.current.x == self.size.x - 1) or \
                       direction == Direction.UP and self.current.y == 0 or \
                       direction == Direction.DOWN and (self.current.y == self.size.y - 1) else False


if __name__ == '__main__':
    filename = 'input/day12.txt'
    data = read_file(filename)

    hill_climb = HillClimb(data, Part.PT1)
    hill_climb.process()
    print(f"The answer to Pt 1 is {hill_climb.answer_pt1}")

    hill_climb = HillClimb(data, Part.PT2)
    hill_climb.process()
    print(f"The answer to Pt 2 is {hill_climb.answer_pt2}")
