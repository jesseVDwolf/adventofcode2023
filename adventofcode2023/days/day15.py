from typing import Optional
from adventofcode2023.day import Day, Result

def hash_(s: str) -> int:
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v

class Day15(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
    
    @property
    def day(self) -> int:
        return 15

    def solve_part_one(self) -> Result:
        return sum( hash_(seq) for seq in self._puzzle_input.split(',') )
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()


if __name__ == '__main__':
    example_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    day = Day15()
    print(day.solve_part_one())
