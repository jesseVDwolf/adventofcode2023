import re

import numpy as np
from math import prod
from adventofcode2023.day import Day, Result


# There are three variables in this day
# Time
# Distance
# Speed
#
# Speed of a boat increases with how long you hold
# the button of the boat
# 0 ms -> 0 milimeter / milisecond
# 1 ms -> 1 milimeter / milisecond
# 2 ms -> 2 milimeter / milisecond
#
# You have a time allocated for a race. For example
# 10 miliseconds. You have to find all different
# options for how long you can hold the button that
# help you break the record.
# i.e. if a race takes 7 ms and the record is mm,
# you can hold the button for 2 ms, which means you
# have 5 ms left. You will go 2 mm/ms for 7 - 2 = 5 ms
# which means you'll travel a total of 10 mm
#


class Day6(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 6
    
    def solve_part_one(self) -> Result:
        input_stripped = re.sub(r' +', ' ', self._puzzle_input)
        matrix = [
            [
                int(n)
                for n in row.split(':')[1].split()
            ]
            for row in input_stripped.split('\n')
        ]
        T = np.transpose(matrix)

        num_ways_to_beat_record = []
        for race in T:
            lasts, distance = race
            
            num_ways = 0
            for hold_button_ms in range(1, lasts + 1):
                ms_left = lasts - hold_button_ms
                mm_traveled = hold_button_ms * ms_left
                if mm_traveled > distance:
                    num_ways += 1
            
            num_ways_to_beat_record.append(num_ways)

        return prod(num_ways_to_beat_record)
    

    def solve_part_two(self) -> Result:
        input_stripped = re.sub(r' +', ' ', self._puzzle_input)
        matrix = [
            [int(''.join(row.split(':')[1].split()))]
            for row in input_stripped.split('\n')
        ]
        T = np.transpose(matrix)

        num_ways_to_beat_record = []
        for race in T:
            lasts, distance = race
            
            num_ways = 0
            for hold_button_ms in range(1, lasts + 1):
                ms_left = lasts - hold_button_ms
                mm_traveled = hold_button_ms * ms_left
                if mm_traveled > distance:
                    num_ways += 1
            
            num_ways_to_beat_record.append(num_ways)

        return prod(num_ways_to_beat_record)