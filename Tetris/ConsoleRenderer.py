from .RendererBase import RendererBase
from .Game import Game
from .Tile import Tile
from colorist import BgColor, BgBrightColor


class ConsoleRenderer(RendererBase):
    def render(self, game: Game) -> None:
        for row in range(game.board.height):
            for col in range(game.board.width):
                color = BgColor.DEFAULT
                match game.board.getTile(row, col):
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

                print(f"{color}  {BgColor.DEFAULT}", end="")
            print()
