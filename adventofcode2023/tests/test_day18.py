import pytest
import numpy as np
from adventofcode2023.days import Day18
from adventofcode2023.days.day18 import Direction, Point, DigOperation

@pytest.fixture
def day() -> Day18:
    return Day18('')


@pytest.mark.parametrize(
    argnames='input_,expected_output',
    argvalues=[
        (
            [
                DigOperation(Direction.LEFT, 4, ''),
                DigOperation(Direction.DOWN, 5, ''),
                DigOperation(Direction.RIGHT, 2, ''),
                DigOperation(Direction.UP, 8, ''),
            ],
            [
                Point(0, 0),
                Point(-4, 0),
                Point(-4, 5),
                Point(-2, 5),
                Point(-2, -3)
            ]
        )
    ]
)
def test_get_grid_points(day: Day18, input_: list[DigOperation], expected_output: list[Point]):
    assert day.get_grid_points(input_) == expected_output


@pytest.mark.parametrize(
    argnames='input_,expected_output',
    argvalues=[
        (
            (
                [
                    DigOperation(Direction.LEFT, 4, ''),
                    DigOperation(Direction.DOWN, 5, ''),
                    DigOperation(Direction.RIGHT, 2, ''),
                    DigOperation(Direction.UP, 8, ''),
                ],
                (
                    (9, 5) 
                ),
                [
                    Point(0 - (-4), 0 - (-3)),
                    Point(-4 - (-4), 0 - (-3)),
                    Point(-4 - (-4), 5 - (-3)),
                    Point(-2 - (-4), 5 - (-3)),
                    Point(-2 - (-4), -3 - (-3))
                ]
            ),
            # min_x = -4, min_y = -3, max_x = 0, max_y = 5
            np.array([
                ['.', '.', '#', '.', '.'],
                ['.', '.', '#', '.', '.'],
                ['.', '.', '#', '.', '.'],
                ['#', '#', '#', '#', '#'],
                ['#', '.', '#', '.', '.'],
                ['#', '.', '#', '.', '.'],
                ['#', '.', '#', '.', '.'],
                ['#', '.', '#', '.', '.'],
                ['#', '#', '#', '.', '.']
            ])
        )
    ]
)
def test_get_grid(day: Day18, input_: tuple[list[DigOperation], tuple[int, int], list[Point]], expected_output: np.ndarray):
    operations, grid_shape, points = input_
    output = day.get_grid(grid_shape, points, operations)
    assert np.array_equal(output, expected_output)



@pytest.fixture
def grid() -> np.ndarray:
    return np.array([
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '.', '.', '.', '.', '.', '#'],
        ['#', '#', '#', '.', '.', '.', '#'],
        ['.', '.', '#', '.', '.', '.', '#'],
        ['.', '.', '#', '.', '.', '.', '#'],
        ['#', '#', '#', '.', '#', '#', '#'],
        ['#', '.', '.', '.', '#', '.', '.'],
        ['#', '#', '.', '.', '#', '#', '#'],
        ['.', '#', '.', '.', '.', '.', '#'],
        ['.', '#', '#', '#', '#', '#', '#']
    ], dtype=np.dtype('U1'))

@pytest.mark.parametrize(
    argnames='input_,expected_output',
    argvalues=[
        (
            Point(0, 0),
            False
        ),
        (
            Point(0, 3),
            False
        ),
        (
            Point(1, 1),
            True
        ),
        (
            Point(3, 2),
            True
        ),
        (
            Point(2, 6),
            True
        )
    ]
)
def test_inside_trench(day: Day18, grid: np.ndarray, input_: Point, expected_output: bool):
    assert day.inside_trench(grid, input_) == expected_output



@pytest.mark.parametrize(
    argnames='input_,expected_output',
    argvalues=[
        (
            (
                np.array([
                    ['#', '#', '#', '#', '#', '#', '#'],
                    ['#', '.', '.', '.', '.', '.', '#'],
                    ['#', '#', '#', '.', '.', '.', '#'],
                    ['.', '.', '#', '.', '.', '.', '#'],
                    ['.', '.', '#', '.', '.', '.', '#'],
                    ['#', '#', '#', '.', '#', '#', '#'],
                    ['#', '.', '.', '.', '#', '.', '.'],
                    ['#', '#', '.', '.', '#', '#', '#'],
                    ['.', '#', '.', '.', '.', '.', '#'],
                    ['.', '#', '#', '#', '#', '#', '#']
                ], dtype=np.dtype('U1')),
                Point(1, 1)
            ),
            np.array([
                ['#', '#', '#', '#', '#', '#', '#'],
                ['#', '#', '#', '#', '#', '#', '#'],
                ['#', '#', '#', '#', '#', '#', '#'],
                ['.', '.', '#', '#', '#', '#', '#'],
                ['.', '.', '#', '#', '#', '#', '#'],
                ['#', '#', '#', '#', '#', '#', '#'],
                ['#', '#', '#', '#', '#', '.', '.'],
                ['#', '#', '#', '#', '#', '#', '#'],
                ['.', '#', '#', '#', '#', '#', '#'],
                ['.', '#', '#', '#', '#', '#', '#']
            ], dtype=np.dtype('U1')),
        )
    ]
)
def test_fill_grid(day: Day18, input_: tuple[np.ndarray, Point], expected_output: np.ndarray):
    grid, starting_point = input_
    assert np.array_equal(day.fill_grid(grid, starting_point), expected_output)
