import os
from queue import Queue
import sys
from textwrap import dedent
from time import sleep
from typing import NamedTuple, Optional, Self

import numpy as np
from adventofcode2023.day import Day, Result

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)


class Beam(NamedTuple):
    p: Point        # location
    d: Point        # direction

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)


class Day16(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 16
    
    @staticmethod
    def _outside_of_grid(grid: np.ndarray, p: Point) -> bool:
        x, y = p
        rows, cols = grid.shape

        return x < 0 or y < 0 or y >= rows or x >= cols
    
    def get_energized_tiles(self, grid: np.ndarray, starting_beam: Beam) -> int:
        directions = {
            '\\': {
                RIGHT: DOWN,
                LEFT: UP,
                DOWN: RIGHT,
                UP: LEFT
            },
            '/': {
                RIGHT: UP,
                LEFT: DOWN,
                DOWN: LEFT,
                UP: RIGHT
            }
        }
        # a beam encodes a location and a direction. A beam may
        # not visit the same location with the same direction.
        beams_visited: set[Beam] = set()

        # keep track of the tiles that one or more beams have
        # traveled over.
        tiles_energized: set[Point] = set()

        queue: Queue[Beam] = Queue()
        queue.put(starting_beam)
        while not queue.empty():

            beam = queue.get()


            # check if beam has moved out of bounds
            if self._outside_of_grid(grid, beam.p):
                continue

            # check if beam is in already visited place
            if beam in beams_visited:
                continue

            c = grid[beam.p.y][beam.p.x]
            match c:

                case '.':
                    queue.put(Beam(beam.p + beam.d, beam.d))
                
                case '|':
                    if beam.d in [UP, DOWN]:
                        queue.put(Beam(beam.p + beam.d, beam.d))
                    else:
                        queue.put(Beam(beam.p + UP, UP))
                        queue.put(Beam(beam.p + DOWN, DOWN))

                case '-':
                    if beam.d in [LEFT, RIGHT]:
                        queue.put(Beam(beam.p + beam.d, beam.d))
                    else:
                        queue.put(Beam(beam.p + LEFT, LEFT))
                        queue.put(Beam(beam.p + RIGHT, RIGHT))

                case '\\' | '/':
                    direction = directions[c][beam.d]
                    queue.put(Beam(beam.p + direction, direction))
            
            tiles_energized.add(beam.p)
            beams_visited.add(beam)

        return len(tiles_energized)
    
    def solve_part_one(self) -> Result:
        grid = np.array(
            object=[ list(x) for x in self._puzzle_input.split('\n') ],
            dtype=np.dtype("U1")
        )
        # starting beam starts at location (0, 0) and moves to the right
        starting_beam = Beam(Point(0, 0), Point(1, 0))
        return self.get_energized_tiles(grid, starting_beam)
    
    def solve_part_two(self) -> Result:
        grid = np.array(
            object=[ list(x) for x in self._puzzle_input.split('\n') ],
            dtype=np.dtype("U1")
        )
        rows, columns = grid.shape
        beams_to_test = (
            # left side -> (0, y) ...
            [Beam(Point(0, y), RIGHT) for y in range(columns)] +
            # top side -> (x, 0) ...
            [Beam(Point(x, 0), DOWN) for x in range(rows)] +
            # right side -> (`columns`, y)
            [Beam(Point(columns -1, y), LEFT) for y in range(columns)] +
            # bottom side -> (`rows`, x)
            [Beam(Point(rows, x), UP) for x in range(rows)]
        )
        return max( self.get_energized_tiles(grid, beam) for beam in beams_to_test )


if __name__ == "__main__":
    example_input = dedent(r"""
    .|...\....
    |.-.\.....
    .....|-...
    ........|.
    ..........
    .........\
    ..../.\\..
    .-.-/..|..
    .|....-|.\
    ..//.|....""").strip()
    day = Day16()
    print(day.solve_part_one())
    print(day.solve_part_two())