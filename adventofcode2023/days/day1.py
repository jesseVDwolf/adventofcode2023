from adventofcode2023.day import Day, Result
from typing import Optional


class Day1(Day):
    DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    def __init__(self, puzzle_input: Optional[str] = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 1

    def solve_part_one(self) -> Result:
        """Find the numbers in the strings

        Returns:
            Result: _description_
        """
        numbers: list[int] = []
        for line in self._puzzle_input.split("\n"):
            idx1 = None
            for idx, c in enumerate(line):
                if c.isdigit():
                    idx1 = idx
                    break

            assert idx1 is not None, f"No digit found in line `{line}`."

            idx2 = None
            for idx, c in enumerate(line[idx + 1 :]):
                if c.isdigit():
                    idx2 = idx + idx1 + 1

            if idx2 is None:
                idx2 = idx1

            num = line[idx1] + line[idx2]
            numbers.append(int(num))

        return sum(numbers)

    def _find_first_digit(self, line: str) -> tuple[Optional[str], Optional[int]]:
        """Example input 'zoneight234'

        Args:
            line (str): _description_

        Returns:
            str: _description_
        """
        d1 = None
        idx1 = None
        for idx, c in enumerate(line):
            if c.isdigit():
                idx1 = idx
                d1 = line[idx]
                break

            for d, digit in enumerate(self.DIGITS):
                size = len(digit)
                if line[idx : idx + size] == digit:
                    idx1 = idx
                    d1 = str(d + 1)
                    break

            if d1 is not None:
                break

        return d1, idx1

    def _find_second_digit(self, line_incr: str) -> Optional[str]:
        d1 = None
        for idx, c in enumerate(line_incr):
            if c.isdigit():
                d1 = line_incr[idx]
            else:
                for d, digit in enumerate(self.DIGITS):
                    size = len(digit)
                    if line_incr[idx : idx + size] == digit:
                        d1 = str(d + 1)

        return d1

    def solve_part_two(self) -> Result:
        numbers: list[int] = []
        for line in self._puzzle_input.split("\n"):
            # look at characters in line
            d1, start_idx = self._find_first_digit(line)

            line_incr = line[start_idx + 1 :]
            d2 = self._find_second_digit(line_incr)

            if d2 is None:
                d2 = d1

            numbers.append(int(d1 + d2))

        return sum(numbers)
