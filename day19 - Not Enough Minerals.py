from __future__ import annotations

from enum import Enum
from typing import List, Dict, Union
from math import ceil

from anytree import AnyNode

from utils import read_file

TIME_LIMIT = 24


class Resource(str, Enum):
    ORE = 'ore'
    CLAY = 'clay'
    OBSIDIAN = 'obsidian'
    GEODE = 'geode'


class Blueprint:
    def __init__(self, line: str):
        words = line.split(':')
        self.id = int(words[0][-2:])
        robots = [robot for robot in words[1].split(".") if robot]
        self.robots = {}
        for robot in robots:
            words = robot.split()
            self.robots[Resource(words[1])] = \
                {Resource(words[i + 1]): int(word) for i, word in enumerate(words) if word.isdigit()}
        self.max_robots = {}
        for resource in Resource:
            if resource != Resource.GEODE:
                max_spend = max([self.robots[robot_type].get(resource, 0) for robot_type in Resource])
                self.max_robots[resource] = max_spend


class State(AnyNode):
    def __init__(self, id: str,
                 blueprint: Blueprint,
                 robots: Dict[Resource, int] = None,
                 resources: Dict[Resource, int] = None,
                 minutes: int = 0,
                 parent=None,
                 children=None):
        super().__init__(id=id, parent=parent, children=children)
        self.blueprint = blueprint
        self.robots = robots if robots else \
            {Resource.ORE: 1, Resource.CLAY: 0, Resource.OBSIDIAN: 0, Resource.GEODE: 0}
        self.resources = resources if resources else \
            {k: 0 for k in Resource}
        self.minutes = minutes

    def __eq__(self, other):
        return True if self.robots == other.robots and \
                       self.resources == other.resources and \
                       self.minutes <= other.minutes else False

    @property
    def robots_to_buy(self):
        return [robot for robot in Resource if self.can_use_another(robot) and self.can_wait_for(robot)]

    def min_to_wait(self, robot_type: Resource):
        min_to_wait = []
        for resource in self.blueprint.robots[robot_type].keys():
            needed = max(self.blueprint.robots[robot_type][resource] - self.resources[resource], 0)
            min_to_wait.append(ceil(needed / self.robots[resource]) if needed > 0 else 1)
        return max(min_to_wait)

    def can_wait_for(self, robot_type: Resource):
        return True if all([self.robots[resource] > 0 for resource in self.blueprint.robots[robot_type].keys()]) \
            else False

    def can_use_another(self, robot_type: Resource):
        return True if robot_type == Resource.GEODE or \
            self.robots[robot_type] < self.blueprint.max_robots[robot_type] else False

    def get_new_state(self, robot_type: Resource):
        delta_min = self.min_to_wait(robot_type)
        new_state = State(
            f"{self.id}/{robot_type}",
            self.blueprint,
            {k: v + (1 if k == robot_type else 0) for k, v in self.robots.items()},
            {k: v + (delta_min + 1)*self.robots[k] - self.blueprint.robots[robot_type].get(k, 0) \
                for k, v in self.resources.items()},
            self.minutes + delta_min + 1,
            parent=self)
        return new_state


class Puzzle:
    def __init__(self, data: List[str]):
        self.blueprints = [Blueprint(line) for line in data if line]
        self.visited: List[State] = []
        self.not_visited = 0

    def build_tree(self, state: State, max_geodes: int) -> int:
        self.visited.append(state)
        print(f'{state.minutes}')
        print(f'entering {state.robots.items()} {state.resources.items()}')
        if state.minutes == TIME_LIMIT - 1:
            print(f'hit time limit {state.resources[Resource.GEODE]} geodes while max_geodes is {max_geodes}')
            return state.resources[Resource.GEODE] + state.robots[Resource.GEODE]
        if self.__cannot_beat_max(state, max_geodes):
            print(f'returning early {max_geodes}')
            return state.resources[Resource.GEODE]
        else:
            for robot in state.robots_to_buy:
                # print(state.robots_to_buy)
                new_state = state.get_new_state(robot)
                if new_state not in self.visited:
                    geodes = self.build_tree(new_state, max_geodes)
                    max_geodes = max(geodes, max_geodes)
                else:
                    self.not_visited += 1
                    # print('found same state', len(self.visited), self.not_visited)
            return max_geodes

    @staticmethod
    def __cannot_beat_max(state: State, max_geodes: int):
        delta_min = TIME_LIMIT - state.minutes
        # diff = sum([v - state.robots[k] for k, v in state.blueprint.robots[Resource.GEODE].items()])
        # delta_min = delta_min - diff
        potential_geodes = state.resources[Resource.GEODE] + delta_min * state.robots[Resource.GEODE] + \
            sum([i for i in range(1, delta_min)])
        return True if potential_geodes <= max_geodes else False


if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    puzzle = Puzzle(data)
    import datetime
    # answers = []
    # for i, blueprint in enumerate(puzzle.blueprints):
    #     puzzle = Puzzle(data)
    #     print(f'processing blueprint {blueprint.id}')
    #     start = datetime.datetime.now()
    #     max_geodes = puzzle.build_tree(State('start', blueprint), 0)
    #     answers.append(blueprint.id * max_geodes)
    #     print(f"{datetime.datetime.now() - start}")
    # print(f'The answer to part 1 is {sum(answers)}')

    buys = [Resource.CLAY,
            Resource.CLAY,
            Resource.CLAY,
            Resource.OBSIDIAN,
            Resource.CLAY,
            Resource.OBSIDIAN,
            Resource.GEODE,
            Resource.GEODE]

    state = State('start', puzzle.blueprints[0])
    states = []
    for buy in buys:
        states.append(state)
        new_state = state.get_new_state(buy)
        state = new_state
    print("h")
