import fileinput
import math
from collections import defaultdict, Counter, deque
from copy import deepcopy


class Broadcaster:
    def __init__(self, name, dests) -> None:
        self.name = name
        self.dests = dests
        self.modules = None
        self.to_send = []

    def receive(self, pulse):
        self.to_send.append(pulse)

    def send(self):
        sent = []
        for pulse in self.to_send:
            for dest in self.dests:
                self.modules[dest].receive(pulse, self.name)
            sent.append(pulse)
        self.to_send = []
        return self.dests, sent

    def __repr__(self) -> str:
        return f"Broadcaster(name={self.name})"


class FlipFlop:
    """
    Flip-flop modules (prefix %)
    Are either on or off;
    Initially off.
    If receives a high pulse, it is ignored and nothing happens.
    If receives a low pulse, it flips between on and off.
        If it was off, it turns on and sends a high pulse.
        If it was on, it turns off and sends a low pulse.
    """

    def __init__(self, name, dests):
        self.name = name
        self.on = False
        self.dests = dests
        self.modules = None
        self.to_send = []

    def receive(self, pulse, input):
        if pulse == "lo":
            self.toggle()
            pulse = "hi" if self.on else "lo"
            self.to_send.append(pulse)

    def send(self):
        sent = []
        if self.to_send:
            for pulse in self.to_send:
                for dest in self.dests:
                    self.modules[dest].receive(pulse, self.name)
                sent.append(pulse)
            self.to_send = []
            return self.dests, sent
        return [], []

    def toggle(self):
        self.on = not self.on

    def __repr__(self) -> str:
        return f"FlipFlop(name={self.name}, on={self.on}))"


class Conjunction:
    """
    Conjunction modules (prefix &)
    Remember the type of the most recent pulse received from each of their connected input modules;
    They initially default to remembering a low pulse for each input.
    When a pulse is received, the conjunction module first updates its memory for that input.
    Then, if it remembers high pulses for all inputs, it sends a low pulse;
    otherwise, it sends a high pulse.
    """

    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self.inputs = []
        self.memo = dict()
        self.modules = None
        self.to_send = []

    def register(self, input):
        self.inputs.append(input)
        self.memo[input] = "lo"

    def receive(self, pulse, input):
        self.memo[input] = pulse

        self.to_send.append(self.pulse())

    def pulse(self):
        pulse_ = "hi"
        if all(self.memo[input] == "hi" for input in self.inputs):
            pulse_ = "lo"
        return pulse_

    def send(self):
        sent = []
        for pulse in self.to_send:
            for dest in self.dests:
                if dest in self.modules:
                    self.modules[dest].receive(pulse, self.name)
            sent.append(pulse)
        self.to_send = []
        return self.dests, sent

    def __repr__(self) -> str:
        return f"Conjunction(name={self.name}, memo={self.memo})"


def parse():
    network = defaultdict(list)
    types = {}
    modules = {}
    for line in fileinput.input():
        left, right = line.strip().split(" -> ")
        right = right.strip().split(", ")

        if left != "broadcaster":
            type_, left = left[0], left[1:]
            types[left] = type_

            if type_ == "%":
                modules[left] = FlipFlop(name=left, dests=right)
            elif type_ == "&":
                modules[left] = Conjunction(name=left, dests=right)
            else:
                assert False, type_
        else:
            type_ = "b"
            modules[left] = Broadcaster(name=left, dests=right)

        network[left].extend(right)

    for name, dests in network.items():
        for dest in dests:
            if types.get(dest) == "&":
                modules[dest].register(name)

        modules[name].modules = modules

    return network, types, modules


def step(network, modules, s=None, verbose=False):
    c = Counter()
    broadcaster: Broadcaster = modules["broadcaster"]
    if verbose:
        print(f"button -low-> broadcaster")
    broadcaster.receive("lo")
    c["lo"] += 1
    receivers, pulses = broadcaster.send()
    if verbose:
        for r in receivers:
            print(f"broadcaster -{pulses}-> {r}")
    for pulse in pulses:
        c[pulse] += len(receivers)

    while receivers:
        nreceivers = []
        for next_ in receivers:
            if next_ not in modules:
                receivers = []
                nreceivers.extend(receivers)
                receivers = nreceivers
                continue
            module = modules[next_]
            receivers, pulses = module.send()
            if verbose:
                for r in receivers:
                    print(f"{next_} -{pulses}-> {r}")
            if pulses:
                for pulse in pulses:
                    c[pulse] += len(receivers)
            nreceivers.extend(receivers)
            receivers = nreceivers

    return c


def step_with_cycles(network, modules, cycles, s=None):
    c = Counter()
    broadcaster: Broadcaster = modules["broadcaster"]
    broadcaster.receive("lo")
    c["lo"] += 1
    receivers, pulses = broadcaster.send()
    for pulse in pulses:
        c[pulse] += len(receivers)

    found = False

    while receivers:
        nreceivers = []
        for next_ in receivers:
            if next_ not in modules:
                receivers = []
                nreceivers.extend(receivers)
                receivers = nreceivers
                continue
            module = modules[next_]
            receivers, pulses = module.send()

            if next_ in cycles and not cycles[next_] and "hi" in pulses:
                cycles[next_] = s + 1
                if all(cycles.values()):
                    found = True

            if pulses:
                for pulse in pulses:
                    c[pulse] += len(receivers)
            nreceivers.extend(receivers)
            receivers = nreceivers

    return c, found


def run(network, modules, steps=1, verbose=False):
    C = Counter()
    for s in range(steps):
        c = step(network, modules, s=s, verbose=verbose)
        C += c
    return C


def find_cycles(network, modules, steps=1):
    cycles = {m: None for m in modules["th"].inputs}

    for s in range(steps):
        _, found = step_with_cycles(network, modules, cycles, s)

        if found:
            return math.lcm(*cycles.values())


def search(network, start, target):
    queue = deque([(start, [start], set())])

    paths = []
    while queue:
        node, path, seen = queue.popleft()

        if node == target:
            paths.append(path)
            continue

        if node in seen:
            continue

        for next_ in network[node]:
            queue.append((next_, path + [next_], {*seen, node}))
    return paths


def main():
    network, types, modules = parse()
    count = run(network, deepcopy(modules), steps=1_000)
    print(f"Part 1: {math.prod(count.values())}")
    print(f"Part 2: {find_cycles(network, deepcopy(modules), steps=10_000)}")


if __name__ == "__main__":
    main()
