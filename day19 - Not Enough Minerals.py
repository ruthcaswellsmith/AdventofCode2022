from __future__ import annotations

from enum import Enum
from typing import List, Dict, Union

from anytree import AnyNode, PreOrderIter

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

    def can_afford(self, robot_type: Resource):
        for resource in Resource:
            if self.resources[resource] < self.blueprint.robots[robot_type].get(resource, 0):
                return False
        return True

    def can_use_another(self, resource: Resource):
        return True if self.resources[resource] < self.blueprint.max_robots[resource] - 1 else False

    @property
    def actions(self):
        if self.can_afford(Resource.GEODE):
            return [Resource.GEODE]
        if self.minutes == TIME_LIMIT - 1:
            return [None]
        actions = []
        if self.can_afford(Resource.ORE) and self.can_use_another(Resource.ORE):
            actions.append(Resource.ORE)
        if self.can_afford(Resource.CLAY) and self.can_use_another(Resource.CLAY):
            actions.append(Resource.CLAY)
        if self.can_afford(Resource.OBSIDIAN) and self.can_use_another(Resource.OBSIDIAN):
            actions.append(Resource.OBSIDIAN)
        actions.append(None)
        return actions

    def get_new_state(self, action: Union[None, Resource]):
        new_state = State(
            f"{self.id}/{'Buy ' if action else 'Wait'}{action if action else ''}",
            self.blueprint,
            self.robots.copy(),
            self.resources.copy(),
            self.minutes,
            parent=self)
        for robot_type in self.robots:
            new_state.resources[robot_type] += new_state.robots[robot_type]
        if action:
            new_state.robots[action] += 1
            costs = new_state.blueprint.robots[action]
            for key, val in costs.items():
                new_state.resources[key] -= val
        new_state.minutes += 1
        return new_state


class Puzzle:
    def __init__(self, data: List[str]):
        self.blueprints = [Blueprint(line) for line in data if line]

        # actions = [
        #     None,
        #     None,
        #     Resource.CLAY,
        #     None,
        #     Resource.CLAY,
        #     None,
        #     Resource.CLAY,
        #     None,
        #     None,
        #     None,
        #     Resource.OBSIDIAN,
        #     Resource.CLAY,
        #     None,
        #     None,
        #     Resource.OBSIDIAN,
        #     None,
        #     None,
        #     Resource.GEODE,
        #     None,
        #     None,
        #     Resource.GEODE,
        #     None,
        #     None,
        #     None
        # ]
        #
        # start = State('start', self.blueprints[0])
        # current_state = start
        # for action in actions:
        #     current_state = current_state.get_new_state(action)

    def build_tree(self, state: State, max_geodes: int) -> int:
        if state.minutes == TIME_LIMIT or self.__cannot_beat_max(state, max_geodes):
            # print(f'returning with {state.resources[Resource.GEODE]} geodes while max_geodes is {max_geodes}')
            return state.resources[Resource.GEODE]
        else:
            for action in state.actions:
                new_state = state.get_new_state(action)
                geodes = self.build_tree(new_state, max_geodes)
                max_geodes = max(geodes, max_geodes)
            return max_geodes

    @staticmethod
    def __cannot_beat_max(state: State, max_geodes: int):
        delta_min = TIME_LIMIT - state.minutes
        potential_geodes = state.resources[Resource.GEODE] + delta_min * state.robots[Resource.GEODE] + \
            sum([i for i in range(1, delta_min)])
        return True if potential_geodes <= max_geodes else False


if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    puzzle = Puzzle(data)
    import datetime
    start = datetime.datetime.now()
    answers = []
    for blueprint in puzzle.blueprints:
        max_geodes = puzzle.build_tree(State('start', blueprint), 0)
        answers.append(blueprint.id * max_geodes)
    print(f"{datetime.datetime.now() - start}")
    print(f'The answer to Part 1 is')
