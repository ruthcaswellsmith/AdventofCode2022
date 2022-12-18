from __future__ import annotations
from typing import List, Tuple, Dict
from collections import namedtuple
from itertools import permutations
import numpy as np

from utils import read_file
LARGE = 1_000_000


class Node:
    def __init__(self, id: int, adj_list: List[int]):
        self.id = id
        self.adj_list = adj_list
        self.cost = LARGE


class Graph:
    def __init__(self, nodes: List[Node], edge_costs: np.array):
        self.nodes = nodes
        self.edge_costs = edge_costs
        self.shortest_paths = edge_costs.copy()
        self.current_cost = 0
        self.visited = List[Node]

    @property
    def num_nodes(self):
        return len(self.nodes)

    @property
    def unvisited_nodes(self):
        unvisited = [n for n in self.nodes if n not in self.visited]
        unvisited.sort(key=lambda n: n.cost)
        return unvisited

    def get_node(self, id: int):
        return next(iter(n for n in self.nodes if n.id == id))

    def find_all_shortest_paths(self):
        for n in self.nodes:
            self.__find_shortest_paths(n)

    def __find_shortest_paths(self, starting_node: Node):
        self.visited, self.current_cost = [], 0
        for n in self.nodes:
            n.cost = LARGE
        current = starting_node
        current.cost = 0

        done = False
        while not done:
            neighbors = self.__get_unvisited_neighbors(current)
            self.__update_costs_for_neighbors(current, neighbors)
            self.visited.append(current)
            if not len(self.visited) == self.num_nodes:
                current = self.unvisited_nodes[0]
            else:
                done = True
        for n in self.nodes:
            self.shortest_paths[starting_node.id, n.id] = n.cost
            self.shortest_paths[n.id, starting_node.id] = n.cost

    def __get_unvisited_neighbors(self, current: Node) -> List[Node]:
        return [self.get_node(i) for i in current.adj_list if self.get_node(i) not in self.visited]

    def __update_costs_for_neighbors(self, current: Node, neighbors: List[Node]):
        for neighbor in neighbors:
            neighbor.cost = min(neighbor.cost,
                                current.cost + self.edge_costs[current.id, neighbor.id])


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
        self.nodes = [(Node(i, [self.name_to_id[n] for n in v.adj_valves])) for i, v in enumerate(self.valves)]
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