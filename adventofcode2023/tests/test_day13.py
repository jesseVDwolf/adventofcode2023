from textwrap import dedent
import numpy as np
import pytest
from adventofcode2023.days import Day13

@pytest.fixture
def day(request: pytest.FixtureRequest) -> Day13:
    return Day13('')

@pytest.fixture
def input_(request: pytest.FixtureRequest) -> str:
    return dedent(request.param).strip()

@pytest.mark.parametrize(
    argnames='input_,expected_output',
    argvalues=[
        (
            """
            #.##..##.
            ..#.##.#.
            ##......#
            ##......#
            ..#.##.#.
            ..##..##.
            #.#.##.#.""",
            (5, None),
        ),
        (
            """
            #...##..#
            #....#..#
            ..##..###
            #####.##.
            #####.##.
            ..##..###
            #....#..#""",
            (None, 4),
        ),
        (
            """
            #...##.
            ####..#
            ....##.
            ..#.##.
            #.##..#
            .##....
            ...#..#
            ..###.#
            #..####
            #...##.
            #...##.""",
            (None, 10),
        ),
        (
            """
            .####.##......#
            ...##.##..##..#
            ...##.##..##..#
            .####.##......#
            #.##.#..#.##.#.
            ..#####.##.###.
            .#...#...#..#..
            #######.######.
            .#.#...########""",
            (None, 2)
        ),
        (
            """
            #...#..#.
            #...#..#.
            .####..#.
            ..#..#..#
            ...#....#
            ##..###..
            #...####.
            #...####.
            ##..##...
            ...#....#
            ..#..#..#
            .####..#.
            #...#..#.""",
            (None, 1),
        ),
        (
            """
            #...##.#...#.##
            ##...#.###..###
            #....##..#.###.
            .###..#.##.....
            ##.#..##.#.#.#.
            ####.#...#.#...
            .#.....#..#...#
            .#.....#..#...#
            ####.#...#.#...
            ##.#..##.#.#.#.
            .###..#.##....#
            #....##..#.###.
            ##...#.###..###
            #...##.#...#.##
            ##..#...#.#.#.#
            #...#.##.##....
            #...#.##.##....""",
            (None, 16),
        ),
        (
            """
            .##..#.##.#..
            #.###.#..#.##
            ......####...
            #......##....
            .#.#.#....#..
            ..#.#.####.#.
            ####..####..#
            #.#..#....#..
            ..#...####...
            ..#...####...
            #.#..#....#..
            ####..####..#
            ..#.#.####.#.""",
            (None, 9),
        )
    ],
    indirect=['input_'],
    ids=list(range(7))
)
def test_get_reflection_point(day: Day13, input_: str, expected_output: tuple[int, int]):
    vert, hori = expected_output
    p = np.array(object=[ list(s) for s in input_.split('\n') ], dtype=np.dtype('U1'))
    assert day.get_reflection_point_hori(p) == hori
    assert day.get_reflection_point_vert(p) == vert
