import re
from collections import defaultdict
from dataclasses import dataclass


def process_initial(lines: list[str]) -> dict[str, list]:
    """dynamically build the initial layout"""
    lines.reverse()
    data = defaultdict(list)
    index = {idx: character for idx, character in enumerate(lines[0]) if character != " "}

    for line in lines[1:]:
        for idx, name in index.items():
            if line[idx] != " ":
                data[name].append(line[idx])
    return data


@dataclass
class Move:
    qty: int
    from_stack: str
    to_stack: str

    def __post_init__(self):
        """convert the number of moves to int"""
        self.qty = int(self.qty)


def process_moves(lines: list[str]) -> list[Move]:
    return [Move(*(re.findall(r"\d+", line))) for line in lines if line]


with open("day5-input.txt") as f:
    header, moves = f.read().split("\n\n")
    cargo_hold = process_initial(header.split("\n"))
    moves_data = process_moves(moves.split("\n"))

# Process the moves
for move in moves_data:
    in_flight = cargo_hold[move.from_stack][-move.qty :]
    in_flight.reverse()
    cargo_hold[move.from_stack] = cargo_hold[move.from_stack][: -move.qty]
    cargo_hold[move.to_stack].extend(in_flight)

top = [stacks[-1] for stacks in cargo_hold.values()]
print("".join(top))

# PART 2
with open("day5-input.txt") as f:
    header, moves = f.read().split("\n\n")
    cargo_hold = process_initial(header.split("\n"))
    moves_data = process_moves(moves.split("\n"))

# Process the moves
for move in moves_data:
    in_flight = cargo_hold[move.from_stack][-move.qty :]
    cargo_hold[move.from_stack] = cargo_hold[move.from_stack][: -move.qty]
    cargo_hold[move.to_stack].extend(in_flight)

top = [stacks[-1] for stacks in cargo_hold.values()]
print("".join(top))
