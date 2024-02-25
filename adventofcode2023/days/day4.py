from textwrap import dedent
from adventofcode2023.day import Day, Result

import re
from typing import Self
from dataclasses import dataclass

@dataclass
class Card:
    number: int
    winning_numbers: list[int]
    your_numbers: list[int]

    @classmethod
    def from_line(cls, line: str) -> Self:
        cleaned_line = re.sub(r' +', ' ', line)
        card_conf, number_lines = cleaned_line.split(':')
        number = int(card_conf.split(' ')[1])

        winning_numbers_line, your_numbers_line = number_lines.split('|')
        winning_numbers = [ int(n) for n in winning_numbers_line.strip().split(' ') ]
        your_numbers = [ int(n) for n in your_numbers_line.strip().split(' ') ]

        return cls(number, winning_numbers, your_numbers)
    
    def get_matching_numbers(self) -> list[int]:
        return [ n for n in self.your_numbers if n in self.winning_numbers ]

class Day4(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 4

    def solve_part_one(self) -> Result:
        lines = self._puzzle_input.split('\n')
        sum_winning_numbers: list[int] = []
        for line in lines:

            import re

            line = re.sub(r' +', ' ', line)
            _, cards = line.split(':')

            winning_number_line, your_number_line = cards.split('|')
            
            winning_numbers = [ int(n) for n in winning_number_line.strip().split(' ') ]
            your_numbers = [ int(n) for n in your_number_line.strip().split(' ') ]

            your_winning_numbers = [ n for n in your_numbers if n in winning_numbers ]
            if your_winning_numbers:
                sum_winning_numbers.append( 1 * (2 ** (len(your_winning_numbers) - 1)) )

        return sum(sum_winning_numbers)
    

    def solve_part_two(self) -> Result:
        cards = [ Card.from_line(line) for line in self._puzzle_input.split('\n') ]
        instances = { c.number: 0 for c in cards }

        from collections import deque

        dq_cards_to_check: deque[Card] = deque(cards)
        while len(dq_cards_to_check) > 0:

            card = dq_cards_to_check.popleft()
            matching_numbers = card.get_matching_numbers()

            if len(matching_numbers) > 0:
                starting_number = card.number + 1
                ending_number = starting_number + len(matching_numbers)

                for card_num in range(starting_number, ending_number):
                    dq_cards_to_check.append( cards[card_num - 1] )

            instances[card.number] += 1

        return sum(instances.values())


if __name__ == '__main__':
    example_input = dedent("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""").strip()

    day = Day4(example_input)
    print(day.solve_part_one())
    print(day.solve_part_two())