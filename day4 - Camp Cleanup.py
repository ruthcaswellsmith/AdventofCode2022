from utils import read_file


class Assignment:
    def __init__(self, assignment: str):
        sections = [int(sections) for sections in assignment.split('-')]
        self.sections = set([i for i in range(sections[0], sections[1]+1)])


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
        return len(self.assignment1.sections.intersection(self.assignment2.sections)) > 0

    @staticmethod
    def __contains(assignment1, assignment2):
        return assignment1.sections.issubset(assignment2.sections)


if __name__ == '__main__':
    filename = 'input/day4.txt'
    data = read_file(filename)

    pairs = [Pair(line) for line in data]
    print(f"The answer to part 1 is {sum([pair.one_contains_another for pair in pairs])}")
    print(f"The answer to part 2 is {sum([pair.assignments_overlap for pair in pairs])}")
