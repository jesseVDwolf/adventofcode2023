import pytest
from adventofcode2023.days.day4 import Card

@pytest.mark.parametrize(
    argnames='input_,expected_output',
    argvalues=[
        (
            'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
            Card(3, [1, 21, 53, 59, 44], [69, 82, 63, 72, 16, 21, 14, 1])
        )
    ]
)
def test_card(input_: str, expected_output: Card):
    assert Card.from_line(input_) == expected_output
