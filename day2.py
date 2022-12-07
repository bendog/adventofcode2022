from dataclasses import dataclass


@dataclass
class Move:
    name: str
    points: int
    defeats: str
    weakness: str


ROCK = Move(name="rock", points=1, defeats="scissors", weakness="paper")
PAPER = Move(name="paper", points=2, defeats="rock", weakness="scissors")
SCISSORS = Move(name="scissors", points=3, defeats="paper", weakness="rock")


class Game:
    victory_points = {
        True: 6,
        None: 3,
        False: 0,
    }

    def __init__(self, opponent: str, response: str | None):
        # opponent
        self.opponent: Move | None = None
        self.set_opponent(opponent)
        # responses
        self.response: Move | None = None
        self.set_response(response)

    def __repr__(self):
        return f"their:{self.opponent} VS our:{self.response}"

    def set_opponent(self, value: str):
        if value == "A":
            self.opponent = ROCK
        elif value == "B":
            self.opponent = PAPER
        elif value == "C":
            self.opponent = SCISSORS

    def set_response(self, value: str):
        if value in {"X", "rock"}:
            self.response = ROCK
        elif value in {"Y", "paper"}:
            self.response = PAPER
        elif value in {"Z", "scissors"}:
            self.response = SCISSORS

    @property
    def victory(self) -> bool | None:
        if not self.opponent or not self.response:
            raise ValueError("Game not ready.")
        if self.opponent.name == self.response.defeats:
            return True
        elif self.opponent.defeats == self.response.name:
            return False
        return None

    @property
    def score(self) -> int:
        return self.response.points + self.victory_points[self.victory]


# import data
with open("day2-input.txt") as f:
    games = [Game(*line.split()) for line in f]

# get total score
print(sum(game.score for game in games))

# PART TWO! that was a curve ball, all that work for nothing!
VICTORY_MATRIX = {
    "X": False,
    "Y": None,
    "Z": True,
}

with open("day2-input.txt") as f:
    data = [line.split() for line in f]
    games = []
    for opponent_move, outcome in data:
        game = Game(opponent_move, "")
        if VICTORY_MATRIX[outcome] is True:
            game.set_response(game.opponent.weakness)
        elif VICTORY_MATRIX[outcome] is False:
            game.set_response(game.opponent.defeats)
        else:
            game.set_response(game.opponent.name)
        games.append(game)

print(sum(game.score for game in games))
