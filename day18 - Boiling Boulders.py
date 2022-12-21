from __future__ import annotations
from typing import List
import sys

from utils import read_file, XYZ, Orientation

sys.setrecursionlimit(10_000)


class Side:
    def __init__(self, orientation: Orientation, xyz: XYZ):
        self.orientation = orientation
        self.xyz = xyz

    def __eq__(self, other):
        return True if self.orientation == other.orientation and self.xyz == other.xyz else False

    def __hash__(self):
        return hash(self.orientation) + hash(self.xyz)

    @property
    def name(self):
        return f"{self.orientation}-{self.xyz.id}"


class Cube:
    def __init__(self, xyz: XYZ):
        self.xyz = xyz

    @property
    def id(self):
        return self.xyz.id

    @property
    def neighbors(self):
        return [
            Cube(XYZ((self.xyz.x + 1, self.xyz.y, self.xyz.z))),
            Cube(XYZ((self.xyz.x - 1, self.xyz.y, self.xyz.z))),
            Cube(XYZ((self.xyz.x, self.xyz.y + 1, self.xyz.z))),
            Cube(XYZ((self.xyz.x, self.xyz.y - 1, self.xyz.z))),
            Cube(XYZ((self.xyz.x, self.xyz.y, self.xyz.z + 1))),
            Cube(XYZ((self.xyz.x, self.xyz.y, self.xyz.z - 1)))
        ]

    @property
    def sides(self):
        return [
            Side(Orientation.X, XYZ((self.xyz.x, self.xyz.y, self.xyz.z))),
            Side(Orientation.X, XYZ((self.xyz.x + 1, self.xyz.y, self.xyz.z))),
            Side(Orientation.Y, XYZ((self.xyz.x, self.xyz.y, self.xyz.z))),
            Side(Orientation.Y, XYZ((self.xyz.x, self.xyz.y + 1, self.xyz.z))),
            Side(Orientation.Z, XYZ((self.xyz.x, self.xyz.y, self.xyz.z))),
            Side(Orientation.Z, XYZ((self.xyz.x, self.xyz.y, self.xyz.z + 1)))
        ]

    def __eq__(self, other):
        return True if self.xyz == other.xyz else False


class Lava:
    def __init__(self, data: List[str]):
        self.cubes = [Cube(XYZ(tuple([int(ele) for ele in line.split(',')]))) for line in data]
        self.x_max = max([cube.xyz.x for cube in self.cubes])
        self.y_max = max([cube.xyz.y for cube in self.cubes])
        self.z_max = max([cube.xyz.z for cube in self.cubes])
        self.visited = []
        self.surface_area = self.calc_surface_area(Cube(XYZ((0, 0, 0))))

    def calc_surface_area(self, cube: Cube):
        if cube in self.cubes:
            return 1
        self.visited.append(cube)
        return sum([self.calc_surface_area(neighbor) for neighbor in cube.neighbors if
                    neighbor not in self.visited and self.__in_cuboid(neighbor)])

    def __in_cuboid(self, cube):
        return True if -1 <= cube.xyz.x <= self.x_max + 1 and \
                       -1 <= cube.xyz.y <= self.y_max + 1 and \
                       -1 <= cube.xyz.z <= self.z_max + 1 else False

    @property
    def exposed_sides(self):
        exposed_sides = set()
        [[exposed_sides.remove(side) if side in exposed_sides else exposed_sides.add(side) \
            for side in set(cube.sides)] for cube in self.cubes]
        return exposed_sides


if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    lava = Lava(data)
    print(f'The answer to Part 1 is {len(lava.exposed_sides)}')

    print(f'The answer to Part 2 is {lava.surface_area}')
