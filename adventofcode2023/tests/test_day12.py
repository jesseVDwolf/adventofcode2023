from pathlib import Path
import pytest

from adventofcode2023.days import Day12
from collections import Counter
from math import pow

@pytest.fixture
def day12(request: pytest.FixtureRequest) -> Day12:
    puzzle_input = request.param
    return Day12(puzzle_input)

@pytest.mark.parametrize(
    argnames='day12,input,expected_output',
    argvalues=[
        (
            '',
            '???.###',
            [
                '###.###',
                '##..###',
                '#.#.###',
                '#...###',
                '.##.###',
                '.#..###',
                '..#.###',
                '....###'
            ]
        ),
        (
            '',
            '?###????????',
            None
        )
    ],
    indirect=['day12']
)
def test_get_possible_rows(day12: Day12, input: str, expected_output: list[str]):
    unknown_count = Counter(input)['?']
    output = day12._get_possible_rows(input)

    assert len(output) == pow(2, unknown_count)
    if expected_output is not None:
        assert expected_output == output


@pytest.mark.parametrize(
    argnames='day12,possible_rows,group_sizes,output',
    argvalues=[
        (
            '',
            [
                '###.###',
                '##..###',
                '#.#.###',
                '#...###',
                '.##.###',
                '.#..###',
                '..#.###',
                '....###'
            ],
            [1, 1, 3],
            ['#.#.###']
        ),
        (
            '',
            ['##.#.######..#####.'],
            [1, 6, 5],
            []
        ),
        (
            '',
            ['.###.##.#.##'],
            [1, 1, 3],
            []
        ),
        (
            '',
            ['.###.##.#.##'],
            [3, 2, 1],
            []
        )
    ],
    indirect=['day12']
)
def test_get_rows_passed(day12: Day12, possible_rows: list[str], group_sizes: list[int], output: list[str]):
    assert day12._get_rows_passed(possible_rows, group_sizes) == output



@pytest.mark.parametrize(
    argnames='day12,expected_output_1, expected_output_2',
    argvalues=[
        (
            (
                "???.### 1,1,3\n"
                ".??..??...?##. 1,1,3\n"
                "?#?#?#?#?#?#?#? 1,3,1,6\n"
                "????.#...#... 4,1,1\n"
                "????.######..#####. 1,6,5\n"
                "?###???????? 3,2,1",
                21,
                0
            )
        )
    ],
    indirect=['day12']
)
def test_example_inputs(day12: Day12, expected_output_1: int, expected_output_2: int):
    assert day12.solve_part_one() == expected_output_1
