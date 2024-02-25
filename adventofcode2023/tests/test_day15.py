import pytest
from adventofcode2023.days.day15 import hash_

@pytest.mark.parametrize(
    argnames='input,expected_output',
    argvalues=[
        ('rn=1', 30),
        ('cm-', 253)
    ]
)
def test_hash_(input: str, expected_output: int):
    assert hash_(input) == expected_output
