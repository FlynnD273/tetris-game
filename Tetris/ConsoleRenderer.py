from .RendererBase import RendererBase
from .Game import Game
from .Tile import Tile
from colorist import BgColor, BgBrightColor


class ConsoleRenderer(RendererBase):
    """Render the game state to the console using ANSI escape codes."""

    def render(self, game: Game) -> None:
        """Render the game to the console."""
        output = ""
        output += f"{BgColor.DEFAULT}┏{'━'*game.board.width*2}┓\n"
        ghost = game.piece.copy()
        offRow, offCol = ghost.offset
        ghost.offset = (offRow + game.piece.distToGround(game.board), offCol)
        for row in range(game.board.height):
            prevColor = BgColor.DEFAULT
            output += "┃"
            for col in range(game.board.width):
                tile = game.piece.getTileWithOffset(row, col)
                if tile == Tile.Clear:
                    tile = ghost.getTileWithOffset(row, col)
                    if tile == Tile.Clear:
                        tile = game.board.getTile(row, col)
                    else:
                        prevColor = BgColor.DEFAULT
                        output += BgColor.DEFAULT + "🮮🮮"
                        continue
                offRow, offCol = game.piece.offset
                color = self.getColor(tile)
                if prevColor != color:
                    output += f"{color}  "
                else:
                    output += "  "
                prevColor = color
            output += BgColor.DEFAULT + "┃\n"
        output += f"┗{'━'*game.board.width*2}┛\n"
        output += "┏" + "━" * 8 + "┳" + "━" * 11 + "┓\n"
        for row in range(4):
            output += "┃"
            for col in range(4):
                tile = game.nextPiece.getTile(row, col)
                color = self.getColor(tile)
                output += f"{color}  {BgColor.DEFAULT}"
            output += "┃"
            match row:
                case 0:
                    output += "SCORE" + " " * 6 + "┃\n"
                case 1:
                    output += f"{game.score:06}" + " " * 5 + "┃\n"
                case 2:
                    output += "LEVEL" + " " * 6 + "┃\n"
                case 3:
                    output += f"{game.level:02}" + " " * 9 + "┃\n"
                case _:
                    output += "\n"

        output += "┗" + "━" * 8 + "┻" + "━" * 11 + "┛\n"

        print(output)

    def getColor(self, tile: Tile) -> str:
        """Map a Tile color to the ANSI escape code."""
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
