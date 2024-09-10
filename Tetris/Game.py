import math
import random

from .Tile import Tile
from .Mino import Mino, Minos
from .Board import Board


class Game:
    """This stores the state of the game (Board, next piece, random piece bag, score, level) and is responsible for advancing the game state."""

    def __init__(self) -> None:
        self.board: Board = Board()
        self.bag: list[Mino] = []
        self.piece: Mino = self._pickPiece()
        self.linesCleared: int = 0
        self.ticks: int = 0
        self.lastSoftDrop: int = 0

    @property
    def level(self) -> int:
        return math.floor(self.linesCleared / 10)

    @property
    def gravity(self) -> int:
        gravities: list[int] = [
            48,
            43,
            38,
            33,
            28,
            23,
            18,
            13,
            8,
            6,
            5,
            5,
            5,
            4,
            4,
            4,
            3,
            3,
            3,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            1,
        ]
        if self.level >= len(gravities):
            return 1
        return gravities[self.level]

    def _pickPiece(self) -> Mino:
        if not self.bag:
            self.bag = Minos.copy()

        index = random.randint(0, len(self.bag) - 1)
        mino = self.bag[index].copy()
        mino.offset = mino.startOffset

        del self.bag[index]

        return mino

    def rotateCW(self) -> None:
        self.piece.rotateCW(self.board)

    def rotateCCW(self) -> None:
        self.piece.rotateCCW(self.board)

    def shiftLeft(self) -> None:
        offRow, offCol = self.piece.offset
        self.piece.offset = (offRow, offCol - 1)
        if self.piece.distToGround(self.board) == -1:
            self.piece.offset = (offRow, offCol)

    def shiftRight(self) -> None:
        offRow, offCol = self.piece.offset
        self.piece.offset = (offRow, offCol + 1)
        if self.piece.distToGround(self.board) == -1:
            self.piece.offset = (offRow, offCol)

    def softDrop(self) -> None:
        if self.ticks - self.lastSoftDrop < 2:
            return
        self.lastSoftDrop = self.ticks
        offRow, offCol = self.piece.offset
        self.piece.offset = (offRow + 1, offCol)
        if self.piece.distToGround(self.board) == -1:
            self.piece.offset = (offRow, offCol)

    def hardDrop(self) -> None:
        offRow, offCol = self.piece.offset
        self.piece.offset = (offRow + self.piece.distToGround(self.board), offCol)
        self._lockPiece()

    def gameTick(self) -> bool:
        if self.ticks % self.gravity == 0:
            if self.piece.distToGround(self.board) == 0:
                self._lockPiece()
                if self.piece.distToGround(self.board) == -1:
                    return False
            else:
                offRow, offCol = self.piece.offset
                self.piece.offset = (offRow + 1, offCol)
                self.lastSoftDrop = self.ticks
        self.linesCleared += self.board.clearLines()
        self.ticks += 1
        return True

    def _lockPiece(self) -> None:
        for row in range(self.piece.height):
            for col in range(self.piece.width):
                tile = self.piece.getTile(row, col)
                if tile != Tile.Clear:
                    offRow, offCol = self.piece.offset
                    self.board.setTile(row + offRow, col + offCol, tile)

        self.piece = self._pickPiece()
