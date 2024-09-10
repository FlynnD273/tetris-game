from enum import Enum
import math
import random

from .Tile import Tile
from .Mino import Mino, Minos
from .Board import Board


class Actions(Enum):
    Right = 0
    Left = 1
    HardDrop = 2
    SoftDrop = 3
    CW = 4
    CCW = 5


class Game:
    """This stores the state of the game (Board, next piece, random piece bag, score, level) and is responsible for advancing the game state."""

    def __init__(self) -> None:
        self.board: Board = Board()
        self.bag: list[Mino] = []
        self.piece: Mino = self._pickPiece()
        self.linesCleared: int = 0
        self.ticks: int = 0
        self.lastSoftDrop: int = 0
        self.actionsStart: list[int] = [0] * len(Actions)
        self.actionPressed: list[bool] = [False] * len(Actions)
        self.isRunning: bool = True

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
        self.actionPressed[Actions.CW.value] = True

    def rotateCCW(self) -> None:
        self.actionPressed[Actions.CCW.value] = True

    def shiftLeft(self) -> None:
        self.actionPressed[Actions.Left.value] = True

    def shiftRight(self) -> None:
        self.actionPressed[Actions.Right.value] = True

    def softDrop(self) -> None:
        self.actionPressed[Actions.SoftDrop.value] = True

    def hardDrop(self) -> None:
        self.actionPressed[Actions.HardDrop.value] = True

    def gameTick(self) -> bool:
        if not self.isRunning:
            return False
        self.linesCleared += self.board.clearLines()
        if self.actionPressed[Actions.HardDrop.value]:
            offRow, offCol = self.piece.offset
            self.piece.offset = (offRow + self.piece.distToGround(self.board), offCol)
            self._lockPiece()
        elif self.actionPressed[Actions.SoftDrop.value]:
            if self.ticks - self.lastSoftDrop >= 2:
                self.lastSoftDrop = self.ticks
                offRow, offCol = self.piece.offset
                self.piece.offset = (offRow + 1, offCol)
                if self.piece.distToGround(self.board) == -1:
                    self.piece.offset = (offRow, offCol)
        elif self.actionPressed[Actions.Right.value]:
            offRow, offCol = self.piece.offset
            self.piece.offset = (offRow, offCol + 1)
            if self.piece.distToGround(self.board) == -1:
                self.piece.offset = (offRow, offCol)
        elif self.actionPressed[Actions.Left.value]:
            offRow, offCol = self.piece.offset
            self.piece.offset = (offRow, offCol - 1)
            if self.piece.distToGround(self.board) == -1:
                self.piece.offset = (offRow, offCol)
        elif self.actionPressed[Actions.CW.value]:
            self.piece.rotateCW(self.board)
        elif self.actionPressed[Actions.CCW.value]:
            self.piece.rotateCCW(self.board)

        for i in range(len(self.actionPressed)):
            self.actionPressed[i] = False

        if self.ticks % self.gravity == 0:
            if self.piece.distToGround(self.board) == 0:
                self._lockPiece()
            else:
                offRow, offCol = self.piece.offset
                self.piece.offset = (offRow + 1, offCol)
                self.lastSoftDrop = self.ticks
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
        if self.piece.distToGround(self.board) == -1:
            self.isRunning = False
