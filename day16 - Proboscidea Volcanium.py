from __future__ import annotations
from typing import List, Tuple, Dict
from collections import namedtuple

from utils import read_file
LARGE = 1_000_000

NC = namedtuple('ND', 'name cost')


class Node:
    def __init__(self, name: str, adj_list: List[NC]):
        self.name = name
        self.adj_list = adj_list
        self.cost = LARGE
        self.visited = False


class Graph:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.shortest_paths: Dict[Node, List[NC]] = {}

    @property
    def num_nodes(self):
        return len(self.nodes)

    @staticmethod
    def __get_edge_cost(adj_list: List[NC], node: Node):
        return next(iter(t.edge_cost for t in adj_list if t.name == node.name), 0)

    def get_node(self, name: str):
        return next(iter([n for n in self.nodes if n.name == name]), None)

    def find_all_shortest_paths(self):
        for node in self.nodes:
            self.shortest_paths[node] = self.__find_shortest_paths(node)

    def __find_shortest_paths(self, starting_node: Node):
        current, visited = starting_node, []
        for n in self.nodes:
            n.cost = LARGE
            n.visited = False
        current.cost = 0

        done = False
        while not done:
            neighbors = self.__get_unvisited_neighbors(current, visited)
            self.__update_costs_for_neighbors(neighbors)
            visited.append(current)
            if not len(visited) == self.num_nodes:
                self.__update_current(visited)
            else:
                done = True
        return [ND(name=v.name, distance=v.cost) for v in visited if v.name != starting_node.name]

    def __get_unvisited_neighbors(self, current: Node, visited: List[Node]) -> List[Node]:
        return [self.get_node(n.name) for n in current.adj_list if n not in visited]

    def __update_costs_for_neighbors(self, current: Node, neighbors: List[Node]):
        for neighbor in neighbors:
            neighbor.cost = min(neighbor.cost, current.cost + self.__get_edge_cost(current.adj_list, neighbor))

    def __update_current(self, visited: List[Node]):
        unvisited_neighbors = [n for n in self.nodes if not n.visited]
        unvisited_neighbors.sort(key=lambda n: n.cost)
        return unvisited_neighbors[0]



# class Valve:
#     def __init__(self, line: str):
#         self.name = line[line.index('Valve ')+6:line.index('Valve ')+8]
#         self.flow_rate = eval(line[line.index('=')+1:line.index(';')])
#         self.adj_list = line[line.index("valves ")+7:].split() if 'valves' in line else \
#             line[line.index("valve ") + 6:].split()
#         self.adj_list = [n.replace(',', '') for n in self.adj_list]
#         self.cost = LARGE
#         self.visited = False


class Tunnels:
    def __init__(self, data: List[str]):
        self.valves = [Valve(line) for line in data]
        self.tsp_valves = [v for v in self.valves if v.name == 'AA'] + [v for v in self.valves if v.flow_rate > 0]
        for v in self.tsp_valves:
            self.__find_shortest_paths(v)
        self.build_tsp_graph()
        print('h')

    def build_tsp_graph(self):
        for v in self.tsp_valves:
            # for n in self.tsp_valves:
            #     if n.name != v.name:
            #         print('h')
            v.adj_list = [(n.name, abs(n.cost - v.cost)) for n in self.tsp_valves if n.name != v.name]
            print('h')

    @property
    def num_valves(self):
        return len(self.valves)

    @property
    def visited_valves(self):
        return len([v for v in self.valves if v.visited])

    def __find_shortest_paths(self, starting_valve: Valve):
        current, visited = starting_valve, []
        done = False
        while not done:
            neighbors = self.__get_unvisited_neighbors(current, visited)
            self.__update_costs_for_neighbors(neighbors)
            visited.append(current)
            if not len(visited) == self.num_valves:
                self.__update_current(visited)
            else:
                done = True


if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    tunnels = Tunnels(data)
    print('h')