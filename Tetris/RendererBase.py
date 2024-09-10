from .Game import Game
from .Mino import Mino


class RendererBase:
    def render(self, game: Game) -> None:
        raise NotImplementedError()

    def renderMino(self, mino: Mino) -> None:
        raise NotImplementedError()
