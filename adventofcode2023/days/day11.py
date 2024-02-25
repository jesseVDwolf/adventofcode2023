from pprint import pprint
import numpy as np
from typing import NamedTuple, Optional
from itertools import combinations
from adventofcode2023.day import Day, Result

class Point(NamedTuple):
    x: int
    y: int


def manhattan(a: Point, b: Point) -> int:
    """Manhattan distance between two points

    Args:
        a (Point): point a
        b (Point): point b

    Returns:
        int: distance
    """
    return abs(b.x - a.x) + abs(b.y - a.y)


class Day11(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
    

    @property
    def day(self) -> int:
        return 11
    
    @staticmethod
    def expand_column(universe: np.ndarray, idx: int) -> np.ndarray:
        column = np.array(('.', ) * universe.shape[0], dtype=np.dtype('U1'))
        return np.insert(universe, idx, column, axis=1)
    
    @staticmethod
    def expand_row(universe: np.ndarray, idx: int) -> np.ndarray:
        row = np.array(('.', ) * universe.shape[1], dtype=np.dtype('U1'))
        return np.insert(universe, idx, row, axis=0)
    
    def get_expanded_universe(self, universe: np.ndarray, idx: int, row_or_column: int) -> np.ndarray:
        if row_or_column == 1 and idx == universe.shape[1]:
            return universe
        
        if row_or_column == 0 and idx == universe.shape[0]:
            return self.get_expanded_universe(universe, 0, 1)

        if row_or_column == 0:
            if all(c == '.' for c in universe[idx]):
                new_universe = self.expand_row(universe, idx + 1)
                return self.get_expanded_universe(new_universe, idx + 2, 0)
            else:
                return self.get_expanded_universe(universe, idx + 1, 0)
        else:
            if all(c == '.' for c in universe.T[idx]):
                new_universe = self.expand_column(universe, idx + 1)
                return self.get_expanded_universe(new_universe, idx + 2, 1)
            else:
                return self.get_expanded_universe(universe, idx + 1, 1)
    

    @staticmethod
    def get_point_combinations(universe: np.ndarray) -> list[tuple[Point, Point]]:
        points: list[Point] = []
        iterator = np.nditer(universe, flags=['multi_index'])
        for c in iterator:
            if c == '#':
                x, y = iterator.multi_index
                points.append(Point(x, y))
        
        return list(combinations(points, 2))


    
    def solve_part_one(self) -> Result:
        # 1. expand the universe
        # 2. generate pairs
        # 3. sum up the lengths of distances between all pairs
        base = np.array([ list(s) for s in self._puzzle_input.split('\n') ], dtype=np.dtype('U1'))
        universe = self.get_expanded_universe(base, 0, 0)
        combinations = self.get_point_combinations(universe)

        return sum( manhattan(*pair) for pair in combinations )
    
    @staticmethod
    def get_galaxy_locations(universe: np.ndarray) -> list[Point]:
        galaxies: list[Point] = []
        iter = np.nditer(universe, flags=['multi_index'])
        for c in iter:
            if c == '#':
                y, x = iter.multi_index
                galaxies.append(Point(x, y))
        
        return galaxies
    
    def get_expanded_points(self, points: list[Point], incr: int, idx: int, row_indexes: list[int], column_indexes: list[int], row_or_column: int) -> list[Point]:
        if row_or_column == 1 and idx == len(column_indexes):
            return points
        
        if row_or_column == 0 and idx == len(row_indexes):
            return self.get_expanded_points(points, incr, 0, row_indexes, column_indexes, 1)
        
        if row_or_column == 0:
            for i, p in enumerate(points):
                if p.y > row_indexes[idx]:
                    # update the points
                    points[i] = Point(p.x, p.y + int(incr))

            # update the row_indexes
            row_indexes = [ i if i < row_indexes[idx] else i + incr for i in row_indexes ]
            return self.get_expanded_points(points, incr, idx + 1, row_indexes, column_indexes, 0)
        else:
            for i, p in enumerate(points):
                if p.x > column_indexes[idx]:
                    points[i] = Point(p.x + int(incr), p.y)
            
            column_indexes = [i if i < column_indexes[idx] else i + incr for i in column_indexes]
            return self.get_expanded_points(points, incr, idx + 1, row_indexes, column_indexes, 1)

    
    def solve_part_two(self) -> Result:
        # 1. load the string into a 2D numpy array of chars
        # 2. find all the galaxies and store their locations
        # 3. update the galaxies their locations based on the expansions
        # 3.1 Check if the galaxy is right of the expansion. This means the galaxy is moved
        #     This means that if a column is expanded. The galaxy is moved 1e6 to the right
        #     This means that if a row is expanded. The galaxy is moved 1e6 down
        universe = np.array([ list(s) for s in self._puzzle_input.split('\n') ], dtype=np.dtype('U1'))

        points = self.get_galaxy_locations(universe)
        row_indexes = [ idx for idx, row in enumerate(universe) if all( c == '.' for c in row ) ]
        column_indexes = [idx for idx, column in enumerate(universe.T) if all( c == '.' for c in column ) ]
        points = self.get_expanded_points(points, int(1e6) - 1, 0, row_indexes, column_indexes, 0)

        return sum( manhattan(*pair) for pair in combinations(points, 2) )
    

if __name__ == '__main__':
    example_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    day = Day11()
    print(day.solve_part_two())
    
