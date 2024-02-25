from textwrap import dedent
from adventofcode2023.day import Day, Result

from functools import cmp_to_key
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Type, Union

class HandType(Enum):
    FIVE_OF_A_KIND = auto()
    FOUR_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    THREE_OF_A_KIND = auto()
    TWO_PAIR = auto()
    ONE_PAIR = auto()
    HIGH_CARD = auto()

    def strength(self) -> int:
        return len(HandType) - self.value + 1
    

assert HandType.FIVE_OF_A_KIND.strength() == 7
assert HandType.HIGH_CARD.strength() == 1


@dataclass
class HandOfCards:
    type_: HandType = field(init=False)
    cards: str

    def __post_init__(self) -> None:
        assert len(self.cards) == 5

        sorted_cards = sorted(self.cards)
        from itertools import groupby

        groups = [ ''.join(g) for _, g in groupby(sorted_cards) ]
        sorted_groups = sorted(groups, key=lambda x: len(x))
        if len(sorted_groups) == 1:
            self.type_ = HandType.FIVE_OF_A_KIND
        elif len(sorted_groups) == 2 and len(sorted_groups[0]) == 1:
            self.type_ = HandType.FOUR_OF_A_KIND
        elif len(sorted_groups) == 2 and len(sorted_groups[0]) == 2:
            self.type_ = HandType.FULL_HOUSE
        elif len(sorted_groups) == 3 and len(sorted_groups[-1]) == 3:
            self.type_ = HandType.THREE_OF_A_KIND
        elif len(sorted_groups) == 3:
            self.type_ = HandType.TWO_PAIR
        elif len(sorted_groups) == 4:
            self.type_ = HandType.ONE_PAIR
        else:
            self.type_ = HandType.HIGH_CARD


@dataclass
class BonusHandOfCards:
    type_: HandType = field(init=False)
    cards: str

    @staticmethod
    def _get_most_common_card(cards: str) -> str:
        from collections import Counter

        counter = Counter(cards)
        most_common = counter.most_common()
        for tup in most_common:
            v, _ = tup
            if v == 'J':
                continue
            else:
                return v
        
        # could be only jokers in the hand
        # does not matter what we return here
        return '2'


    def __post_init__(self) -> None:
        assert len(self.cards) == 5

        from copy import deepcopy
        cards = deepcopy(self.cards)

        # if J(oker) is also a card. Update sorted_cards (NOT THE INSTANCE VARIABLE .cards)
        # to set J to the card that is most common already
        if 'J' in cards:
            joker_card = self._get_most_common_card(cards)
            cards = cards.replace('J', joker_card)
        
        sorted_cards = sorted(cards)
        from itertools import groupby

        groups = [ ''.join(g) for _, g in groupby(sorted_cards) ]
        sorted_groups = sorted(groups, key=lambda x: len(x))
        if len(sorted_groups) == 1:
            self.type_ = HandType.FIVE_OF_A_KIND
        elif len(sorted_groups) == 2 and len(sorted_groups[0]) == 1:
            self.type_ = HandType.FOUR_OF_A_KIND
        elif len(sorted_groups) == 2 and len(sorted_groups[0]) == 2:
            self.type_ = HandType.FULL_HOUSE
        elif len(sorted_groups) == 3 and len(sorted_groups[-1]) == 3:
            self.type_ = HandType.THREE_OF_A_KIND
        elif len(sorted_groups) == 3:
            self.type_ = HandType.TWO_PAIR
        elif len(sorted_groups) == 4:
            self.type_ = HandType.ONE_PAIR
        else:
            self.type_ = HandType.HIGH_CARD


assert HandOfCards('AAAAA').type_ == HandType.FIVE_OF_A_KIND
assert HandOfCards('AA8AA').type_ == HandType.FOUR_OF_A_KIND
assert HandOfCards('23332').type_ == HandType.FULL_HOUSE
assert HandOfCards('TTT98').type_ == HandType.THREE_OF_A_KIND
assert HandOfCards('23432').type_ == HandType.TWO_PAIR
assert HandOfCards('A23A4').type_ == HandType.ONE_PAIR
assert HandOfCards('23456').type_ == HandType.HIGH_CARD

HOC = Union[HandOfCards, BonusHandOfCards]

class Day7(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
        self._cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        self._strengths = { k: v for v, k in enumerate(reversed(self._cards)) }

    @property
    def day(self) -> int:
        return 7

    def sort_hands_on_strength(self, a: tuple[HOC, int], b: tuple[HOC, int]) -> int:
        left, _  = a
        right, _ = b
        # 1 if a > b, 0 if eq, -1 if smaller
        if left.type_.strength() > right.type_.strength():
            return 1
        elif left.type_.strength() < right.type_.strength():
            return -1
        else:
            # check the individual cards
            for x, y in zip(left.cards, right.cards):
                if x == y:
                    continue
                
                if self._strengths[x] > self._strengths[y]:
                    return 1
                else:
                    return -1

    
    def solve_part_one(self) -> Result:
        hands: list[tuple[HandOfCards, int]] = []
        lines = self._puzzle_input.split('\n')
        for line in lines:
            cards, bid = line.split()
            bid = int(bid)

            hands.append((HandOfCards(cards), bid))
        
        total_winnings = 0
        for idx, hand_with_bid in enumerate(sorted(hands, key=cmp_to_key(self.sort_hands_on_strength))):

            rank = idx + 1
            _, bid = hand_with_bid
            total_winnings += (rank * bid)

        return total_winnings


    def solve_part_two(self) -> Result:
        hands: list[tuple[BonusHandOfCards, int]] = []
        lines = self._puzzle_input.split('\n')
        for line in lines:
            cards, bid = line.split()
            bid = int(bid)

            hands.append((BonusHandOfCards(cards), bid))

        total_winnings = 0
        for idx, hand_with_bid in enumerate(sorted(hands, key=cmp_to_key(self.sort_hands_on_strength))):

            rank = idx + 1
            _, bid = hand_with_bid
            total_winnings += (rank * bid)

        return total_winnings


if __name__ == '__main__':
    example_input = dedent("""32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483""").strip()
    
    day = Day7(example_input)
    print(day.solve_part_one())
    print(day.solve_part_two())
