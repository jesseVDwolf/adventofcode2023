from abc import ABC, abstractmethod
from importlib import resources
from pathlib import Path
from typing import Optional

type Result = int | str


class Day(ABC):
    def __init__(self, puzzle_input: Optional[str] = None) -> None:
        super().__init__()
        if puzzle_input is None:
            puzzle_input = self._get_puzzle_input(self.day)

        self._puzzle_input = puzzle_input

    @property
    @abstractmethod
    def day(self) -> int:
        pass

    @abstractmethod
    def solve_part_one(self) -> Result:
        """Method to be implemented by day class that solves part one of a day.

        Args:
            input (str): input string used for the puzzle

        Returns:
            Result: result object containing the puzzle solution
        """
        ...

    @abstractmethod
    def solve_part_two(self) -> Result:
        """Method to be implemented by day class that solves part two of a day.

        Args:
            input (str): input string used for the puzzle

        Returns:
            Result: result object containing the puzzle solution
        """
        ...

    @staticmethod
    def _get_puzzle_input(day: int) -> str:
        puzzle_input_file = resources.files(__package__).joinpath('static', 'inputs', f'aoc{day}.txt')
        return puzzle_input_file.read_text()
