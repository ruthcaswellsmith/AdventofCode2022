from __future__ import annotations
from typing import List, Tuple, Dict
from collections import namedtuple

from utils import read_file
LARGE = 1_000_000

NC = namedtuple('NC', 'name cost')


class Node:
    def __init__(self, name: str, adj_list: List[NC]):
        self.name = name
        self.adj_list = adj_list
        self.cost = LARGE


class Graph:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.shortest_paths: Dict[str, List[NC]] = {}
        self.visited = List[Node]

    @property
    def num_nodes(self):
        return len(self.nodes)

    @property
    def unvisited_nodes(self):
        unvisited = [n for n in self.nodes if n not in self.visited]
        unvisited.sort(key=lambda n: n.cost)
        return unvisited

    @staticmethod
    def __get_edge_cost(adj_list: List[NC], node: Node):
        return next(iter(t.cost for t in adj_list if t.name == node.name), 0)

    def get_node(self, name: str):
        return next(iter([n for n in self.nodes if n.name == name]), None)

    def find_all_shortest_paths(self):
        for node in self.nodes:
            self.shortest_paths[node.name] = self.__find_shortest_paths(node)

    def __find_shortest_paths(self, starting_node: Node):
        current = starting_node
        self.visited = []
        for n in self.nodes:
            n.cost = LARGE
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
        return [NC(name=n.name, cost=n.cost) for n in self.nodes if n.name != starting_node.name]

    def __get_unvisited_neighbors(self, current: Node) -> List[Node]:
        return [self.get_node(n.name) for n in current.adj_list if n not in self.visited]

    def __update_costs_for_neighbors(self, current: Node, neighbors: List[Node]):
        for neighbor in neighbors:
            neighbor.cost = min(neighbor.cost, current.cost + self.__get_edge_cost(current.adj_list, neighbor))


class Valve(Node):
    def __init__(self, line: str):
        name = line[line.index('Valve ')+6:line.index('Valve ')+8]
        adj_nodes = line[line.index("valves ")+7:].split() if 'valves' in line else \
            line[line.index("valve ") + 6:].split()
        adj_list = [NC(n.replace(',', ''), 1) for n in adj_nodes]
        super().__init__(name, adj_list)
        self.flow_rate = eval(line[line.index('=')+1:line.index(';')])


class Tunnels:
    def __init__(self, data: List[str]):
        self.graph_with_all_valves = Graph([Valve(line) for line in data])
        self.graph_with_all_valves.find_all_shortest_paths()
        self.nonzero_valves = [v for v in self.graph_with_all_valves.nodes if v.flow_rate > 0]



if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    tunnels = Tunnels(data)
    print('h')