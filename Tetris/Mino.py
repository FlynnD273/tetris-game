from .Tile import Tile
from .Board import Board


class Mino:
    def __init__(self) -> None:
        self.offset: tuple[int, int] = (0, 0)
        self.startOffset: tuple[int, int] = (0, 0)
        self.color: Tile = Tile.Clear
        self.rotations: list[list[int]] = [[0] * (4 * 4)] * 4
        self.rotation: int = 0
        self.wallkicks: dict[tuple[int, int], list[tuple[int, int]]] = {
            (0, 1): [(0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)],
            (1, 2): [(0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)],
            (2, 3): [(0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)],
            (3, 0): [(0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)],
        }
        items = list(self.wallkicks.items())
        for key, value in items:
            a, b = key
            self.wallkicks[(b, a)] = [(-x, -y) for x, y in [offset for offset in value]]

    @property
    def width(self) -> int:
        return 4

    @property
    def height(self) -> int:
        return 4

    @property
    def currTiles(self) -> list[int]:
        return self.rotations[self.rotation]

    def rotateCW(self, board: Board) -> None:
        prevRotation = self.rotation
        prevOffset = self.offset
        self.rotation += 1
        self.rotation = self.rotation % 4
        self.tryRotation(board, prevRotation, prevOffset)

    def rotateCCW(self, board: Board) -> None:
        prevRotation = self.rotation
        prevOffset = self.offset
        self.rotation += 3  # Needed because modulo doesn't like negative numbers
        self.rotation = self.rotation % 4
        self.tryRotation(board, prevRotation, prevOffset)

    def tryRotation(
        self, board: Board, prevRotation: int, prevOffset: tuple[int, int]
    ) -> None:
        isValid = False
        for kick in self.wallkicks[(prevRotation, self.rotation)]:
            kickRow, kickCol = kick
            offRow, offCol = prevOffset
            self.offset = (kickRow + offRow, kickCol + offCol)
            if self.distToGround(board) >= 0:
                isValid = True
                break
        if not isValid:
            self.offset = prevOffset
            self.rotation = prevRotation

    def distToGround(self, board: Board) -> int:
        """Returns -1 if intersecting with the board, 0 if on the ground, and the number of empty tiles between the mino and the ground otherwise."""
        offRow, offCol = self.offset
        lowestPoints: list[int] = [-1] * 4
        for row in range(self.height - 1, -1, -1):
            for col in range(self.width):
                if self.getTile(row, col) != Tile.Clear:
                    if (
                        not row + offRow < 0
                        and board.getTile(row + offRow, col + offCol) != Tile.Clear
                    ):
                        return -1
                    if lowestPoints[col] == -1:
                        lowestPoints[col] = row

        dist = 0
        while offRow + dist <= board.height:
            for col in range(self.width):
                if lowestPoints[col] == -1:
                    continue
                checkRow = offRow + dist + lowestPoints[col] + 1
                if board.getTile(checkRow, col + offCol) != Tile.Clear:
                    return dist
            dist += 1

        return dist

    def getTile(self, row: int, col: int) -> Tile:
        """Get the tile at the specified row and column."""
        return self.color if self.currTiles[row * self.width + col] else Tile.Clear

    def getTileWithOffset(self, row: int, col: int) -> Tile:
        """Get the tile at the specified row and column."""
        offRow, offCol = self.offset
        if (
            row < offRow
            or row >= offRow + self.height
            or col < offCol
            or col >= offCol + self.width
        ):
            return Tile.Clear
        return (
            self.color
            if self.currTiles[(row - offRow) * self.width + (col - offCol)]
            else Tile.Clear
        )

    def copy(self) -> "Mino":
        m = Mino()
        m.rotations = self.rotations.copy()
        m.offset = self.offset
        m.startOffset = self.startOffset
        m.rotation = self.rotation
        m.color = self.color
        return m


class TMino(Mino):
    def __init__(self) -> None:
        super().__init__()
        # fmt: off
        self.rotations: list[list[int]] = [
                [0, 0, 0, 0,
                 1, 1, 1, 0,
                 0, 1, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 1, 1, 0, 0, 
                 0, 1, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 1, 1, 1, 0, 
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 0, 1, 1, 0, 
                 0, 1, 0, 0,
                 0, 0, 0, 0,],
                ]
        # fmt: on
        self.color = Tile.Magenta
        self.offset = (-1, 3)
        self.startOffset = self.offset


class JMino(Mino):
    def __init__(self) -> None:
        super().__init__()
        # fmt: off
        self.rotations: list[list[int]] = [
                [0, 0, 0, 0,
                 1, 1, 1, 0,
                 0, 0, 1, 0,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 0, 1, 0, 0, 
                 1, 1, 0, 0,
                 0, 0, 0, 0,],
                [1, 0, 0, 0,
                 1, 1, 1, 0, 
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 1, 0,
                 0, 1, 0, 0, 
                 0, 1, 0, 0,
                 0, 0, 0, 0,],
                ]
        # fmt: on
        self.color = Tile.Orange
        self.offset = (-1, 3)
        self.startOffset = self.offset


class LMino(Mino):
    def __init__(self) -> None:
        super().__init__()
        # fmt: off
        self.rotations: list[list[int]] = [
                [0, 0, 0, 0,
                 1, 1, 1, 0,
                 1, 0, 0, 0,
                 0, 0, 0, 0,],
                [1, 1, 0, 0,
                 0, 1, 0, 0, 
                 0, 1, 0, 0,
                 0, 0, 0, 0,],
                [0, 0, 1, 0,
                 1, 1, 1, 0, 
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 0, 1, 0, 0, 
                 0, 1, 1, 0,
                 0, 0, 0, 0,],
                ]
        # fmt: on
        self.color = Tile.DBlue
        self.offset = (-1, 3)
        self.startOffset = self.offset


class OMino(Mino):
    def __init__(self) -> None:
        super().__init__()
        # fmt: off
        self.rotations: list[list[int]] = [
                [0, 1, 1, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 1, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 1, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 1, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                ]
        # fmt: on
        self.color = Tile.Yellow
        self.offset = (0, 3)
        self.startOffset = self.offset


class SMino(Mino):
    def __init__(self) -> None:
        super().__init__()
        # fmt: off
        self.rotations: list[list[int]] = [
                [0, 0, 0, 0,
                 0, 1, 1, 0,
                 1, 1, 0, 0,
                 0, 0, 0, 0,],
                [1, 0, 0, 0,
                 1, 1, 0, 0,
                 0, 1, 0, 0,
                 0, 0, 0, 0,],
                [0, 0, 1, 1,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 0, 1, 1, 0,
                 0, 0, 1, 0,
                 0, 0, 0, 0,],
                ]
        # fmt: on
        self.color = Tile.Green
        self.offset = (-1, 3)
        self.startOffset = self.offset


class ZMino(Mino):
    def __init__(self) -> None:
        super().__init__()
        # fmt: off
        self.rotations: list[list[int]] = [
                [0, 0, 0, 0,
                 1, 1, 0, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 1, 1, 0, 0,
                 1, 0, 0, 0,
                 0, 0, 0, 0,],
                [1, 1, 0, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 0, 1, 0, 
                 0, 1, 1, 0, 
                 0, 1, 0, 0, 
                 0, 0, 0, 0,],
                ]
        # fmt: on
        self.color = Tile.Red
        self.offset = (-1, 3)
        self.startOffset = self.offset


class IMino(Mino):
    def __init__(self) -> None:
        super().__init__()
        # fmt: off
        self.rotations: list[list[int]] = [
                [0, 0, 0, 0,
                 0, 0, 0, 0,
                 1, 1, 1, 1,
                 0, 0, 0, 0,],
                [0, 1, 0, 0,
                 0, 1, 0, 0,
                 0, 1, 0, 0,
                 0, 1, 0, 0,],
                [0, 0, 0, 0,
                 1, 1, 1, 1,
                 0, 0, 0, 0,
                 0, 0, 0, 0,],
                [0, 0, 1, 0,
                 0, 0, 1, 0,
                 0, 0, 1, 0,
                 0, 0, 1, 0,],
                ]
        # fmt: on
        self.color = Tile.LBlue
        self.offset = (-2, 3)
        self.startOffset = self.offset


Minos = [IMino(), JMino(), LMino(), OMino(), SMino(), TMino(), ZMino()]
