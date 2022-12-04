from typing import Optional

from utils import read_file


class Assignment:
    def __init__(self, assignment: str):
        sections = assignment.split('-')
        self.sections = set([])
        self.beg = int(sections[0])
        self.end = int(sections[1])


class Pair:
    def __init__(self, pair: str):
        assignments = pair.split(',')
        self.assignment1 = Assignment(assignments[0])
        self.assignment2 = Assignment(assignments[1])

    @property
    def one_contains_another(self):
        return self.__contains(self.assignment1, self.assignment2) or \
               self.__contains(self.assignment2, self.assignment1)

    @property
    def assignments_overlap(self):
        return self.assignment1.beg <= self.assignment2.beg <= self.assignment1.end or \
               self.assignment1.beg <= self.assignment2.end <= self.assignment1.end or \
               self.assignment2.beg <= self.assignment1.end <= self.assignment2.end or \
               self.assignment2.beg <= self.assignment1.end <= self.assignment2.end

    def __contains(self, assignment1, assignment2):
        return assignment1.beg <= assignment2.beg and assignment1.end >= assignment2.end


if __name__ == '__main__':
    filename = 'input/day4.txt'
    data = read_file(filename)

    pairs = [Pair(line) for line in data]
    print(f"The answer to part 1 is {sum([pair.one_contains_another for pair in pairs])}")
    print(f"The answer to part 2 is {sum([pair.assignments_overlap for pair in pairs])}")
