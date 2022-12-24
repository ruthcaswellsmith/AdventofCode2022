from __future__ import annotations

from typing import List

from utils import read_file, CircularLinkedList, Node, Part


class File:
    DECRYPTION_KEY = 811589153

    def __init__(self, data: List[str], part: Part):
        if part == Part.PT1:
            self.linked_list = CircularLinkedList([int(data[i]) for i in range(len(data))])
        else:
            self.linked_list = CircularLinkedList([self.DECRYPTION_KEY * int(data[i]) for i in range(len(data))])
        self.zero = next(iter([node for node in self.linked_list.nodes if node.value == 0]), None)

    @property
    def length(self):
        return len(self.linked_list.nodes)

    @property
    def answer(self):
        nums = []
        for num in [1000, 2000, 3000]:
            self.linked_list.current = self.zero
            nums.append(self.linked_list.get_node(num % self.length).value)
        return sum(nums)

    def mix(self):
        for node in self.linked_list.nodes:
            self.move_node(node)

    def move_node(self, node: Node):
        if node.value == 0:
            return

        self.linked_list.current = self.linked_list.nodes[node.id]
        pre_node = self.linked_list.get_node(node.value % (self.length - 1))
        post_node = pre_node.next
        if node.value > 0:
            node.previous.next = node.next
            post_node.previous = node
            pre_node.next = node
            node.next.previous = node.previous
        else:
            node.next.previous = node.previous
            pre_node.next = node
            post_node.previous = node
            node.previous.next = node.next
        node.previous = pre_node
        node.next = post_node


if __name__ == '__main__':
    filename = 'input/day20.txt'
    data = read_file(filename)

    file = File(data, Part.PT1)
    file.mix()
    print(f'The answer to Pt 1 is {file.answer}')

    file = File(data, Part.PT2)
    for _ in range(10):
        file.mix()
    print(f'The answer to Pt 2 is {file.answer}')

