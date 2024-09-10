from . import Game


class RendererBase:
    def render(self, game: Game) -> None:
        raise NotImplementedError()
