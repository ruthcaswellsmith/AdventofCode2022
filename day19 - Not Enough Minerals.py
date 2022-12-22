from __future__ import annotations

from enum import Enum
from typing import List, Dict, Union

from anytree import AnyNode, PreOrderIter

from utils import read_file


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
        print()


class State(AnyNode):
    def __init__(self, id: str,
                 blueprint: Blueprint, robots: Dict[Resource, int], resources: Dict[Resource, int], minutes: int,
                 parent=None, children=None):
        super().__init__(id=id, parent=parent, children=children)
        self.blueprint = blueprint
        self.robots = robots
        self.resources = resources
        self.minutes = minutes

    def can_afford(self, robot_type: Resource):
        for resource in Resource:
            cost = self.blueprint.robots[robot_type].get(resource, None)
            if cost and self.resources[resource] < cost:
                return False
        return True

    def can_use_another(self, resource: Resource):
        return True if self.robots[resource] < self.blueprint.max_robots[resource] else False

    @property
    def actions(self):
        if self.can_afford(Resource.GEODE):
            return [Resource.GEODE]
        actions = [None]
        if self.can_afford(Resource.ORE) and self.can_use_another(Resource.ORE):
            actions.append(Resource.ORE)
        if self.can_afford(Resource.CLAY) and self.can_use_another(Resource.CLAY):
            actions.append(Resource.CLAY)
        if self.can_afford(Resource.OBSIDIAN) and self.can_use_another(Resource.OBSIDIAN):
            actions.append(Resource.OBSIDIAN)
        return actions

    def take_action(self, action: Union[None, Resource]):
        for robot_type in self.robots:
            self.resources[robot_type] += self.robots[robot_type]
        if action:
            self.robots[action] += 1
            costs = self.blueprint.robots[action]
            for key, val in costs.items():
                self.resources[key] -= val
        self.minutes += 1


class Puzzle:
    TIME_LIMIT = 24

    def __init__(self, data: List[str]):
        self.blueprints = [Blueprint(line) for line in data if line]
        print('h')
    #     states = self.process_state(blueprint, [initial_state])
    #
    # def process_state(self, blueprint, states):
    #     done = False
    #     while not done:
    #         current_state = previous_states[1]
    #         for action in current_state.actions:
    #             next_state = self.perform_action(blueprint, state, action)
    #             if next_state.time == self.TIME_LIMIT:
    #                 done = True



if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    puzzle = Puzzle(data)
    print(f'The answer to Part 1 is')
