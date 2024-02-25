from copy import deepcopy
from typing import Optional
from adventofcode2023.day import Day, Result

from math import dist

def gcd(a: int, b: int) -> int:
    """The greatest common divisor, or gcd, of integers a and b, at least one which is nonzero, is the greatest positive integer d that is a divisor of both a and b. 

    Args:
        a (int): Integer a
        b (int): Integer b

    Returns:
        int: The greatest common divisor
    """
    while b > 0:
        a, b = b, a % b

    return a


class Day9(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
    
    @property
    def day(self) -> int:
        return 9
    
    @staticmethod
    def get_last_value(seq: list[int]) -> int:
        if not any( n != 0 for n in seq):
            return 0
        
        return seq[-1] + Day9.get_last_value([ seq[i + 1] - seq[i] for i in range(len(seq) - 1) ])
    
    def solve_part_one(self) -> Result:
        sequences = [
            [ int(n) for n in line.split() ] for line
            in self._puzzle_input.split("\n") if line
        ]

        return sum(self.get_last_value(i) for i in sequences)

    
    def solve_part_two(self) -> Result:
        sequences = [
            [ int(n) for n in line.split() ] for line
            in self._puzzle_input.split("\n") if line
        ]
        
        return sum(self.get_last_value(i[::-1]) for i in sequences)


if __name__ == '__main__':
    
    day = Day9()
    print(day.solve_part_one())
    print(day.solve_part_two())

