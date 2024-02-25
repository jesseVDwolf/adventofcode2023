import heapq
from textwrap import dedent
from time import sleep
from typing import NamedTuple, Optional

import numpy as np
from adventofcode2023.day import Day, Result

# The goal of this day is minimize heat loss.
# The puzzle input represents a grid of numbers
# where each number represents a city block to
# go through. The number itself represents the
# heat loss incurred on the crucible.
# Important:
# - You start in the top left
# - The goal is the bottom right
# - You may only travel 3 consecutive spaces in the same direction
# - You may not go back
#   - Example: If going right, the next step may only be up, down, right

# Implementation
# - A* algorithm: https://en.wikipedia.org/wiki/A*_search_algorithm
# - https://docs.python.org/3/library/heapq.html
#   - A priority queue
# - We need a heuristic function that takes into account the constraints
#   set by the assignment: Only three steps in the same direction and not backwards

class Point(NamedTuple):
    x: int
    y: int

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
DIRS = [ UP, DOWN, LEFT, RIGHT ]

class Node(NamedTuple):
    f_score: int
    g_score: int
    cost: int
    loc: Point

def heuristic(grid: np.ndarray, p: Point) -> int:
    column = grid[p.y:, p.x]
    row = grid[-1, p.x + 1:]
    return sum(column) + sum(row)

a = [
    [1, 2, 5, 8, 3],
    [4, 2, 9, 1, 5],
    [3, 2, 6, 7, 4]
]
assert heuristic(np.array(a, dtype=np.int8), Point(2, 1)) == 26


class PriorityQueue:

    def __init__(self) -> None:
        self._elements: list[Node] = []

    def empty(self) -> bool:
        return len(self._elements) == 0

    def push(self, element: Node) -> None:
        heapq.heappush(self._elements, element)
    
    def pop(self) -> Node:
        return heapq.heappop(self._elements)


class Day17(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
    
    @property
    def day(self) -> int:
        return 17
    
    @staticmethod
    def _outside_of_grid(grid: np.ndarray, p: Point) -> bool:
        x, y = p
        rows, cols = grid.shape

        return x < 0 or y < 0 or y >= rows or x >= cols
    
    def solve_part_one(self) -> Result:
        grid = np.array(
            object=[
                [ int(c) for c in row ]
                for row in self._puzzle_input.split('\n')
            ],
            dtype=np.dtype('int8')
        )
        p_start = Point(0, 0)
        p_goal = Point(x=grid.shape[1] -1, y=grid.shape[0] -1)

        # starting node at (0, 0) with a cost of grid[0][0].
        # each Node keeps track of where it last came from.
        # this is because you can not go 3 steps in the same
        # direction.
        starting_node = Node(
            cost=0,
            loc=p_start,
            f_score=0,
            g_score=heuristic(grid, p_start)
        )

        # Each key represents a Node since its location is unique
        # the value represents a map of directions that that node
        # has been following.
        node_directions: dict[Node, dict[Point, int]] = {}

        # keep track of the cheapest existing path from start to goal.
        # paths[n] where n is the location of a Node, will give back
        # the previous node from where it originated.
        paths: dict[Node, Optional[Node]] = {}

        q = PriorityQueue()
        q.push(starting_node)

        while not q.empty():

            # Since it's a priority queue (min-heap) the Node
            # with the lowest cost will be popped from the Queue
            node = q.pop()

            sleep(0.5)
            print(node)
            
            # exit condition is where the Node put onto the queue
            # has reached the goal location.
            if node.loc == p_goal:
                print("Goal reached")
                break
            
            directions = node_directions[node]
            for d, times_travelled in directions.items():

                # coordinates of the new node to be visited
                new_location = Point(x=node.loc.x + d.x, y=node.loc.y + d.y)
                if self._outside_of_grid(grid, new_location):
                    continue

                # there should be one direction with a value > 0 so
                # this is the direction that is currently followed.
                # Exception here is the starting node.
                current_direction = max(directions.items(), key=lambda x: x[1])[0]

                # nodes are not allowed to move in opposite directions
                # and they are not allowed to move in the same direction
                # for more then 3 times.
                opposite_d = Point(-current_direction.x, -current_direction.y)
                if (node.loc != p_start and d == opposite_d) or times_travelled >= 3:
                    continue
                
                # reset all other directions but increase
                # the one in which we're currently moving
                new_directions = { d: 0 for d in DIRS }
                new_directions[d] = directions[d] + 1

                # cost of the new node f(n) = g(n) + h(n) where
                # g(n) is the cost of the current node plus all
                # preceding once and h(n) is a heuristic function
                # that estimates the cost from the current node
                # to the goal
                # tentative_g_score = node.g_score + grid[new_location.y][new_location.x]

                # cost_new_node = grid[new_location.y][new_location.x] + node.cost + heuristic(grid, new_location)
            
                # # TODO use paths
                # new_node = Node(cost=cost_new_node, loc=new_location)
                # q.push(new_node)
                # node_directions[new_node] = new_directions


        return super().solve_part_one()
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()


if __name__ == '__main__':
    example_input = dedent("""
    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533
    """).strip()
    day = Day17(example_input)
    print(day.solve_part_one())