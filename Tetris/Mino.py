from . import Board, Tile


class Mino:
    def __init__(self) -> None:
        self.tiles: list[Tile] = [Tile.Clear] * (4 * 4)
        self.offset = (0, 0)

    def rotateCW(self, board: Board) -> None:
        raise NotImplementedError()

    def rotateCCW(self, board: Board) -> None:
        raise NotImplementedError()

    def distToGround(self, board: Board) -> int:
        raise NotImplementedError()
