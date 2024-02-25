from itertools import product
from queue import Queue
from textwrap import dedent

import numpy as np
from adventofcode2023.day import Day, Result

from typing import NamedTuple
from enum import StrEnum

class Direction(StrEnum):
    RIGHT = 'R'
    LEFT = 'L'
    UP = 'U'
    DOWN = 'D'

class DigOperation(NamedTuple):
    dir: Direction
    meters: int
    color: str

class Point(NamedTuple):
    x: int
    y: int

class Day18(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
    
    @property
    def day(self) -> int:
        return 18

    @staticmethod
    def get_grid_points(operations: list[DigOperation]) -> list[Point]:
        p = Point(0, 0)
        points: list[Point] = [p]
        for op in operations:

            x, y = p
            match op.dir:

                case Direction.LEFT:
                    p = Point(x - op.meters, y)

                case Direction.RIGHT:
                    p = Point(x + op.meters, y)

                case Direction.UP:
                    p = Point(x, y - op.meters)

                case Direction.DOWN:
                    p = Point(x, y + op.meters)
            
            points.append(p)
        
        return points
    
    @staticmethod
    def get_grid(grid_shape: tuple[int, int], points: list[Point], operations: list[DigOperation]) -> np.ndarray:
        grid = np.full(shape=grid_shape, fill_value='.', dtype=np.dtype('U1'))

        for op, p in zip(operations, points[:-1]):
            x, y = p
            match op.dir:

                case Direction.LEFT:
                    grid[y, x - op.meters: x + 1] = '#'

                case Direction.RIGHT:
                    grid[y, x: x + op.meters] = '#'

                case Direction.UP:
                    grid[y - op.meters: y + 1, x] = '#'

                case Direction.DOWN:
                    grid[y: y + op.meters, x] = '#'
        
        return grid

    @staticmethod
    def inside_trench(grid: np.ndarray, p: Point) -> bool:
        """Check if a point is inside of a "trench". In below
        example the V is inside while the X is not.

        [['#' '#' '#' '#' '#' '#' '#']
         ['#' '.' '.' '.' '.' '.' '#']
         ['#' '#' '#' '.' '.' '.' '#']
         ['.' 'X' '#' '.' 'V' '.' '#']
         ['.' '.' '#' '.' '.' '.' '#']
         ['#' '#' '#' '.' '#' '#' '#']
         ['#' '.' '.' '.' '#' '.' '.']
         ['#' '#' '.' '.' '#' '#' '#']
         ['.' '#' '.' '.' '.' '.' '#']
         ['.' '#' '#' '#' '#' '#' '#']]

        Args:
            grid (np.ndarray): 2D array describing the grid with trenches
            p (Point): point in the grid

        Returns:
            bool: true if inside, false if not
        """
        return (
            np.count_nonzero(grid[:p.y + 1, p.x] == '#') % 2 == 1 and   # top
            np.count_nonzero(grid[p.y:, p.x] == '#') % 2 == 1 and       # bottom
            np.count_nonzero(grid[p.y, :p.x + 1] == '#') % 2 == 1 and   # left
            np.count_nonzero(grid[p.y, p.x:] == '#') % 2 == 1
        )
    
    def get_point_inside(self, grid: np.ndarray, p: Point) -> Point:
        dirs = product([1, 0, -1], repeat=2)
        for d in dirs:
            x, y = d
            starting_point = Point(p.x + x, p.y + y)
            if self.inside_trench(grid, starting_point):
                return starting_point
        
        raise ValueError(f"Point {p} not next to point inside trench.")


    def fill_grid(self, grid: np.ndarray, starting_point: Point) -> np.ndarray:
        q: Queue[Point] = Queue()
        height, width = grid.shape

        visited = set()
        q.put(starting_point)
        while not q.empty():

            p = q.get()
            if p in visited:
                continue

            if p.x > 0 and grid[p.y, p.x - 1] == '.':
                q.put(Point(p.x - 1, p.y))
            
            if p.x < (width - 1) and grid[p.y, p.x + 1] == '.':
                q.put(Point(p.x + 1, p.y))

            if p.y > 0 and grid[p.y - 1, p.x] == '.':
                q.put(Point(p.x, p.y - 1))

            if p.y < (height - 1) and grid[p.y + 1, p.x] == '.':
                q.put(Point(p.x, p.y + 1))
            
            grid[p.y, p.x] = '#'
            visited.add(p)
        
        return grid


    
    def solve_part_one(self) -> Result:
        # 1. parse instructions into list of DigOperation
        # 2. find width and height
        # 2.1. create a list of points
        # 2.2. Loop over points and find smallest, largest x,y
        # 3. find point within trench
        # 4. Use floodfill to find how much lava can be inside
        operations = [
            DigOperation(Direction(dir_), int(meters), color[1:-1])
            for dir_, meters, color in [ 
                operation.split(' ')
                for operation in self._puzzle_input.split('\n')
            ]
        ]
        points = self.get_grid_points(operations)
        assert len(operations) + 1 == len(points)
        
        min_x, min_y = np.min(points, axis=0)
        max_x, max_y = np.max(points, axis=0)
    
        # map points to grid
        adjusted_points = [
            Point(p.x - min_x, p.y - min_y)
            for p in points
        ]
        grid_shape = (max_y - min_y + 1), (max_x - min_x + 1)
        grid = self.get_grid(grid_shape, adjusted_points, operations)

        # find point trench (walk the #)
        starting_point = self.get_point_inside(grid, adjusted_points[0])
        
        # fill with floodfill
        grid = self.fill_grid(grid, starting_point)
        return np.count_nonzero(grid == '#')
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()


if __name__ == '__main__':
    example_input = dedent("""
    R 6 (#70c710)
    D 5 (#0dc571)
    L 2 (#5713f0)
    D 2 (#d2c081)
    R 2 (#59c680)
    D 2 (#411b91)
    L 5 (#8ceee2)
    U 2 (#caa173)
    L 1 (#1b58a2)
    U 2 (#caa171)
    R 2 (#7807d2)
    U 3 (#a77fa3)
    L 2 (#015232)
    U 2 (#7a21e3)""").strip()
    day = Day18()
    print(day.solve_part_one())
