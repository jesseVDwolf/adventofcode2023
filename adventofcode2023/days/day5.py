from itertools import chain
from adventofcode2023.day import Day, Result

from typing import Self, Generator
from dataclasses import dataclass

@dataclass
class Range:
    min: int
    max: int

    def contains(self, v: int) -> bool:
        return self.min <= v <= self.max


@dataclass
class Mapping:
    dst_range: Range
    src_range: Range

    @classmethod
    def from_line(cls, line: str) -> Self:
        # 50 98 2
        numbers = [ int(n) for n in line.strip().split() ]
        dst_range_start, src_range_start, range_length = numbers
        range_length -= 1

        type_range = Range(dst_range_start, dst_range_start + range_length)
        seed_range = Range(src_range_start, src_range_start + range_length)
        return cls(type_range, seed_range)

assert Mapping.from_line("50 98 2") == Mapping(Range(50, 51), Range(98, 99))


@dataclass
class SeedResult:
    number: int
    result: dict[str, int]


@dataclass
class SeedMapper:

    # seed_to_soil: Mapping
    # soil_to_fertilizer: Mapping
    # fertilizer_to_water: Mapping
    # water_to_light: Mapping
    # light_to_temperature: Mapping
    # temperature_to_humidity: Mapping
    # humidity_to_location: Mapping

    seeds: list[int]
    mappings: list[list[Mapping]]

    @staticmethod
    def _parse_seeds(seed_line: str) -> list[int]:
        # seeds: 79 14 55 13
        _, seed_numbers_line = seed_line.split(':')
        seed_numbers_line = seed_numbers_line.strip()

        return [ int(n) for n in seed_numbers_line.split(' ') ]
    
    @staticmethod
    def _parse_part(part_string: str) -> list[Mapping]:
        # fertilizer-to-water map:
        # 49 53 8
        # 0 11 42
        # 42 0 7
        # 57 7 4
        mapping_lines = part_string.split('\n')[1:]
        return [ Mapping.from_line(line) for line in mapping_lines ]

    @classmethod
    def from_string(cls, input_string: str) -> Self:
        parts = input_string.split('\n\n')

        seeds = cls._parse_seeds(parts[0])
        mappings = [
            cls._parse_part(part_string)
            for part_string in parts[1:]
        ]  
        return cls(seeds, mappings)
    
    def __repr__(self) -> str:
        from pprint import pformat

        mapping_formatted = pformat(self.mappings, width=60)
        return f"{self.seeds}\n{mapping_formatted}"
    
    def get_seed_mappings(self) -> list[SeedResult]:

        # for each seed, go through all the mappings
        # to end up at the configuration for each seed
        seed_results: list[SeedResult] = []
        for seed in self.seeds:

            mapping_types = [
                'soil',
                'fertitilizer',
                'water',
                'light',
                'temperature',
                'humidity',
                'location'
            ]
            seed_mapping = { k: 0 for k in mapping_types }
            v = seed
            for type_with_list in zip(mapping_types, self.mappings):

                # for each Mapping, check if `v` is in the range
                found_in_range = False
                type_, mapping_list = type_with_list
                for mapping in mapping_list:

                    if mapping.src_range.contains(v):
                        diff = v - mapping.src_range.min
                        v = mapping.dst_range.min + diff
                        seed_mapping[type_] = v
                        found_in_range = True
                        break

                if not found_in_range:
                    seed_mapping[type_] = v

            seed_results.append(SeedResult(seed, seed_mapping))
    
        return seed_results
    

@dataclass
class BonusSeedMapper:

    # seed_to_soil: Mapping
    # soil_to_fertilizer: Mapping
    # fertilizer_to_water: Mapping
    # water_to_light: Mapping
    # light_to_temperature: Mapping
    # temperature_to_humidity: Mapping
    # humidity_to_location: Mapping

    seeds: Generator[int, None, None]
    mappings: list[list[Mapping]]

    from typing import Generator

    @staticmethod
    def _parse_seeds(seed_line: str) -> chain[int]:
        # seeds: 79 14 55 13
        _, seed_numbers_line = seed_line.split(':')
        seed_numbers_line = seed_numbers_line.strip()

        seed_ranges = [ int(n) for n in seed_numbers_line.split(' ') ]
        assert len(seed_ranges) % 2 == 0

        from itertools import batched, chain

        seed_numbers = (
            range(start, start + length)
            for start, length in batched(seed_ranges, 2)
        )
        return chain(*seed_numbers)
    
    @staticmethod
    def _parse_part(part_string: str) -> list[Mapping]:
        # fertilizer-to-water map:
        # 49 53 8
        # 0 11 42
        # 42 0 7
        # 57 7 4
        mapping_lines = part_string.split('\n')[1:]
        return [ Mapping.from_line(line) for line in mapping_lines ]

    @classmethod
    def from_string(cls, input_string: str) -> Self:
        parts = input_string.split('\n\n')

        seeds = cls._parse_seeds(parts[0])
        mappings = [
            cls._parse_part(part_string)
            for part_string in parts[1:]
        ]  
        return cls(seeds, mappings)
    
    def __repr__(self) -> str:
        from pprint import pformat

        mapping_formatted = pformat(self.mappings, width=60)
        return f"{self.seeds}\n{mapping_formatted}"
    
    def get_lowest_location(self) -> int:

        # for each seed, go through all the mappings
        # to end up at the configuration for each seed
        lowest_location = None
        for seed in self.seeds:

            mapping_types = [
                'soil',
                'fertitilizer',
                'water',
                'light',
                'temperature',
                'humidity',
                'location'
            ]
            seed_mapping = { k: 0 for k in mapping_types }
            v = seed
            for type_with_list in zip(mapping_types, self.mappings):

                # for each Mapping, check if `v` is in the range
                found_in_range = False
                type_, mapping_list = type_with_list
                for mapping in mapping_list:

                    if mapping.src_range.contains(v):
                        diff = v - mapping.src_range.min
                        v = mapping.dst_range.min + diff
                        seed_mapping[type_] = v
                        found_in_range = True
                        break

                if not found_in_range:
                    seed_mapping[type_] = v

            if lowest_location is None or seed_mapping['location'] < lowest_location:
                lowest_location = seed_mapping['location']
    
        return lowest_location


class Day5(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 5

    def solve_part_one(self) -> Result:
        seed_mapper = SeedMapper.from_string(self._puzzle_input)
        results = seed_mapper.get_seed_mappings()
        return min(results, key=lambda x: x.result['location']).number
    
    def solve_part_two(self) -> Result:
        seed_mapper = BonusSeedMapper.from_string(self._puzzle_input)
        return seed_mapper.get_lowest_location()
