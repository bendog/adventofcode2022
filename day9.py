from dataclasses import dataclass, field
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])
Move = namedtuple("Move", ["direction", "distance"])


@dataclass
class RopeEnd:
    name: str
    history: list[Position] = field(default_factory=list)

    @property
    def position(self) -> Position | None:
        return self.history[-1] if self.history else None

    def set_position(self, *args):
        self.history.append(Position(*args))

    def __str__(self) -> str:
        return f"{self.name} {self.position}"


class Rope:
    def __init__(self):
        self.head = RopeEnd("head")
        self.head.set_position(0, 0)
        self.tail = RopeEnd("tail")
        self.tail.set_position(0, 0)

    def move_head(self, direction: str):
        current_position = self.head.position
        if direction in {"L", "R"}:
            self.head.set_position(
                current_position.x + (-1 if direction == "L" else 1), current_position.y
            )
        else:
            self.head.set_position(
                current_position.x, current_position.y + (-1 if direction == "D" else 1)
            )

    def move_tail(self):
        # check move not needed
        if (
            abs(self.head.position.x - self.tail.position.x) <= 1
            and abs(self.head.position.y - self.tail.position.y) <= 1
        ):
            # if the head is close enough, don't move
            self.tail.set_position(*self.tail.position)
        else:
            tail_x, tail_y = self.tail.position
            if self.head.position.x > tail_x:
                tail_x += 1
            if self.head.position.x < tail_x:
                tail_x -= 1
            if self.head.position.y > tail_y:
                tail_y += 1
            if self.head.position.y < tail_y:
                tail_y -= 1
            self.tail.set_position(tail_x, tail_y)

    def process_moves(self, moves: list[Move]):
        """process the moves file"""
        for direction, distance in moves:
            for _ in range(distance):
                self.move_head(direction)
                self.move_tail()
                print(self)

    @property
    def number_of_tail_positions(self):
        """answer to part 1"""
        return len(set(self.tail.history))

    def __str__(self):
        return f"{self.head} <- {self.tail}"


with open("day9-input.txt") as f:
    moves = [row.replace("\n", "").split() for row in f]
    moves = [Move(m[0], int(m[1])) for m in moves]

rope = Rope()
rope.process_moves(moves)
print(f"{rope.number_of_tail_positions=}")
