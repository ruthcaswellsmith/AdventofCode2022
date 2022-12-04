from abc import ABC, abstractmethod
from enum import Enum

from utils import read_file


class Outcome(int, Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


class Shape(int, Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Round(ABC):
    THEIR_SHAPE = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}

    def __init__(self, first_letter: str, second_letter: str):
        self.their_shape = self.THEIR_SHAPE[first_letter]
        self.second_letter = second_letter

    @property
    @abstractmethod
    def my_shape(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self):
        raise NotImplementedError

    @property
    def points(self) -> int:
        return self.my_shape + self.outcome


class RoundPt1(Round):
    MY_SHAPE = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}

    @property
    def my_shape(self):
        return self.MY_SHAPE[self.second_letter]

    @property
    def outcome(self):
        if self.their_shape == self.my_shape:
            return Outcome.DRAW
        if self.their_shape == Shape.ROCK:
            return Outcome.WIN if self.my_shape == Shape.PAPER else Outcome.LOSS
        elif self.their_shape == Shape.PAPER:
            return Outcome.WIN if self.my_shape == Shape.SCISSORS else Outcome.LOSS
        else:
            return Outcome.WIN if self.my_shape == Shape.ROCK else Outcome.LOSS


class RoundPt2(Round):
    OUTCOME = {'X': Outcome.LOSS, 'Y': Outcome.DRAW, 'Z': Outcome.WIN}

    @property
    def my_shape(self):
        if self.outcome == Outcome.DRAW:
            return self.their_shape
        elif self.outcome == Outcome.WIN:
            return Shape.ROCK if self.their_shape == Shape.SCISSORS else \
                Shape.PAPER if self.their_shape == Shape.ROCK else \
                Shape.SCISSORS
        else:
            return Shape.ROCK if self.their_shape == Shape.PAPER else \
                Shape.PAPER if self.their_shape == Shape.SCISSORS else \
                Shape.SCISSORS

    @property
    def outcome(self):
        return self.OUTCOME[self.second_letter]


if __name__ == '__main__':
    filename = 'input/day2.txt'
    data = read_file(filename)

    rounds = [RoundPt1(line[0], line[2]) for line in data]
    print(f"The answer to part 1 is {sum([round.points for round in rounds])}")

    rounds = [RoundPt2(line[0], line[2]) for line in data]
    print(f"The answer to part 2 is {sum([round.points for round in rounds])}")
