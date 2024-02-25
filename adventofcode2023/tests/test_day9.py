from typing import Generator
import pytest

from adventofcode2023.days import Day9
from adventofcode2023.tests.utils import get_example_inputs


@pytest.fixture(scope='function')
def example() -> Generator[tuple[str, str], None, None]:
    for example_input, example_expected_output in get_example_inputs(day=9):
        yield example_input, example_expected_output


@pytest.mark.unit
@pytest.mark.parametrize(
    argnames='input,expected_output',
    argvalues=[
        ([0, 3, 6, 9, 12, 15], 18),
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
    ]
)
def test_get_extrapolated_value(input: list[int], expected_output: int):
    assert Day9.get_last_value(input) == expected_output


@pytest.mark.example
def test_example_input(example: tuple[str, str]):
    puzzle_input, expected_output = example
    assert str(Day9(puzzle_input).solve_part_one()) == expected_output
