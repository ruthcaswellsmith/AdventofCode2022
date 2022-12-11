from typing import List
from enum import Enum, auto
import math
from decimal import Decimal


def read_file(file):
    with open(file, 'r') as f:
        return f.read().rstrip('\n').split('\n')


class Part(str, Enum):
    PT1 = auto()
    PT2 = auto()


class Direction(str, Enum):
    EAST = auto()
    WEST = auto()
    NORTH = auto()
    SOUTH = auto()


def primefactors(n: Decimal) -> List[int]:
    # Rewritten based on algorithm from pythonpool
    factors = []

    # even number divisible
    while n % 2 == 0:
        factors.append(2),
        n = n // 2

    # n became odd
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i

    if n > 2:
        factors.append(n)

    return factors
