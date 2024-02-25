import pytest

from adventofcode2023.days import Day10
from textwrap import dedent

@pytest.mark.parametrize(
    argnames='input,expected_output',
    argvalues=[
        pytest.param(
            """
            .....
            .S-7.
            .|.|.
            .L-J.
            .....
            """,
            (1, 1),
            id=str((1, 1))
        ),
        pytest.param(
            """
            .....
            .F-7.
            .|.|.
            .L-S.
            .....
            """,
            (3, 3),
            id=str((3, 3))
        )
    ]
)
def test_find_start_coordinates(input: str, expected_output: tuple[int, int]):
    assert Day10.find_start_coordinates(dedent(input).strip()) == expected_output
