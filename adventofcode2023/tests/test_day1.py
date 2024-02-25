import pytest

from adventofcode2023.days import Day1

# test the example

@pytest.fixture(scope='session')
def day1() -> Day1:
    return Day1('')

# test individual cases
@pytest.mark.parametrize(
    argnames='input,output',
    argvalues=[
        ('two1nine', ('2', 0)),
        ('4nineeightseven2', ('4', 0))
    ]
)
def test_find_first_digit(day1: Day1, input: str, output: tuple[str, int]):
    v = day1._find_first_digit(input)
    assert v == output, f"Invalid value {v}"


@pytest.mark.parametrize(
    argnames='input,output',
    argvalues=[
        ('two1nine', '9'),
        ('4nineeightseven2', '2') 
    ]
)
def test_find_second_digit(day1: Day1, input: str, output: str):
    v = day1._find_second_digit(input)
    assert v == output, f"Invalid value {v}"
