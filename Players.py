from Input import (
    InputHandler,
    OnPressRequireResetHook,
    OnPressRepeatingHook,
    OnPressRepeatDelayedHook,
)
from Tetris.Game import Game
import pygame

WASD = [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_DOWN,
    pygame.K_RIGHT,
    pygame.K_z,
    pygame.K_x,
]


class Player:
    """A base player to play the game"""

    def setup(self, game: Game, first: bool) -> None:
        """setup the player with the game"""
        raise NotImplementedError()

    def update(self) -> None:
        """allow the player to provide game input"""
        raise NotImplementedError()


class InputPlayer(Player):
    """A player that accepts keyboard input of either wasd or ijkl depending on being first"""

    def __init__(self) -> None:
        self.input_handler = InputHandler()

    def setup(self, game: Game, first: bool) -> None:
        input_method = WASD

        self.input_handler.add_hook(
            OnPressRepeatDelayedHook(input_method[1], game.shiftLeft, 15)
        )
        self.input_handler.add_hook(
            OnPressRepeatDelayedHook(input_method[3], game.shiftRight, 15)
        )
        self.input_handler.add_hook(
            OnPressRequireResetHook(input_method[0], game.hardDrop)
        )
        self.input_handler.add_hook(
            OnPressRepeatingHook(input_method[2], game.softDrop)
        )
        self.input_handler.add_hook(
            OnPressRequireResetHook(input_method[4], game.rotateCCW)
        )
        self.input_handler.add_hook(
            OnPressRequireResetHook(input_method[5], game.rotateCW)
        )

    def update(self) -> None:
        self.input_handler.update(pygame.key.get_pressed())


class AIPlayer(Player):

    def __init__(self, filepath: str):
        if not filepath:
            raise IOError("File path must be specifiec")
        from Tetris.AI import AI

        self.ai = AI(filepath)

    def setup(self, game: Game, first: bool) -> None:
        self.game = game

    def update(self) -> None:
        action = self.ai.get_action(self.game.board.tiles, self.game.piece)
        self.game.actionPressed[action] = True

