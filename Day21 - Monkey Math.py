from __future__ import annotations

import operator
from typing import List
from utils import read_file, Operator, Part

OPS = {
    Operator.ADD: operator.add,
    Operator.SUBTRACT: operator.sub,
    Operator.MULTIPLY: operator.mul,
    Operator.DIVIDE: operator.truediv,
}

ROOT = 'root'
HUMN = 'humn'
LEFT_PAREN = '('
RIGHT_PAREN = ')'


class Monkey:
    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text

    @property
    def knows_it_all(self):
        return self.text.isdigit()

    @property
    def words(self):
        return self.text.split()


class Monkeys:

    def __init__(self, data: List[str], part: Part):
        self.part = part
        self.monkeys = {words[0]: Monkey(words[0], words[1]) for line in data if \
                        (words := [w.strip() for w in line.split(':')])}

    def build_expression(self, id: str) -> str:
        monkey = self.monkeys[id]
        if monkey.knows_it_all:
            return monkey.text if self.part == Part.PT1 else \
                monkey.text if monkey.id != HUMN else HUMN
        else:
            return LEFT_PAREN + \
                   self.build_expression(monkey.words[0]) + \
                   monkey.words[1] + \
                   self.build_expression(monkey.words[2]) + \
                    RIGHT_PAREN

    def find_humn(self):
        exp1 = self.build_expression(self.monkeys[ROOT].words[0])
        exp2 = self.build_expression(self.monkeys[ROOT].words[2])
        return self.unwind(
            eval(exp1) if HUMN in exp2 else eval(exp2),
            exp1 if HUMN in exp1 else exp2)

    def unwind(self, known: int, unknown: str):
        exp1, exp2, op = self.__divide_unknown(unknown)
        if HUMN in exp1:
            new_known = int(OPS[self.__get_inverse_operator(op)](known, eval(exp2)))
            return new_known if exp1 == HUMN else self.unwind(new_known, exp1)
        else:
            new_known = int(OPS[self.__get_inverse_operator(op)](known, eval(exp1))) if \
                op in [Operator.ADD, Operator.MULTIPLY] else \
                int(OPS[op](eval(exp1), known))
            return new_known if exp2 == HUMN else self.unwind(new_known, exp2)

    def __divide_unknown(self, text: str):
        text = self.__strip_outer_parens(text)
        op_ind = self.__find_op(text)
        return text[:op_ind], text[op_ind+1:], Operator(text[op_ind])

    @staticmethod
    def __find_op(text: str):
        if LEFT_PAREN not in text:
            ind = 0
            while ind < len(text):
                if not (text[ind].isalpha() or text[ind].isnumeric()):
                    return ind
                ind += 1

        num_paren = 1 if text[0] == LEFT_PAREN else 0
        ind = 1
        while num_paren > 0:
            num_paren += 1 if text[ind] == LEFT_PAREN else -1 if text[ind] == RIGHT_PAREN else 0
            ind += 1
        return ind

    @staticmethod
    def __get_inverse_operator(op: Operator):
        return Operator.SUBTRACT if op == Operator.ADD else \
            Operator.ADD if op == Operator.SUBTRACT else \
            Operator.MULTIPLY if op == Operator.DIVIDE else \
            Operator.DIVIDE

    @staticmethod
    def __strip_outer_parens(text: str):
        return text[1:len(text) - 1] if LEFT_PAREN in text else text


if __name__ == '__main__':
    filename = 'input/day21.txt'
    data = read_file(filename)

    monkeys = Monkeys(data, Part.PT1)
    print(f'The answer to Pt 1 is {int(eval(monkeys.build_expression(ROOT)))}')

    monkeys = Monkeys(data, Part.PT2)
    print(f'The answer to Pt 2 is {monkeys.find_humn()}')
