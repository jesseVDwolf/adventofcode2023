from adventofcode2023.day import Day, Result

Network = dict[str, tuple[str, str]]

class Day8(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 8
    
    def parse_input(self) -> (str, Network):
        lines = self._puzzle_input.split("\n")
        instructions = lines[0]

        network: dict[str, tuple[str, str]] = {}
        for line in lines[2:]:
            key_string, value_string = line.split("=")
            key = key_string.strip()

            left, right = value_string.split(", ")
            left = left.strip()[1:]
            right = right[:-1]

            network[key] = (left, right)

        return instructions, network

    def get_steps_to_end(self, instructions: str, network: Network) -> int:
        steps = 1
        node = 'AAA'
        while True:
            
            end_found = False
            for ins in instructions:

                left_node, right_node = network[node]
                node = right_node if ins == 'R' else left_node

                if node == 'ZZZ':
                    end_found = True
                    break

                steps += 1
            
            if end_found is True:
                break

        return steps
    
    def solve_part_one(self) -> Result:
        return self.get_steps_to_end(*self.parse_input())
    
    def solve_part_two(self) -> Result:
        return 1


if __name__ == '__main__':
    pass