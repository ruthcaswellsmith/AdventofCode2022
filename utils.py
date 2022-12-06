from enum import Enum, auto


def read_file(file):
    with open(file, 'r') as f:
        return f.read().rstrip('\n').split('\n')


class Part(str, Enum):
    PT1 = auto()
    PT2 = auto()
