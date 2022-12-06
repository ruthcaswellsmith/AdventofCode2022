from queue import Queue

from utils import read_file, Part


class Datastream:
    def __init__(self, text: str, part: Part):
        self.part = part
        self.datastream = text
        self.pos = 0
        self.queue = Queue()
        [self.__add_to_queue() for i in range(self.len_queue)]

    @property
    def location_of_marker(self):
        return self.pos + 1

    @property
    def len_queue(self):
        return 4 if self.part == Part.PT1 else 14

    @property
    def type_of_marker(self):
        return 'start-of-packet' if self.part == Part.PT1 else 'start-of-message'

    @property
    def found_marker(self) -> bool:
        return len(set([self.queue.queue[i] for i in range(self.len_queue)])) == self.len_queue

    def __add_to_queue(self):
        self.pos += 1
        if self.queue.qsize() == self.len_queue:
            self.queue.get()
        self.queue.put(self.datastream[self.pos])

    def find_marker(self) -> int:
        while not self.found_marker:
            self.__add_to_queue()
        return self.pos


if __name__ == '__main__':
    filename = 'input/Day6.txt'
    data = read_file(filename)

    datastream = Datastream(data[0], Part.PT1)
    datastream.find_marker()
    print(f"The {datastream.type_of_marker} marker is located at {datastream.location_of_marker}")

    datastream = Datastream(data[0], Part.PT2)
    datastream.find_marker()
    print(f"The {datastream.type_of_marker} marker is located at {datastream.location_of_marker}")
