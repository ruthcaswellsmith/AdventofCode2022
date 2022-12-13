from __future__ import annotations
from enum import Enum, auto
from typing import List, Union
import numpy as np
from functools import total_ordering

from utils import read_file

RIGHT_BRACKET = ']'
LEFT_BRACKET = '['
COMMA = ','


class OrderType(str, Enum):
    LESS_THAN = auto()
    GREATER_THAN = auto()


@total_ordering
class Packet:
    def __init__(self, item: List):
        self.item = item

    def __lt__(self, other):
        return self.get_order(self.item, other.item) == OrderType.LESS_THAN

    def __eq__(self, other):
        return self.item == other.item

    def get_order(self, left: List, right: List) -> Union[None, OrderType]:
        result = None
        l_ind, r_ind = 0, 0
        len_l, len_r = len(left), len(right)
        while not result and l_ind < len_l and r_ind < len_r:
            l, l_ind = self.__increment(left, l_ind)
            r, r_ind = self.__increment(right, r_ind)
            if isinstance(r, int) and isinstance(l, int):
                result = OrderType.LESS_THAN if l < r else OrderType.GREATER_THAN if r < l else None
            else:
                result = self.get_order(
                    [l] if isinstance(r, list) and isinstance(l, int) else l,
                    [r] if isinstance(l, list) and isinstance(r, int) else r
                )
        if result:
            return result
        if l_ind == len_l and r_ind < len_r:
            return OrderType.LESS_THAN
        if r_ind == len_r and l_ind < len_l:
            return OrderType.GREATER_THAN

    @staticmethod
    def __increment(text: List, ind: int):
        return text[ind], ind + 1


class Pair:
    def __init__(self, data: List[str]):
        self.left = Packet(eval(data[0]))
        self.right = Packet(eval(data[1]))


class DistressSignal:
    DIVIDER_PACKETS = [Packet([[2]]), Packet([[6]])]

    def __init__(self, data: List[str]):
        self.pairs = [Pair([data[3*i], data[3*i+1]]) for i in range(len(data)//3+1)]
        self.packets = [Packet(eval(data[i])) for i in range(len(data)) if data[i]]

    @property
    def answer_pt1(self):
        return sum([i+1 for i, pair in enumerate(self.pairs) if pair.left < pair.right])

    @property
    def answer_pt2(self):
        return np.prod([sorted(self.packets + self.DIVIDER_PACKETS).index(packet) + 1 for
                        packet in self.DIVIDER_PACKETS])


if __name__ == '__main__':
    filename = 'input/day13.txt'
    data = read_file(filename)

    distress_signal = DistressSignal(data)
    print(f"The answer to Pt 1 is {distress_signal.answer_pt1}")
    print(f"The answer to Pt 2 is {distress_signal.answer_pt2}")
