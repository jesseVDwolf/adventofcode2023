from typing import Optional
from adventofcode2023.day import Day, Result
from itertools import product

class Day3(Day):

    def __init__(self, puzzle_input: Optional[str] = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 3
    
    def _puzzle_input_to_grid(self) -> list[list[str]]:
        return [
            [ c for c in line ]
            for line in self._puzzle_input.split('\n')
        ]
    
    @staticmethod
    def _parse_number_from_grid(chars: list[str], x: int) -> int:
        """Find the number in the list of chars. Set all digits to '.' so they're
        ignored the next time.

        Args:
            chars (list[str]): Row passed from the grid
            x (int): x on the 1D line

        Returns:
            int: number
        """
        def update_list_inplace(start_idx: int, end_idx: int):
            range_ = range(start_idx, end_idx)
            for idx in range_:
                chars[idx] = '.'

        start_idx = x
        while start_idx >= 0 and chars[start_idx].isdigit():
            start_idx -= 1
        
        end_idx = x
        width = len(chars)
        while end_idx < width and chars[end_idx].isdigit():
            end_idx += 1

        num = int(''.join(chars[start_idx + 1: end_idx]))
        update_list_inplace(start_idx, end_idx)
        return num


    def _has_number_adjacent(self, grid: list[list[str]], x: int, y: int) -> list[int]:
        """If the grid has digits adjacent horizontally, vertically or diagonally, return
        a list of all numbers found. If nothing found return None.

        Args:
            grid (list[list[str]]): grid
            x (int): current x location
            y (int): current y location

        Returns:
            list[int] | None: None if no digits found, else list of whole numbers found
        """
        if len(grid) == 0 or len(grid[0]) == 0:
            raise ValueError(f"Invalid grid.")

        width = len(grid[0])
        height = len(grid)
        numbers: list[int] = []

        for pos in product([-1, 0, 1], repeat=2):
            x_incr, y_inr = pos
            x_check, y_check = (x + x_incr, y + y_inr)
            if (
                x_check >= 0 and x_check < width and
                y_check >= 0 and y_check < height
            ):
                if grid[y_check][x_check].isdigit():
                    num = self._parse_number_from_grid(grid[y_check], x_check)
                    numbers.append(num)
        
        return numbers
    
    def solve_part_one(self) -> Result:
        numbers: list[int] = []
        grid = self._puzzle_input_to_grid()
        for y, row in enumerate(grid):

            for x, c in enumerate(row):

                if not c.isdigit() and c != '.':
                    if nums := self._has_number_adjacent(grid, x, y):
                        numbers.extend(nums)
        
        return sum(numbers)
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()
