from .Game import Game
from .Mino import Mino


class RendererBase:
    """Base renderer class to support multiple output modes."""
    def render(self, game: Game) -> None:
        """Render the current game state."""
        raise NotImplementedError()
