from dataclasses import dataclass
from pprint import pprint
from typing import NamedTuple, Optional
from adventofcode2023.day import Day, Result
from enum import Enum, auto
import numpy as np

class Direction(Enum):
    UP = auto()
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()

# a rock moves in the grid either
# left, right, up or down.
directions = {
    Direction.UP: (0, 1),
    Direction.DOWN: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.LEFT: (-1, 0)
}


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class RockGroup:
    # A cubed shaped rock has a fixed location
    # I can count the amount of stones that will
    # be rolling towards it and afterwards calculate
    # the total load of that group of stones based
    # on its location
    location: Point
    rolling_stones: int

    def score(self, max_y: int) -> int:
        # the score is calculated based on its location.
        # Specifically its y location. y = 0 means 10
        # points, y = 1 means 9 etc.
        # 
        # A rockgroup that represents the following
        # '#.0.0' at location (5, 6) where y = 6
        # where the height of the platform is 10
        # gives you a score of sum(range())
        # for each additional stone found.
        max_score = max_y - self.location.y
        return sum(range(max_score - self.rolling_stones + 1, max_score + 1))


class Day14(Day):
    """
    For day 14 you get a matrix of chars with 3 types of characters:
    - # : Represents a cubed stone that does not move
    - O : Represents a stone that is a smooth ball and can roll
    - . : Represents an empty space

    APPROACH 1
    Create the metal platform (the matrix) and load it into memory. Loop over
    the matrix and move every rock that you find. You have to create a new matrix
    here so as to prevent reprocessing rocks.
    
    APPROACH 2
    For each column, use the position of the rolling rocks relative to the blocked
    rocks. Create a group for each blocked rock (including the edge), with all the
    rolling rocks that won't pass it. You can then calculate the load of each rock
    using the position of the blocked rock - n.

    Example:
    - '.O.#.O.O..#O.O...' -> Rolls up (north)
        - groups: [ '#.O.', '#.O.O..', '#O.O...' ]
        - size per group:
            - '#.O.' -> '#O..' -> 17
            - '#.O.O..' -> '#OO....' -> 13 + 12
            - '#O.O...' -> '#OO....' -> 7 + 6
    """

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
    
    @property
    def day(self) -> int:
        return 14
    
    @staticmethod
    def get_rock_groups(platform: np.ndarray) -> list[RockGroup]:
        rockgroups: list[RockGroup] = []
        iter = np.nditer(platform, flags=['multi_index'])
        for c in iter:
            if c == '#':
                y, x = iter.multi_index
                column = platform.T[x]
                stone_group = column[y + 1:]
                next_cubed_stone = np.where(stone_group == '#')[0]
                if next_cubed_stone.size == 0:
                    rolling_stones = np.count_nonzero(stone_group == 'O')
                else:
                    rolling_stones = np.count_nonzero(stone_group[:next_cubed_stone[0]] == 'O')

                rockgroups.append(RockGroup(Point(x, y), rolling_stones))

        return rockgroups
    
    def solve_part_one(self) -> Result:
        # 1. load the platform into a 2D array
        # 2. calculate new location of rounded rocks if platform is tilted north
        # 2.1. Create groups of cube-shaped rocks and the stones below them (since stones roll north)
        # 3. calculate the load of the stones
        platform = np.array([ list(s) for s in self._puzzle_input.split('\n') ], dtype=np.dtype('U1'))

        # add a layer of cubed shaped stones at the top so they always stop somewhere
        platform = np.insert(platform, 0, np.array(('#',) * platform.shape[1]), axis=0)
        rockgroups = self.get_rock_groups(platform)
        pprint(rockgroups)
        print(sum( group.score(platform.shape[1]) for group in rockgroups ))
        return super().solve_part_one()
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()


if __name__ == '__main__':
    example_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    day = Day14()
    print(day.solve_part_one())
