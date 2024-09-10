from . import Board


class Game:
    """This stores the state of the game (Board, next piece, random piece bag, score, level) and is responsible for advancing the game state."""

    def __init__(self) -> None:
        self.board = Board()
