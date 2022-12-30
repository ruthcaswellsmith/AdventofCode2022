from __future__ import annotations

from typing import List
from utils import read_file

MINUS = "-"
DOUBLE_MINUS = "="
ZERO = '0'
FIVE = 5
MAX_DIGITS = 20


class FuelRequirements:
    def __init__(self, data: List[str]):
        self.place_values = {
            k: 5**k for k, v in enumerate(range(MAX_DIGITS))
        }
        self.lower_bounds = [1] + [FIVE ** (i+1) - sum([2 * FIVE**j for j in range(i+1)]) for i in range(MAX_DIGITS - 1)]
        self.upper_bounds = [sum([2 * FIVE**j for j in range(i)]) for i in range(1, MAX_DIGITS + 1)]
        self.decimals = [self.snafu_to_decimal(line) for line in data]
        print()

    @property
    def sum_requirements(self):
        return sum(self.decimals)

    @property
    def answer_pt1(self):
        return self.decimal_to_snafu(self.sum_requirements)

    def snafu_to_decimal(self, text: str):
        return sum([self.__convert_char(v[0], v[1]) for \
                    v in [(len(text)-i-1, text[i]) for i in range(len(text)-1, -1, -1)]])

    def __convert_char(self, place: int, char: str):
        return int(char) * self.place_values[place] if char.isdigit() else -self.place_values[place] if \
            char == MINUS else -2 * self.place_values[place]

    def decimal_to_snafu(self, num: int):
        snafu = ""
        most_sig_dig = next(iter([i for i in range(MAX_DIGITS) if self.lower_bounds[i] <= num <= self.upper_bounds[i]]))
        for i in range(most_sig_dig, -1, -1):
            upper_bound, lower_bound = self.upper_bounds[i], self.lower_bounds[i]
            multiple = 2 if abs(num) > (upper_bound - self.place_values[i]) else \
                1 if abs(num) >= lower_bound else 0
            if num < 0:
                dig = DOUBLE_MINUS if multiple == 2 else MINUS if multiple == 1 else ZERO
            else:
                dig = str(multiple)
            snafu += dig
            num -= multiple * self.place_values[i] if num > 0 else -multiple * self.place_values[i]
        return snafu


if __name__ == '__main__':
    filename = 'input/day25.txt'
    data = read_file(filename)

    fuel_requirements = FuelRequirements(data)
    print(f'The answer to Pt 1 is {fuel_requirements.answer_pt1}')
