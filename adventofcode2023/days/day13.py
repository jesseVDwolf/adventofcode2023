from typing import Optional
from adventofcode2023.day import Day, Result
from textwrap import dedent
import numpy as np

class Day13(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 13
    
    def get_reflection_point_vert(self, p: np.ndarray) -> int | None:

        def is_mirror(p: np.ndarray, i: int, j: int) -> bool:
            # a valid reflection means the 2D matrix is equal to its mirrored version
            return np.array_equal(np.flip(p[::, i:j+1], axis=1), p[::, i:j+1])
        
        # loop over pairs of columns from left to right
        # if you find two pairs that match, check the left
        # and right side if they're mirrored.
        for i in range(p.shape[1] - 1):
            if np.array_equal(p[::,i], p[::,i+1]):
                # check right if already past halfway point
                if i >= (p.shape[1] // 2):
                    x = p.shape[1] - ((p.shape[1] - i - 1) * 2)
                    if is_mirror(p, x, p.shape[1]):
                        return i + 1

                # else check left side
                else:
                    if is_mirror(p, 0, i * 2 + 1):
                        return i + 1
    
    def get_reflection_point_hori(self, p: np.ndarray) -> int | None:

        def is_mirror(p: np.ndarray, i: int, j: int) -> bool:
            # a valid reflection means the 2D matrix is equal to its mirrored version
            return np.array_equal(np.flip(p[i:j+1,::], axis=0), p[i:j+1,::])
        
        # loop over pairs of rows from top to bottom
        # if you find two pairs that match, check the top
        # and bottom side they're mirrored
        for i in range(p.shape[0] - 1):
            if np.array_equal(p[i,::], p[i+1,::]):
                # check bottom if already past halfway point
                if i >= (p.shape[0] // 2):
                    x = p.shape[0] - ((p.shape[0] - i - 1) * 2)
                    if is_mirror(p, x, p.shape[0]):
                        return i + 1
                
                # else check top
                else:
                    if is_mirror(p, 0, i * 2 + 1):
                        return i + 1

    def solve_part_one(self) -> Result:
        notes_summary = 0
        for pattern in self._puzzle_input.split('\n\n'):
            p = np.array(
                object=[ list(s) for s in pattern.split('\n') ],
                dtype=np.dtype('U1')
            )

            a = self.get_reflection_point_vert(p)
            b = self.get_reflection_point_hori(p)
            assert not all( x == None for x in [a, b])
            assert any(x != None for x in [a, b])
            if a is None:
                notes_summary += (100 * b)
            else:
                notes_summary += a

        return notes_summary
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()
    


if __name__ == '__main__':
    example_input = dedent("""
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.""").strip()

    day = Day13()
    print(day.solve_part_one())

