import pytest
import numpy as np
from adventofcode2023.days import Day11

@pytest.fixture
def day() -> Day11:
    return Day11('')

@pytest.mark.parametrize(
    argnames='input,expected_output',
    argvalues=[
        (
            np.array((
                ('.', '#', '.', '.'),
                ('.', '.', '#', '.'),
                ('.', '.', '.', '.')
            ), dtype=np.dtype('U1')),
            np.array((
                ('.', '.', '#', '.', '.', '.'),
                ('.', '.', '.', '#', '.', '.'),
                ('.', '.', '.', '.', '.', '.'),
                ('.', '.', '.', '.', '.', '.')
            ), dtype=np.dtype('U1'))
        )
    ]
)
def test_get_expanded_universe(day: Day11, input: np.ndarray, expected_output: np.ndarray):
    assert np.array_equal(day.get_expanded_universe(input, 0, 0), expected_output)

