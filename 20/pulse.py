from __future__ import annotations
import fileinput
import math
from collections import defaultdict, Counter, deque
from copy import deepcopy
from typing import Dict, List, Tuple


class Module:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.to_send: List[str] = []

    def connect(self, dests: List[Module]) -> None:
        self.dests = dests

    def receive(self, pulse: str, input: str) -> None:
        raise NotImplementedError()

    def send(self) -> Tuple[List[Module], List[str]]:
        sent: List[str] = []
        if not self.to_send:
            return [], []

        for pulse in self.to_send:
            for dest in self.dests:
                dest.receive(pulse, self.name)
            sent.append(pulse)
        self.to_send = []
        return self.dests, sent


class NoOp(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def receive(self, pulse: str, input: str) -> None:
        return

    def send(self) -> Tuple[List[Module], List[str]]:
        return [], []


class Broadcaster(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def receive(self, pulse: str, input: str) -> None:
        self.to_send.append(pulse)

    def __repr__(self) -> str:
        return f"Broadcaster(name={self.name})"


class FlipFlop(Module):
    """
    Flip-flop modules (prefix %)
    Are either on or off;
    Initially off.
    If receives a high pulse, it is ignored and nothing happens.
    If receives a low pulse, it flips between on and off.
        If it was off, it turns on and sends a high pulse.
        If it was on, it turns off and sends a low pulse.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.on = False

    def receive(self, pulse: str, input: str) -> None:
        if pulse == "lo":
            self.toggle()
            pulse = "hi" if self.on else "lo"
            self.to_send.append(pulse)

    def toggle(self):
        self.on = not self.on

    def __repr__(self) -> str:
        return f"FlipFlop(name={self.name}, on={self.on}))"


class Conjunction(Module):
    """
    Conjunction modules (prefix &)
    Remember the type of the most recent pulse received from each of their connected input modules;
    They initially default to remembering a low pulse for each input.
    When a pulse is received, the conjunction module first updates its memory for that input.
    Then, if it remembers high pulses for all inputs, it sends a low pulse;
    otherwise, it sends a high pulse.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.inputs = []
        self.memo = dict()

    def register(self, input):
        self.inputs.append(input)
        self.memo[input] = "lo"

    def receive(self, pulse: str, input: str) -> None:
        self.memo[input] = pulse
        self.to_send.append(self.pulse())

    def pulse(self) -> str:
        pulse_ = "hi"
        if all(self.memo[input] == "hi" for input in self.inputs):
            pulse_ = "lo"
        return pulse_

    def __repr__(self) -> str:
        return f"Conjunction(name={self.name}, memo={self.memo})"


def parse():
    network = defaultdict(list)
    types = {}
    nodes = set()
    modules = {}
    for line in fileinput.input():
        left, right = line.strip().split(" -> ")
        right = right.strip().split(", ")

        if left.startswith("%"):
            type_, left = left[0], left[1:]
            types[left] = type_
            modules[left] = FlipFlop(name=left)
        elif left.startswith("&"):
            type_, left = left[0], left[1:]
            types[left] = type_
            modules[left] = Conjunction(name=left)
        elif left.startswith("broadcaster"):
            modules[left] = Broadcaster(name=left)

        nodes.add(left)
        nodes.update(set(right))

        network[left].extend(right)

    for node in nodes:
        if node not in modules:
            modules[node] = NoOp(name=node)

    for name, dests in network.items():
        modules[name].connect([modules[d] for d in dests])
        for dest in dests:
            if types.get(dest) == "&":
                modules[dest].register(name)

    return network, types, modules


def step(modules: Dict[str, Module], cycles=None, s=None, verbose=False):
    c = Counter({"lo": 1})

    broadcaster: Broadcaster = modules["broadcaster"]
    broadcaster.receive("lo", "button")
    receivers, pulses = broadcaster.send()
    for pulse in pulses:
        c[pulse] += len(receivers)

    queue = deque(receivers)

    if verbose:
        print(f"button -low-> broadcaster")
        for r in receivers:
            print(f"broadcaster -{pulses}-> {r}")

    found = False

    while queue:
        receiver = queue.popleft()

        receivers, pulses = receiver.send()
        for pulse in pulses:
            c[pulse] += len(receivers)

        for to_process in receivers:
            queue.append(to_process)

        if cycles:
            if (
                receiver.name in cycles
                and cycles[receiver.name] is None
                and "hi" in pulses
            ):
                cycles[receiver.name] = s + 1
                if all(cycles.values()):
                    found = True

    return c, found


def run(modules, steps=1, verbose=False):
    C = Counter()
    for s in range(steps):
        c, _ = step(modules, s=s, verbose=verbose)
        C += c
    return C


def find_cycles(modules, steps=1, verbose=False):
    cycles = {m: None for m in modules["th"].inputs}
    for s in range(steps):
        _, found = step(modules, cycles, s=s, verbose=verbose)
        if found:
            return math.lcm(*cycles.values())
    return -1


def main():
    network, types, modules = parse()
    count = run(deepcopy(modules), steps=1_000)
    print(f"Part 1: {math.prod(count.values())}")
    print(f"Part 2: {find_cycles(deepcopy(modules), steps=10_000)}")


if __name__ == "__main__":
    main()
