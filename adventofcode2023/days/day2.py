from typing import Optional
from adventofcode2023.day import Day, Result
from math import prod

class Day2(Day):

    def __init__(self, puzzle_input: Optional[str] = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 2
    
    def solve_part_one(self) -> Result:
        max_colors = {'red': 12, 'green': 13, 'blue': 14}

        lines = self._puzzle_input.split("\n")
        ids: list[int] = []
        for line in lines:

            game_conf, cubes = line.split(':')

            *_, game_id = game_conf.split(' ')
            game_id = int(game_id)
            game_is_possible = True

            for cube in cubes.split(';'):
                
                start_colors = { 'red': 0, 'green': 0, 'blue': 0 }
                for roll in cube.split(','):

                    num, color = roll.strip().split(' ')
                    num = int(num)

                    start_colors[color] += num
                
                if any( start_colors[k] > max_colors[k] for k in max_colors ):
                    game_is_possible = False
                    break
            
            if game_is_possible:
                ids.append(game_id)

        return sum(ids)

    
    def solve_part_two(self) -> Result:
        powers: list[int] = []
        for line in self._puzzle_input.split('\n'):

            _, grabs = line.split(':')

            fewest_colors = { 'red': 0, 'green': 0, 'blue': 0 }
            for grab in grabs.split(';'):

                for cube in grab.split(','):

                    num, color = cube.strip().split(' ')
                    num = int(num)

                    if num > fewest_colors[color]:
                        fewest_colors[color] = num

            powers.append(prod(fewest_colors.values()))

        return sum(powers)