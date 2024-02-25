import pytest
from adventofcode2023.days import Day8
from adventofcode2023.days.day8 import Network

@pytest.fixture
def day(request: pytest.FixtureRequest) -> Day8:
    puzzle_input = request.param
    return Day8(puzzle_input)


@pytest.mark.parametrize(
    argnames='day,expected_output',
    argvalues=[
        (
            """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""",
            (
                "RL",
                {
                    "AAA": ("BBB", "CCC"),
                    "BBB": ("DDD", "EEE"),
                    "CCC": ("ZZZ", "GGG"),
                    "DDD": ("DDD", "DDD"),
                    "EEE": ("EEE", "EEE"),
                    "GGG": ("GGG", "GGG"),
                    "ZZZ": ("ZZZ", "ZZZ"),
                },
            )
        )
    ]
)
def test_parse_input(day: Day8, expected_output: tuple[str, Network]):
    assert day.parse_input() == expected_output


@pytest.mark.parametrize(
    argnames='day,expected_output',
    argvalues=[
        (
            """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""",
            2
        ),
        (
            """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""",
            6
        )
    ]
)
def test_get_steps_to_end(day: Day8, expected_output: int):
    assert day.get_steps_to_end(*day.parse_input()) == expected_output
