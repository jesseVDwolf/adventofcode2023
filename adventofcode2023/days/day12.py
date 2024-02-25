from typing import Optional
from adventofcode2023 import Day, Result
from copy import deepcopy
from collections import Counter
from itertools import product, groupby

class Day12(Day):

    def __init__(self, puzzle_input: Optional[str] = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 12
    
    @staticmethod
    def _get_possible_rows(row_of_springs: str) -> list[str]:
        """Produce all possible combinations of groups for a row. Resolve the ? to a # or .

        Example:

        row_of_springs = '???.###'
        output =
            [ ....### ]
            [ ..#.### ]
            [ .#..### ]
            [ #...### ]
            [ .##.### ]
            [ ##..### ]
            [ #.#.### ]
            [ ###.### ]

        Args:
            row_of_springs (str): string containing characters representing spring states

        Returns:
            list[str]: possible rows
        """
        assert all( c in '?#.' for c in row_of_springs )

        possible_rows: list[str] = []
        unknown_count = Counter(row_of_springs)['?']
        for combination in product('#.', repeat=unknown_count):

            unknown_idx = 0
            row = deepcopy(row_of_springs)
            for idx, c in enumerate(row_of_springs):
                if c == '?':
                    row = row[:idx] + combination[unknown_idx] + row[idx + 1:]
                    unknown_idx += 1

            possible_rows.append(row)
        
        return possible_rows
    
    @staticmethod
    def _get_rows_passed(possible_rows: list[str], group_sizes: list[int]) -> list[str]:
        rows_passed: list[str] = []
        for row in possible_rows:
            
            sizes_found: list[int] = []
            for type_, group in groupby(row):

                if type_ == '#':
                    group = list(group)
                    sizes_found.append(len(group))

            
            if group_sizes == sizes_found:
                rows_passed.append(row)
        
        return rows_passed
    
    def solve_part_one(self) -> Result:
        arrangements: list[int] = []
        for line in self._puzzle_input.split('\n'):
            row_of_strings, group_size_string = line.split(' ')
            group_sizes = [ int(n) for n in group_size_string.split(',') ]

            possible_rows = self._get_possible_rows(row_of_strings)
            rows_passed = self._get_rows_passed(possible_rows, group_sizes)

            arrangements.append(len(rows_passed))
        
        return sum(arrangements)
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()

