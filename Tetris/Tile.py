from enum import Enum


class Tile(Enum):
    """The color of a mino tile."""

    LBlue = 0
    DBlue = 1
    Orange = 2
    Yellow = 3
    Green = 4
    Red = 5
    Magenta = 6
    Clear = 7


Tiles = [
    Tile.LBlue,
    Tile.DBlue,
    Tile.Orange,
    Tile.Yellow,
    Tile.Green,
    Tile.Red,
    Tile.Magenta,
    Tile.Clear,
]
