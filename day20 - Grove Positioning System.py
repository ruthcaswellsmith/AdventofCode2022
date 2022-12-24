from __future__ import annotations

from typing import List

from utils import read_file, CircularLinkedList, Node


class File:
    def __init__(self, data: List[str]):
        self.linked_list = CircularLinkedList([int(data[i]) for i in range(len(data))])
        self.zero = next(iter([node for node in self.linked_list.nodes if node.value == 0]), None)
        self.length = len(self.linked_list.nodes)

    @property
    def answer_pt1(self):
        nums = []
        for num in [1000, 2000, 3000]:
            self.linked_list.current = self.zero
            nums.append(self.linked_list.get_node(num % self.length).value)
        return sum(nums)

    def mix(self):
        for node in self.linked_list.nodes:
            self.move_node(node)
            # current = self.linked_list.head
            # print(f"Moving Node {node.value}")
            # l = []
            # for i in range(len(self.linked_list.nodes)):
            #     l.append(current.value)
            #     current = current.next
            # print(l)
            # print('now in reverse')
            # l = []
            # current = self.linked_list.head
            # for i in range(len(self.linked_list.nodes)):
            #     l.append(current.value)
            #     current = current.previous
            # print(l)

    def move_node(self, node: Node):
        if node.value == 0:
            return

        self.linked_list.current = self.linked_list.nodes[node.id]
        if node.value > 0:
            pre_node = self.linked_list.get_node(node.value)
            post_node = pre_node.next
            node.previous.next = node.next
            post_node.previous = node
            pre_node.next = node
            node.next.previous = node.previous
        else:
            post_node = self.linked_list.get_node(node.value)
            pre_node = post_node.previous
            node.next.previous = node.previous
            pre_node.next = node
            post_node.previous = node
            node.previous.next = node.next
        node.previous = pre_node
        node.next = post_node


if __name__ == '__main__':
    filename = 'input/day20.txt'
    data = read_file(filename)

    file = File(data)
    file.mix()
    print(f'The answer to Pt 1 is {file.answer_pt1}')

    # Guessed 4207.  Too low.
