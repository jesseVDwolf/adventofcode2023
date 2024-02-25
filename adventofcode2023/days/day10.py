from typing import NamedTuple, Optional
from adventofcode2023.day import Day, Result
    

class Day10(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 10

    
    @staticmethod
    def find_start_coordinates(rows: str) -> tuple[int, int]:
        for y, row in enumerate(rows.split('\n')):
            x = row.find('S')
            if x > 0:
                return x, y
        
        raise ValueError(f'Starting possition not found.')
        
    
    def solve_part_one(self) -> Result:
        """The goal is to find the tile in the loop that is the furthest from the start.

        Returns:
            Result: Futhest number of tiles from the starting tile
        """

        x, y = self.find_start_coordinates(self._puzzle_input)
        pipe_grid = [ s.strip() for s in self._puzzle_input.split('\n') ]
        
        # Each pipe connects to two ends
        pipe_ends = {
            "|": [ ( 0,-1), ( 0, 1) ],
            "-": [ (-1, 0), ( 1, 0) ],
            "L": [ ( 0,-1), ( 1, 0) ],
            "J": [ ( 0,-1), (-1, 0) ],
            "7": [ (-1, 0), ( 0, 1) ],
            "F": [ ( 1, 0), ( 0, 1) ],
        }

        from queue import Queue

        q = Queue()

        # load the initial queue with the two starting points
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            char = pipe_grid[y + dy][x + dx]
            if char in pipe_ends:
                for dx2, dy2 in pipe_ends[char]:
                    
                    # check if S is on the end or start of any of the pipe types
                    # taking into account original location (x, y) + the direction
                    # (dx, dy) and the end of the pipe (dx2, dy2)
                    if x == (x + dx + dx2) and y == (y + dy + dy2):

                        # add the position of that pipe
                        q.put((1, (x + dx, y + dy)))

        # The starting point must have only 2 entrances:
        # one ingoing and one outgoing.
        assert q.qsize() == 2

        # Do bookkeeping on where you've already been.
        # for each coordinate track the amount of times you've
        # been there. Start with the start position (x, y) 'S'
        dist = {(x, y): 0}
        while not q.empty():
            # get new coordinate to check
            d, (x, y) = q.get()

            # If we've already passed this coordinate then
            # ignore it and move to the next item in the queue
            if (x, y) in dist:
                continue

            # add the new coordinate
            dist[(x, y)] = d
            
            # Add new coordinates to check to the queue
            for dx, dy in pipe_ends[pipe_grid[y][x]]:
                q.put((d + 1, (x + dx, y + dy)))
    
        return max(dist.values())
    
    def solve_part_two(self) -> Result:
        return 1
    

if __name__ == '__main__':
    day = Day10()
    print(day.solve_part_one())

