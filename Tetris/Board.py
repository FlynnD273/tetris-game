from .Tile import Tile, Tiles
import random


class Board:
    """The game board. The only keeps track of static tiles, and is responsible for clearing lines."""

    def __init__(self) -> None:
        self.tiles: list[Tile] = [Tile.Clear] * (self.width * self.height)

    @property
    def width(self) -> int:
        """The width of the board."""
        return 10

    @property
    def height(self) -> int:
        """The height of the board."""
        return 20

    def clearLines(self) -> int:
        rowsToClear: list[int] = []
        for row in range(self.height - 1, -1, -1):
            isClear = True
            for col in range(self.width):
                if self.getTile(row, col) == Tile.Clear:
                    isClear = False
                    break
            if isClear:
                rowsToClear.append(row)

        offset = 0
        row = self.height - 1
        while row - offset >= 0:
            if offset < len(rowsToClear) and rowsToClear[offset] == row:
                offset += 1
            if offset > 0:
                for col in range(self.width):
                    self.setTile(row, col, self.getTile(row - offset, col))
            row -= 1

        while offset > 0:
            for col in range(self.width):
                self.setTile(offset - 1, col, Tile.Clear)
            offset -= 1

        return len(rowsToClear)

    def getTile(self, row: int, col: int) -> Tile:
        return self.tiles[row * self.width + col]

    def setTile(self, row: int, col: int, tile: Tile) -> None:
        self.tiles[row * self.width + col] = tile

    def fillRandom(self, density: float = 0.5) -> None:
        """Generates a random board, used only for testing the renderers."""
        for i in range(len(self.tiles)):
            if random.random() < density:
                self.tiles[i] = Tiles[random.randint(0, len(Tiles) - 1)]
            else:
                self.tiles[i] = Tile.Clear
