from __future__ import annotations
from typing import Union

import numpy as np

from utils import read_file, CircularLinkedList, XYPair, Direction


class Rock:
    def __init__(self, values: np.array):
        self.values = values
        self.pos: Union[XYPair, None] = None

    @property
    def width(self):
        return self.values.shape[1]

    @property
    def height(self):
        return self.values.shape[0]


ROCKS = [
    Rock(np.array([[1, 1, 1, 1]])),
    Rock(2 * np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])),
    Rock(3 * np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]])),
    Rock(4 * np.array([[1], [1], [1], [1]])),
    Rock(5 * np.array([[1, 1], [1, 1]])),
]


class TowerState:
    def __init__(self, rock_num: int, height: int, top_row: np.array, jet_id: int, rock_id: int):
        self.rock_num = rock_num
        self.height = height
        self.top_row = top_row
        self.jet_id = jet_id
        self.rock_id = rock_id

    def __eq__(self, other: TowerState):
        return True if sum(self.top_row == other.top_row) == len(self.top_row) and \
            self.jet_id == other.jet_id and self.rock_id == other.rock_id else False


class Tower:
    TOWER_WIDTH = 7
    MAX_HEIGHT = 10_000

    def __init__(self, jets: str):
        self.rocks = CircularLinkedList(ROCKS)
        self.jets = CircularLinkedList([Direction.LEFT if jet == '<' else Direction.RIGHT for jet in jets])
        self.tower = np.zeros((self.MAX_HEIGHT, self.TOWER_WIDTH + 2))
        self.tower[:, 0] = 8 * np.ones((self.MAX_HEIGHT, ))
        self.tower[:, self.TOWER_WIDTH + 1] = 8 * np.ones((self.MAX_HEIGHT, ))
        self.tower[self.MAX_HEIGHT - 1, :] = 8 * np.ones((self.TOWER_WIDTH + 2, ))
        self.current_x = self.MAX_HEIGHT - 1
        self.unique_states = []
        self.start_rock = 0
        self.start_height = 0
        self.rocks_in_pattern = 0
        self.pattern_height = 0

    def let_rocks_fall(self, num):
        rock_num = 0
        while rock_num < num:
            rock = self.rocks.get_next()
            rock.pos = self.__get_rock_starting_pos(rock)
            rock_num += 1
            self.__let_rock_fall(rock)
        return self.tower_height

    def find_pattern(self):
        rock_num = 0
        pattern_found = False
        while not pattern_found:
            rock = self.rocks.get_next()
            rock.pos = self.__get_rock_starting_pos(rock)
            rock_num += 1
            self.__let_rock_fall(rock)
            current_state = TowerState(rock_num,
                                       self.tower_height,
                                       self.tower[self.current_x, :],
                                       self.jets.current.id,
                                       self.rocks.current.id)
            self.unique_states.append(current_state)
            if self.unique_states.count(current_state) == 3:
                states = [state for state in self.unique_states if state == current_state]
                if states[2].rock_num - states[1].rock_num == states[1].rock_num - states[0].rock_num:
                    pattern_found = True
                    self.start_rock = states[0].rock_num
                    self.start_height = states[0].height
                    self.rocks_in_pattern = states[1].rock_num - states[0].rock_num
                    self.pattern_height = states[1].height - states[0].height
                    return

    def get_total_height(self, num_rocks: int):
        num_of_repeats = (num_rocks - self.start_rock) // self.rocks_in_pattern
        extra_rocks = (num_rocks - self.start_rock) % self.rocks_in_pattern

        tower = Tower(data[0])
        height_floor_to_extra = tower.let_rocks_fall(self.start_rock + extra_rocks)
        extra_height = height_floor_to_extra - self.start_height
        return self.start_height + self.pattern_height * num_of_repeats + extra_height

    def __let_rock_fall(self, rock: Rock):
        landed = False
        while not landed:
            jet = self.jets.get_next()
            if self.__can_move(rock, jet):
                rock.pos.y += 1 if jet == Direction.RIGHT else -1
            if self.__can_move(rock, Direction.DOWN):
                rock.pos.x += 1
            else:
                landed = True
                self.current_x = min(rock.pos.x, self.current_x)
                target = self.tower[rock.pos.x:rock.pos.x + rock.height, rock.pos.y: rock.pos.y + rock.width]
                self.tower[rock.pos.x:rock.pos.x + rock.height, rock.pos.y: rock.pos.y + rock.width] = \
                    target + rock.values

    @property
    def tower_height(self):
        return self.MAX_HEIGHT - 1 - self.current_x

    def __get_rock_starting_pos(self, rock: Rock):
        # This is pos of upper left corner of rock
        return XYPair((self.current_x - 3 - rock.height, 3))

    def __can_move(self, rock: Rock, direction: Direction):
        if direction == Direction.RIGHT:
            target_array = self.tower[rock.pos.x: rock.pos.x + rock.height, \
                           rock.pos.y + 1: rock.pos.y + 1 + rock.width]
        elif direction == Direction.LEFT:
            target_array = self.tower[rock.pos.x: rock.pos.x + rock.height, \
                           rock.pos.y - 1: rock.pos.y - 1 + rock.width]
        else:
            target_array = self.tower[rock.pos.x + 1: rock.pos.x + 1 + rock.height, \
                           rock.pos.y: rock.pos.y + rock.width]
        return sum(sum(np.logical_and(rock.values, target_array))) == 0


if __name__ == '__main__':
    filename = 'input/day17.txt'
    data = read_file(filename)

    tower = Tower(data[0])
    tower.find_pattern()
    tower_height = tower.get_total_height(2022)
    print(f'The answer to Part 1 is {tower_height}')

    tower_height = tower.get_total_height(1000000000000)
    print(f'The answer to Part 1 is {tower_height}')
