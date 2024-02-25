from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from pprint import pprint
from queue import Queue
from textwrap import dedent
from typing import Optional, Self, Type, cast
from adventofcode2023.day import Day, Result

# important notes
# - Pulses are always processed in the order they are sent.
#   - Use a Queuing system
# - Pulses can either be LOW or HIGH
# - Each module has a list of destination modules
# - Module types
#   - Flip-Flop
#   - Conjunction
#   - Broadcast
#   - Button

"""
When the button is pressed, a low pulse is send to the broacaster module.
- assert amount_of_broadcaster == 1

The broadcaster sends a low pulse to its destination modules. These pulses
are added to the Queue. We take a pulse from the Queue and see its type and
receiver. We find the receiving module and look at its destination modules.
We ask the Module to give us back a pulse based on the Pulse we give it. This
new pulse is then added to the queue also. We can do this in a loop.
"""

class PulseType(Enum):
    HIGH = auto()
    LOW = auto()

@dataclass
class Pulse:
    type: PulseType
    sender: str
    receiver: str

    def __eq__(self, __value: object) -> bool:        
        other = cast(Self, __value)
        return self.type == other.type and self.receiver == other.receiver


class Module(ABC):

    _prefix = None

    def __init__(self, key: str, inputmodules: list[str], destmodules: list[str]) -> None:
        super().__init__()
        self._key = key
        self._inputmodules = inputmodules
        self._destmodules = destmodules
    

    def destmodules(self) -> list[str]:
        return self._destmodules
    
    def inputmodules(self) -> list[str]:
        return self._inputmodules
    
    def key(self) -> str:
        return self._key
    
    def prefix(self) -> str:
        if self._prefix is None:
            raise NotImplementedError("Overwrite _prefix in child class")
        return self._prefix
    
    def register_inputmodules(self, modules: list[Self]) -> None:
        """Add module keys to _inputmodules if other module specifies it in
        its destination modules.

        Args:
            modules (list[Self]): List of modules
        """
        for m in modules:
            if self.key() in m.destmodules():
                self._inputmodules.append(m.key())
    
    @abstractmethod
    def pulse(self, recvpuls: Pulse) -> list[Pulse]:
        """Generate new pulses based on incoming pulse

        Args:
            recvpuls (Pulse): Incoming Pulse object

        Returns:
            list[Pulse]: List of outgoing Pulses
        """
        ...



class ModuleManager:
    """ The ModuleManager manages one button, one broadcaster,
    n amount of FlipFlops and n amount of Conjuction modules.

    The manager keeps a Queue in which it stores the pulses to
    be send. It checks the destination modules of each module
    when it receives a pulse and decides on follow-up actions.
    """
    _registered_module_cls: dict[str, Type[Module]] = {}

    def __init__(self, modules: dict[str, Module]) -> None:
        self._modules = modules
        self._low_pulses_send = 0
        self._high_pulses_send = 0
        self._button_presses = 0
        self._found_pulse = False

    @classmethod
    def register(cls, module: Type[Module]):
        assert module._prefix is not None

        cls._registered_module_cls[module._prefix] = module
        return cls

    @classmethod
    def from_module_configuration(cls, module_config: str) -> Self:
        modules: dict[str, Module] = {}
        for module_string in module_config.split('\n'):

            for prefix, module in cls._registered_module_cls.items():

                if module_string.startswith(prefix):
                    key, destmodules = module_string.split('->')
                    key = key.strip()

                    if prefix != 'broadcaster':
                        key = key[1:]
                    
                    destmodules = [ key.strip() for key in destmodules.split(',') ]
                    modules[key] = module(key, [], destmodules)
        
        for module in modules.values():
            module.register_inputmodules([
                m for (k, m) in modules.items() if k != module.key()
            ])

        return cls(modules)

    def found_pulse(self) -> bool:
        return self._found_pulse
    
    def button_presses(self) -> int:
        return self._button_presses

    def pulse_product(self) -> int:
        return self._low_pulses_send * self._high_pulses_send

    def press_button(self, look_for_pulse: Optional[Pulse] = None) -> None:
        """Pressing the button module sends a LOW pulse to the broadcaster, who forwards the
        signal to all its destination modules, who process the pulse and send more pulses. This
        continues untill no more pulses are send.
        """
        self._button_presses += 1
        queue: Queue[Pulse] = Queue()
        
        low_pulse_from_button = Pulse(
            sender='button',
            receiver='broadcaster',
            type=PulseType.LOW
        )
        queue.put(low_pulse_from_button)
        while not queue.empty():

            pulse = queue.get()
            if look_for_pulse is not None and pulse == look_for_pulse:
                self._found_pulse = True
                break

            if pulse.type == PulseType.LOW:
                self._low_pulses_send += 1
            else:
                self._high_pulses_send += 1
            
            if (receiving_module := self._modules.get(pulse.receiver)) is not None:
                for generated_pulse in receiving_module.pulse(pulse):
                    queue.put(generated_pulse)



class FlipFlopState(Enum):
    ON = auto()
    OFF = auto()


@ModuleManager.register
class FlipFlop(Module):
    """ Flip-flop modules (prefix %) are either on or off;
    they are initially off. If a flip-flop module receives
    a high pulse, it is ignored and nothing happens.
    
    However, if a flip-flop module receives a low pulse, it
    flips between on and off. If it was off, it turns on and
    sends a high pulse. If it was on, it turns off and sends
    a low pulse."""

    _prefix = '%'

    def __init__(self, key: str, inputmodules: list[str], destmodules: list[str]) -> None:
        super().__init__(key, inputmodules, destmodules)
        self._state = FlipFlopState.OFF

    def pulse(self, recvpuls: Pulse) -> list[Pulse]:
        if recvpuls.type == PulseType.HIGH:
            return []
        else:
            if self._state == FlipFlopState.ON:
                self._state = FlipFlopState.OFF
                return [
                    Pulse(sender=self._key, receiver=module, type=PulseType.LOW)
                    for module in self.destmodules()
                ]
            else:
                self._state = FlipFlopState.ON
                return [
                    Pulse(sender=self._key, receiver=module, type=PulseType.HIGH)
                    for module in self.destmodules()
                ]


@ModuleManager.register
class Conjunction(Module):
    """ Conjunction modules (prefix &) remember the type of
    the most recent pulse received from each of their connected
    input modules; they initially default to remembering a low
    pulse for each input. When a pulse is received, the conjunction
    module first updates its memory for that input. Then, if it
    remembers high pulses for all inputs, it sends a low pulse;
    otherwise, it sends a high pulse."""

    _prefix = '&'
    
    def __init__(self, key: str, inputmodules: list[str], destmodules: list[str]) -> None:
        super().__init__(key, inputmodules, destmodules)
        self._pulse_memory = {}
    
    def register_inputmodules(self, modules: list[Self]) -> None:
        for m in modules:
            if self.key() in m.destmodules():
                self._inputmodules.append(m.key())
                self._pulse_memory[m.key()] = PulseType.LOW
    
    def pulse(self, recvpuls: Pulse) -> list[Pulse]:
        self._pulse_memory[recvpuls.sender] = recvpuls.type
        if all( type_ == PulseType.HIGH for type_ in self._pulse_memory.values() ):
            return [
                Pulse(sender=self._key, receiver=module, type=PulseType.LOW)
                for module in self.destmodules()
            ]
        else:
            return [
                Pulse(sender=self._key, receiver=module, type=PulseType.HIGH)
                for module in self.destmodules()
            ]
    

@ModuleManager.register
class Broadcaster(Module):
    """ When the Broadcaster receives a pulse, it sends the same pulse to all of its destination modules. """

    _prefix = 'broadcaster'
    
    def __init__(self, _: str, inputmodules: list[str], destmodules: list[str]) -> None:
        super().__init__('broadcaster', inputmodules, destmodules)

    def pulse(self, recvpuls: Pulse) -> list[Pulse]:
        return [
            Pulse(sender=self._key, receiver=module, type=recvpuls.type)
            for module in self.destmodules()
        ]


class Day20(Day):

    def __init__(self, puzzle_input: str | None = None) -> None:
        super().__init__(puzzle_input)
    
    @property
    def day(self) -> int:
        return 20
    
    def solve_part_one(self) -> Result:
        manager = ModuleManager.from_module_configuration(self._puzzle_input)
        for _ in range(1000):
            manager.press_button()

        return manager.pulse_product()
    
    def solve_part_two(self) -> Result:
        manager = ModuleManager.from_module_configuration(self._puzzle_input)
        while not manager.found_pulse():
            manager.press_button(Pulse(PulseType.LOW, '', 'rx'))
            if manager.button_presses() % 5000 == 0:
                print(manager.button_presses())
        
        return manager.button_presses()


if __name__ == '__main__':
    example_input = dedent("""
    broadcaster -> a, b, c
    %a -> b
    %b -> c
    %c -> inv
    &inv -> a""").strip()

    example_input = dedent("""
    broadcaster -> a
    %a -> inv, con
    &inv -> b
    %b -> con
    &con -> output""").strip()
    day = Day20()
    print(day.solve_part_one())
    print(day.solve_part_two())
