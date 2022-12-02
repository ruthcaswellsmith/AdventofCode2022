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


THEIR_SHAPE = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
MY_SHAPE = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}
OUTCOME = {'X': Outcome.LOSS, 'Y': Outcome.DRAW, 'Z': Outcome.WIN}


class Round:
    def __init__(self, my_shape: Shape, outcome: Outcome):
        self.my_shape = my_shape
        self.outcome = outcome

    @property
    def points(self) -> int:
        return self.my_shape + self.outcome


class RoundPt1(Round):
    def __init__(self, first_letter: str, second_letter: str):
        self.their_shape = THEIR_SHAPE[first_letter]
        self.my_shape = MY_SHAPE[second_letter]
        super().__init__(self.my_shape,
                         self.get_outcome())

    def get_outcome(self):
        if self.their_shape == self.my_shape:
            return Outcome.DRAW
        if self.their_shape == Shape.ROCK:
            return Outcome.WIN if self.my_shape == Shape.PAPER else Outcome.LOSS
        elif self.their_shape == Shape.PAPER:
            return Outcome.WIN if self.my_shape == Shape.SCISSORS else Outcome.LOSS
        else:
            return Outcome.WIN if self.my_shape == Shape.ROCK else Outcome.LOSS


class RoundPt2(Round):
    def __init__(self, first_letter: str, second_letter: str):
        self.their_shape = THEIR_SHAPE[first_letter]
        self.outcome = OUTCOME[second_letter]
        super().__init__(self.get_my_shape(),
                         self.outcome)

    def get_my_shape(self):
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


if __name__ == '__main__':
    filename = 'input/day2.txt'
    data = read_file(filename)

    rounds = [RoundPt1(line[0], line[2]) for line in data]
    print(f"The answer to part 1 is {sum([round.points for round in rounds])}")

    rounds = [RoundPt2(line[0], line[2]) for line in data]
    print(f"The answer to part 2 is {sum([round.points for round in rounds])}")
