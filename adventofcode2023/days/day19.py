from dataclasses import dataclass
from enum import Enum, auto
import re
from textwrap import dedent
from typing import NamedTuple, Optional, Protocol
from adventofcode2023.day import Day, Result

class Rating(NamedTuple):
    x: int
    m: int
    a: int
    s: int


@dataclass
class Workflow:
    ops: list[str]


WorkflowMap = dict[str, Workflow]

class State(Enum):
    START = auto()
    PROCESS = auto()

class WorkflowHandler:


    def __init__(self, workflows: WorkflowMap) -> None:
        self._workflows = workflows
        self._init_attr()
    
    def _init_attr(self) -> None:
        self._workflow: Optional[Workflow] = None
        self._workflow_index = 0
        self._state = State.START
    
    def _reset(self) -> None:
        self._init_attr()
    
    def process(self, rating: Rating) -> bool:

        accepted = None
        while accepted is None:

            match self._state:

                case State.START:
                    self._workflow = self._workflows['in']
                    self._state = State.PROCESS

                case State.PROCESS:
                    assert self._workflow is not None
                    
                    instruction = self._workflow.ops[self._workflow_index]
                    if ':' in instruction:
                        condition, goto = instruction.split(':')
                        left, right = re.split(r'<|>', condition)

                        passed = False
                        v = rating.__getattribute__(left)
                        if '<' in condition:
                            if v < int(right):
                                passed = True
                        else:
                            if v > int(right):
                                passed = True
                        
                        if passed is True:
                            if goto == 'R':
                                accepted = False
                            elif goto == 'A':
                                accepted = True
                            else:
                                self._workflow = self._workflows[goto]
                                self._workflow_index = 0
                        else:
                            self._workflow_index += 1
                    else:
                        goto = instruction
                        if goto == 'R':
                            accepted = False
                        elif goto == 'A':
                            accepted = True
                        else:
                            self._workflow = self._workflows[goto]
                            self._workflow_index = 0

        self._reset()
        return accepted



class Day19(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)

    @property
    def day(self) -> int:
        return 19
    
    @staticmethod
    def parse_workflows(w: str) -> WorkflowMap:
        workflows: dict[str, Workflow] = {}
        for s in w.split('\n'):
            idx = s.find('{')
            key = s[:idx]
            wf = Workflow(s[idx+1:-1].split(','))
            workflows[key] = wf
        
        return workflows
    
    @staticmethod
    def parse_ratings(r: str) -> list[Rating]:
        ratings: list[Rating] = []
        for s in r.split('\n'):
            components = s[1:-1].split(',')
            rating = Rating(*[
                int(x[x.find('=') + 1:])
                for x in components
            ])
            ratings.append(rating)
        
        return ratings
    
    def solve_part_one(self) -> Result:
        workflows, ratings = self._puzzle_input.split('\n\n')
        workflows = workflows.strip()
        workflows = self.parse_workflows(workflows)

        ratings = ratings.strip()
        ratings = self.parse_ratings(ratings)

        handler = WorkflowHandler(workflows)

        return sum( sum(rating) for rating in ratings if handler.process(rating) == True )
    
    def solve_part_two(self) -> Result:
        return super().solve_part_two()


if __name__ == '__main__':
    example_input = dedent("""
    px{a<2006:qkq,m>2090:A,rfg}
    pv{a>1716:R,A}
    lnx{m>1548:A,A}
    rfg{s<537:gd,x>2440:R,A}
    qs{s>3448:A,lnx}
    qkq{x<1416:A,crn}
    crn{x>2662:A,R}
    in{s<1351:px,qqz}
    qqz{s>2770:qs,m<1801:hdj,R}
    gd{a>3333:R,R}
    hdj{m>838:A,pv}

    {x=787,m=2655,a=1222,s=2876}
    {x=1679,m=44,a=2067,s=496}
    {x=2036,m=264,a=79,s=2244}
    {x=2461,m=1339,a=466,s=291}
    {x=2127,m=1623,a=2188,s=1013}""").strip()
    day = Day19()
    print(day.solve_part_one())
