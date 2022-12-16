from typing import List
from itertools import chain
from queue import LifoQueue


from utils import read_file, XYPair, EnhancedRange


class Sensor:
    X = 'x='
    Y = 'y='

    def __init__(self, line: str):
        self.pos = self.__get_xypair(line, 0)
        self.beacon = self.__get_xypair(line, 1)

    def __get_xypair(self, line: str, ind: int):
        x_str = self.__get_substrs(line, self.X, ind)
        y_str = self.__get_substrs(line, self.Y, ind)
        xsub = x_str[len(self.X):]
        xval = eval(xsub[:xsub.find(',')])
        ysub = y_str[len(self.Y):]
        yval = eval(ysub[:ysub.find(':')]) if ysub.find(':') >= 0 else eval(ysub)
        return XYPair((xval, yval))

    @staticmethod
    def __get_substrs(text: str, substr: str, ind: int):
        substrings = [text[i:] for i in range(len(text)) if text.startswith(substr, i)]
        return substrings[ind]

    @property
    def dist_from_beacon(self):
        return self.pos.manhattan(self.beacon)


class Readings:
    MULTIPLE = 4_000_000

    def __init__(self, data: List[str]):
        self.data = data
        self.sensors = [Sensor(line) for line in data]
        self.blocked: LifoQueue[EnhancedRange] = LifoQueue()

    def get_beacons(self, row):
        return [sensor.beacon.x for sensor in self.sensors if sensor.beacon.y == row]

    def answer_pt1(self, row):
        ranges = [self.blocked.queue[i].r for i in range(self.blocked.qsize())]
        blocked = set()
        [blocked.add(i) for i in chain(*ranges)]
        [blocked.remove(beacon) for beacon in self.get_beacons(row) if beacon in blocked]
        return len(blocked)

    def answer_pt2(self):
        for row in range(self.MULTIPLE):
            self.blocked = LifoQueue()
            self.get_blocked(row)
            if self.blocked.qsize() == 2:
                return self.MULTIPLE * (self.blocked.queue[0].r[-1] + 1) + row

    def get_blocked(self, row):
        ranges = []
        for sensor in self.sensors:
            x_delta = sensor.dist_from_beacon - abs(sensor.pos.y - row)
            if x_delta >= 0:
                ranges.append(EnhancedRange(range(sensor.pos.x - x_delta, sensor.pos.x + x_delta + 1)))
        ranges.sort()

        self.blocked.put(ranges[0])
        for r in ranges[1:]:
            last = self.blocked.get()
            if r.contains(last):
                self.blocked.put(r)
            elif r.overlaps(last):
                self.blocked.put(r.combine(last))
            else:
                [self.blocked.put(e) for e in [last, r]]


if __name__ == '__main__':
    filename = 'input/day15.txt'
    data = read_file(filename)

    ROW = 2_000_000
    readings = Readings(data)
    readings.get_blocked(ROW)
    print(f'The answer to Pt 1 is {readings.answer_pt1(ROW)}')
    print(f'The answer to Pt 2 is {readings.answer_pt2()}')
