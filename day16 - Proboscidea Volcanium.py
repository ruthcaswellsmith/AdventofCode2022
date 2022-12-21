from __future__ import annotations
from typing import List, Tuple, Dict
from collections import namedtuple
from itertools import permutations
import numpy as np

from utils import read_file, Graph, GraphNode
LARGE = 1_000_000


class Valve:
    def __init__(self, id: int, line: str):
        self.id = id
        self.name = line[line.index('Valve ')+6:line.index('Valve ')+8]
        self.adj_valves = line[line.index("valves ")+7:].split() if 'valves' in line else \
            line[line.index("valve ") + 6:].split()
        self.adj_valves = [v.replace(',', '') for v in self.adj_valves]
        self.flow_rate = eval(line[line.index('=')+1:line.index(';')])


class Tunnels:
    def __init__(self, data: List[str]):
        self.valves = [Valve(i, line) for i, line in enumerate(data)]
        self.name_to_id = {v.name: i for i, v in enumerate(self.valves)}
        self.nodes = [(GraphNode(i, [self.name_to_id[n] for n in v.adj_valves])) for i, v in enumerate(self.valves)]
        self.graph = Graph(self.nodes, np.logical_not(np.identity(len(self.nodes))).astype(int))
        self.graph.find_all_shortest_paths()
        self.tsp_valves = [v for v in self.valves if v.flow_rate > 0 or v.name == 'AA']
        self.current_max = -1_000_000
        self.find_max_flow(self.__get_valve('AA'))
        self.visited = []
        self.total_cost = 0

    def __get_unvisited_neighbors(self):
        return [n for n in self.tsp_valves if n not in self.visited]

    def find_max_flow(self, valve: Valve):
        self.visited.append(valve)
        neighbors = self.__get_unvisited_neighbors()
        if len(neighbors) == 2:
            return self.graph.shortest_paths[]


    def __get_valve(self, name: str):
        return next(iter(v for v in self.valves if v.name == name))

    def __takes_too_long(self, path: List[Valve]):
        total_time = 0
        for i in range(len(path)-1):
            total_time += self.graph.shortest_paths[path[i].id, path[i+1].id] + 1
            if total_time > 30:
                return True

    def __get_cost(self, path: List[Valve]):
        total_time, total_cost = 0, 0
        for i in range(len(path) - 1):
            total_time += self.graph.shortest_paths[path[i].id, path[i+1].id] + 1
            total_cost += path[i+1].flow_rate * (30 - total_time)
        return total_cost


if __name__ == '__main__':
    filename = 'input/day16.txt'
    data = read_file(filename)

    tunnels = Tunnels(data)
    print('h')