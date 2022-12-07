from queue import LifoQueue
from typing import List

from anytree import AnyNode, PreOrderIter

from utils import read_file


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Line:
    CHANGE_DIR = 'cd'
    LIST = 'ls'
    MOVE_UP = '..'
    DIR = 'dir'

    def __init__(self, text: str):
        self.text = text
        self.words = text.split()

    @property
    def change_dir(self):
        return self.words[1] == self.CHANGE_DIR

    @property
    def move_up(self):
        return self.change_dir and self.words[2] == self.MOVE_UP

    @property
    def target_dir(self):
        return self.words[2]

    @property
    def is_file(self):
        return self.words[0].isdigit()

    @property
    def file(self):
        return File(name=self.words[1], size=int(self.words[0]))


class Directory(AnyNode):
    def __init__(self, id: str, parent=None, children=None, files=[]):
        super().__init__(id=id, parent=parent, children=children)
        self.files = files

    @property
    def size(self):
        return sum([file.size for file in self.files]) + sum([dir.size for dir in self.children])


class TerminalOutput:
    MAX_SIZE = 100_000
    TOTAL_SPACE = 70_000_000
    NEEDED_SPACE = 30_000_000

    def __init__(self, lines: List[str]):
        self.lines = [Line(line) for line in lines]
        self.pos = 0
        self.queue = LifoQueue()

    @property
    def current_node(self):
        return None if self.queue.qsize() == 0 else self.queue.queue[self.queue.qsize()-1]

    @property
    def current_id(self):
        return "" if not self.current_node else self.current_node.id

    @property
    def num_lines(self):
        return len(self.lines)

    @property
    def root_dir(self):
        return self.queue.queue[0]

    @property
    def unused_space(self):
        return self.TOTAL_SPACE - self.root_dir.size

    @property
    def required_to_free(self):
        return self.NEEDED_SPACE - self.unused_space

    @property
    def answer_pt1(self):
        return sum([dir.size for dir in
                    PreOrderIter(self.root_dir, filter_=lambda n: n.size < self.MAX_SIZE)])

    @property
    def answer_pt2(self):
        return min([dir.size for dir in
                    PreOrderIter(self.root_dir, filter_=lambda n: n.size > self.required_to_free)])

    def process(self):
        while self.pos < self.num_lines:
            line = self.lines[self.pos]
            if line.move_up:
                self.queue.get()
            elif line.change_dir:
                self.queue.put(
                    Directory(id=self.current_id + line.target_dir, parent=self.current_node, files=[])
                )
            elif line.is_file:
                self.current_node.files.append(line.file)
            else:
                pass
            self.pos += 1


if __name__ == '__main__':
    filename = 'input/day7.txt'
    data = read_file(filename)

    terminal_output = TerminalOutput(data)
    terminal_output.process()
    print(f"The answer to Pt 1 is {terminal_output.answer_pt1}")
    print(f"The answer to Pt 2 is {terminal_output.answer_pt2}")
