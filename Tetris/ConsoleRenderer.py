from .RendererBase import RendererBase
from .Game import Game
from .Tile import Tile
from .Mino import Mino
from colorist import BgColor, BgBrightColor


class ConsoleRenderer(RendererBase):
    """Render the game state to the console using ANSI escape codes."""

    def render(self, game: Game) -> None:
        """Render the game to the console."""
        print(f"┏{'━'*game.board.width*2}┓")
        for row in range(game.board.height):
            print("┃", end="")
            for col in range(game.board.width):
                tile = game.piece.getTileWithOffset(row, col)
                if tile == Tile.Clear:
                    tile = game.board.getTile(row, col)
                color = self.getColor(tile)
                print(f"{color}  {BgColor.DEFAULT}", end="")
            print("┃")
        print(f"┗{'━'*game.board.width*2}┛")

    def renderMino(self, mino: Mino) -> None:
        for row in range(4):
            for col in range(4):
                color = self.getColor(mino.getTile(row, col))
                print(f"{color}  {BgColor.DEFAULT}", end="")
            print()

    def getColor(self, tile: Tile) -> str:
        color = BgColor.DEFAULT
        match tile:
            case Tile.LBlue:
                color = BgColor.CYAN
            case Tile.DBlue:
                color = BgColor.BLUE
            case Tile.Orange:
                color = BgColor.YELLOW
            case Tile.Yellow:
                color = BgBrightColor.YELLOW
            case Tile.Green:
                color = BgColor.GREEN
            case Tile.Red:
                color = BgColor.RED
            case Tile.Magenta:
                color = BgColor.MAGENTA

        return color
