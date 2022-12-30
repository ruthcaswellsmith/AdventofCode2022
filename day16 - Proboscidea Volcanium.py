from __future__ import annotations
from typing import List, Tuple
import numpy as np
import itertools as it

from utils import read_file, Graph, GraphNode


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
        self.shortest_paths = self.__shortest_paths()
        self.visited_states = {}

    @staticmethod
    def two_partitions(S):
        res_list = []
        for l in range(0, int(len(S) / 2) + 1):
            combis = set(it.combinations(S, l))
            for c in combis:
                res_list.append((sorted(list(c)), sorted(list(S - set(c)))))
        return res_list

    def find_max_with_elephant(self):
        permutations = self.two_partitions(set([v for v in tunnels.shortest_paths if v != 'AA']))
        maxval = 0
        for i, p in enumerate(permutations):
            maxval = max(maxval, tunnels.find_max(26, 'AA', tuple(p[0])) + tunnels.find_max(26, 'AA', tuple(p[1])))
        return maxval

    def find_max(self, time: int, valve: str, valves: Tuple[str]):
        if (time, valve, valves) in self.visited_states:
            return self.visited_states[(time, valve, valves)]

        maxval = 0
        for target in self.shortest_paths[valve]:
            if target in valves:
                continue
            rem_time = time - self.shortest_paths[valve][target] - 1
            if rem_time <= 0:
                continue
            maxval = max(maxval, self.find_max(rem_time, target, valves + (target,)) + \
                         self.get_valve(target).flow_rate * rem_time)

        self.visited_states[(time, valve, valves)] = maxval
        return maxval

    def __shortest_paths(self):
        shortest_paths = {}
        for v in self.valves:
            if v.flow_rate == 0 and v.name != 'AA':
                continue
            shortest_paths[v.name] = {
                target.name: self.graph.shortest_paths[v.id, target.id] for target in self.valves if \
                target.flow_rate > 0 and target.name != v.name
            }
        return shortest_paths

    def get_valve(self, name: str):
        return next(iter(v for v in self.valves if v.name == name))


if __name__ == '__main__':
    filename = 'input/day16.txt'
    data = read_file(filename)

    tunnels = Tunnels(data)
    print(f'The answer to part 1 is {tunnels.find_max(30, "AA", ())}')

    tunnels = Tunnels(data)
    print(f'The answer to part 2 is {tunnels.find_max_with_elephant()}')
