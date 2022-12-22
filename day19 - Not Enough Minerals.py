from __future__ import annotations

from enum import Enum, auto
from typing import List, Dict

from utils import read_file


class Action(str, Enum):
    WAIT = auto()
    BUY_ORE_ROBOT = auto()
    BUY_CLAY_ROBOT = auto()
    BUY_OBSIDIAN_ROBOT = auto()
    BUY_GEODE_ROBOT = auto()


class Resource(str, Enum):
    ORE = 'ore'
    CLAY = 'clay'
    OBSIDIAN = 'obsidian'
    GEODE = 'geode'


class Robot:
    def __init__(self, line: str):
        words = line.split()
        self.robot_type = Resource(words[1]).name
        self.costs = {Resource(words[i+1]): int(word) for i, word in enumerate(words) if word.isdigit()}


class Blueprint:
    def __init__(self, line: str):
        words = line.split(':')
        self.id = int(words[0][-2:])
        self.robots = [Robot(word) for word in words[1].split(".") if word]


class State:
    def __init__(self, blueprint: Blueprint, robots: Dict[Resource, int], resources: Dict[Resource, int], minutes: int):
        self.blueprint = blueprint
        self.robots = robots
        self.resources = resources
        self.minutes = minutes

    @property
    def actions(self):
        actions = [Action.WAIT]
        if self.buy_ore_robot():
            actions.append(Action.BUY_ORE_ROBOT)
        if self.buy_clay_robot():
            actions.append(Action.BUY_CLAY_ROBOT)
        if self.buy_obsidian_robot():
            actions.append(Action.BUY_OBSIDIAN_ROBOT)
        if self.buy_geode_robot():
            actions.append(Action.BUY_GEODE_ROBOT)
        return actions

    def buy_ore_robot(self):
        return True if self.resources[Resource.ORE] > self.blueprint.robots[Resource.ORE] else False

    def buy_clay_robot(self):
        return True if self.resources[Resource.CLAY] > self.robots[Resource.CLAY] else False

    def buy_obsidian_robot(self):
        return True if self.resources[Resource.OBSIDIAN] > self.robots[Resource.OBSIDIAN] else False

    def buy_geode_robot(self):
        return True if self.resources[Resource.GEODE] > self.robots[Resource.GEODE] else False

    def take_action(self, action: Action):
        self.resources[Resource.ORE] +=
        if action == Action.BUY_ORE_ROBOT:
            self.resources[Resource.ORE] -= self.robots[Resource.ORE]
        if action == Action.BUY_ORE_ROBOT:
            self.resources[Resource.ORE] -= self.robots[Resource.ORE]
        if action == Action.BUY_ORE_ROBOT:
            self.resources[Resource.ORE] -= self.robots[Resource.ORE]
        if action == Action.BUY_ORE_ROBOT:
            self.resources[Resource.ORE] -= self.robots[Resource.ORE]

class Puzzle:
    TIME_LIMIT = 24

    def __init__(self, data: List[str]):
        self.blueprints = [Blueprint(line) for line in data if line]
        states = self.process_state(blueprint, [initial_state])

    def process_state(self, blueprint, states):
        done = False
        while not done:
            current_state = previous_states[1]
            for action in current_state.actions:
                next_state = self.perform_action(blueprint, state, action)
                if next_state.time == self.TIME_LIMIT:
                    done = True



if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    puzzle = Puzzle(data)
    print(f'The answer to Part 1 is')
