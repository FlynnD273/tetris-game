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
        """Clear all full lines and return the number of lines cleared."""
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
            while offset < len(rowsToClear) and rowsToClear[offset] == row - offset:
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
        """Get the tile at the specified row and column."""
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return Tile.LBlue
        return self.tiles[row * self.width + col]

    def setTile(self, row: int, col: int, tile: Tile) -> None:
        """Set the tile at the specified row and column."""
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return
        self.tiles[row * self.width + col] = tile

    def fillRandom(self, density: float = 0.5) -> None:
        """Generates a random board, used only for testing the renderers."""
        for i in range(len(self.tiles)):
            if random.random() < density:
                self.tiles[i] = Tiles[random.randint(0, len(Tiles) - 1)]
            else:
                self.tiles[i] = Tile.Clear

    def copy(self) -> "Board":
        """Create a copy of the Board instance."""
        b = Board()
        b.tiles = self.tiles.copy()
        return b

    def __eq__(self, value: object, /) -> bool:
        """Element-wise equality check."""
        if not isinstance(value, Board):
            return False

        for a, b in zip(self.tiles, value.tiles):
            if a != b:
                return False
        return True
