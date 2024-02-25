import pytest

from adventofcode2023.days import Day3
from typing import Iterable
from copy import deepcopy

@pytest.fixture(scope='function')
def day3() -> Day3:
    return Day3('')

@pytest.mark.parametrize(
    argnames='range_,chars,output',
    argvalues=[
        (
            range(3),
            ['4', '6', '7', '.', '.', '1', '1', '4', '.', '.'],
            467
        ),
        (
            range(5, 10),
            ['4', '6', '7', '.', '.', '1', '1', '4', '5', '6'],
            11456
        )
    ]
)
def test_parse_number_from_grid(day3: Day3, range_: Iterable[int], chars: list[str], output: int):
    for i in range_:
        copy = deepcopy(chars)
        assert day3._parse_number_from_grid(copy, i) == output
