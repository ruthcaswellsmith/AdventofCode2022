from __future__ import annotations

from enum import Enum
from math import ceil
import numpy as np
from typing import List, Dict
from queue import Queue
import json

from utils import read_file, Part


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


class State:
    def __init__(self, blueprint: Blueprint,
                 time_limit: int,
                 robots: Dict[Resource, int] = None,
                 resources: Dict[Resource, int] = None,
                 minutes: int = 0):
        self.blueprint = blueprint
        self.time_limit = time_limit
        self.robots = robots if robots else \
            {Resource.ORE: 1, Resource.CLAY: 0, Resource.OBSIDIAN: 0, Resource.GEODE: 0}
        self.resources = resources if resources else {k: 0 for k in Resource}
        self.minutes = minutes

    def __eq__(self, other):
        return True if self.robots == other.robots and \
                       self.resources == other.resources and \
                       self.minutes <= other.minutes else False

    @property
    def identifier(self):
        return f"{json.dumps(self.robots)}-{json.dumps(self.resources)}-{self.minutes}"

    @property
    def geodes(self):
        return self.resources[Resource.GEODE]

    @property
    def robots_to_buy(self):
        return [robot for robot in Resource if self.can_use_another(robot) and self.can_wait_for(robot) \
                and self.min_to_wait(robot) <= self.time_limit - 1 - self.minutes]

    def min_to_wait(self, robot_type: Resource):
        min_to_wait = []
        for resource in self.blueprint.robots[robot_type].keys():
            needed = max(self.blueprint.robots[robot_type][resource] - self.resources[resource], 0)
            min_to_wait.append(ceil(needed / self.robots[resource]) if needed > 0 else 0)
        return max(min_to_wait)

    def can_wait_for(self, robot_type: Resource):
        return True if all([self.robots[resource] > 0 for resource in self.blueprint.robots[robot_type].keys()]) \
            else False

    def can_use_another(self, robot_type: Resource):
        if robot_type == Resource.GEODE:
            return True
        delta = self.time_limit - self.minutes
        if self.resources[robot_type] + delta * self.robots[robot_type] >= delta * self.blueprint.max_robots[robot_type]:
            return False
        if self.robots[robot_type] == self.blueprint.max_robots[robot_type]:
            return False
        return True

    def get_end_state(self):
        time_to_end = self.time_limit - self.minutes
        end_state = State(
            self.blueprint,
            self.time_limit,
            self.robots,
            {k: v + time_to_end*self.robots[k] for k, v in self.resources.items()},
            self.minutes + time_to_end)
        return end_state

    def get_new_state(self, robot_type: Resource):
        delta_min = self.min_to_wait(robot_type)
        new_state = State(
            self.blueprint,
            self.time_limit,
            {k: v + (1 if k == robot_type else 0) for k, v in self.robots.items()},
            {k: v + (delta_min + 1)*self.robots[k] - self.blueprint.robots[robot_type].get(k, 0) \
                for k, v in self.resources.items()},
            self.minutes + delta_min + 1)
        return new_state

    def can_beat_max(self, max_geodes: int):
        delta_min = self.time_limit - self.minutes
        # diff = sum([v - state.robots[k] for k, v in state.blueprint.robots[Resource.GEODE].items()])
        # delta_min = delta_min - diff
        potential_geodes = self.resources[Resource.GEODE] + delta_min * self.robots[Resource.GEODE] + \
            sum([i for i in range(1, delta_min)])
        return True if potential_geodes > max_geodes else False


class Puzzle:
    def __init__(self, data: List[str], part: Part):
        self.blueprints = [Blueprint(line) for line in data if line]
        if part == Part.PT2:
            self.blueprints = [b for i, b in enumerate(self.blueprints) if i < 3]
        self.visited = {}
        self.queue = Queue()
        self.max_geodes = []

    def process(self, time_limit: int):
        for i in range(len(self.blueprints)):
            state = State(self.blueprints[i], time_limit)
            self.visited = {}
            self.queue = Queue()
            self.max_geodes.append(self.bfs(state))

    @property
    def answer_pt1(self):
        return sum([(i+1) * v for i, v in enumerate(self.max_geodes)])

    @property
    def answer_pt2(self):
        return np.prod([v for v in self.max_geodes])

    def bfs(self, state: State):
        self.queue.put(state)
        max_geodes = 0

        while self.queue.qsize() > 0:
            state = self.queue.get()
            end_state = state.get_end_state()
            max_geodes = max(max_geodes, end_state.geodes)
            for robot_type in state.robots_to_buy:
                neighbor = state.get_new_state(robot_type)
                if neighbor.can_beat_max(max_geodes):
                    if neighbor.identifier not in self.visited:
                        self.queue.put(neighbor)
                        self.visited[neighbor.identifier] = neighbor.geodes
        return max_geodes


if __name__ == '__main__':
    filename = 'input/day19.txt'
    data = read_file(filename)

    puzzle = Puzzle(data, Part.PT1)
    puzzle.process(24)
    print(f"The answer to Part 1 is {puzzle.answer_pt1}")

    puzzle = Puzzle(data, Part.PT2)
    puzzle.process(32)
    print(f"The answer to Part 2 is {puzzle.answer_pt2}")
