from __future__ import annotations
from dataclasses import dataclass, field
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])
Move = namedtuple("Move", ["direction", "distance"])


@dataclass
class RopeKnot:
    name: str
    history: list[Position] = field(default_factory=lambda: [Position(0, 0)])
    head: RopeKnot | None = None
    tail: RopeKnot | None = None

    @property
    def position(self) -> Position | None:
        return self.history[-1] if self.history else None

    def __str__(self) -> str:
        return f"{self.name} {self.position}"

    def set_position(self, *args):
        self.history.append(Position(*args))
        if self.tail:
            self.tail.reposition()

    def reposition(self):
        """reposition self to match knot at head"""
        if not self.head:
            raise ValueError("Headless Knot")
        # check move not needed
        if (
            abs(self.head.position.x - self.position.x) <= 1
            and abs(self.head.position.y - self.position.y) <= 1
        ):
            # if the head is close enough, don't move
            self.set_position(*self.position)
        else:
            tail_x, tail_y = self.position
            if self.head.position.x > tail_x:
                tail_x += 1
            if self.head.position.x < tail_x:
                tail_x -= 1
            if self.head.position.y > tail_y:
                tail_y += 1
            if self.head.position.y < tail_y:
                tail_y -= 1
            self.set_position(tail_x, tail_y)

    def process_move(self, direction: str):
        current_position = self.position
        if direction in {"L", "R"}:
            self.set_position(
                current_position.x + (-1 if direction == "L" else 1), current_position.y
            )
        else:
            self.set_position(
                current_position.x, current_position.y + (-1 if direction == "D" else 1)
            )

    def process_moves(self, moves: list[Move]):
        """process the moves file"""
        for direction, distance in moves:
            for _ in range(distance):
                self.process_move(direction)

    @property
    def number_of_positions(self):
        """answer to part 1"""
        return len(set(self.history))

    def __str__(self):
        return f"{self.name} {self.position} <- {self.tail}"


with open("day9-input.txt") as f:
    moves = [row.replace("\n", "").split() for row in f]
    moves = [Move(m[0], int(m[1])) for m in moves]

head = RopeKnot("H")
head.tail = RopeKnot("T")
head.tail.head = head
tail = head.tail
head.process_moves(moves)
print(f"{tail.number_of_positions=}")

### PART 2 ###


# Build chain
head = RopeKnot("H")
tail = head
for x in range(1, 10):
    tail.tail = RopeKnot(x)
    tail.tail.head = tail
    tail = tail.tail
head.process_moves(moves)

print(f"{tail.number_of_positions=}")
