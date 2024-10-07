from Input import (
    InputHandler,
    OnPressRequireResetHook,
    OnPressRepeatingHook,
    OnPressRepeatDelayedHook,
)
from Tetris.Game import Game
from Tetris.AI import AI
import pygame

WASD = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e]
IJKL = [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_u, pygame.K_o]


class Player:
    """A base player to play the game"""

    def setup(game: Game, first: bool) -> None:
        """setup the player with the game"""
        raise NotImplementedError()

    def update() -> None:
        """allow the player to provide game input"""
        raise NotImplementedError()


class InputPlayer(Player):
    """A player that accepts keyboard input of either wasd or ijkl depending on being first"""

    input_handler = None

    def setup(self, game: Game, first: bool) -> None:
        input_method = WASD if first else IJKL

        self.input_handler = InputHandler()
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


def make_AI() -> AI:
    """ask about the AI file that should be used"""
    # breakpoint()
    question = "What keras file should be used: "
    while 1:
        file_name = ""
        try:
            file_name = input(question)
            if not file_name.endswith(".keras"):
                file_name += ".keras"
            return AI(file_name)
        except Exception as err:
            print(err)
            pass
        finally:
            question = f"{file_name} could not be found or was not valid: "


class AIPlayer(Player):

    def __init__(self):
        self.ai = make_AI()

    def setup(self, game: Game, _first: bool) -> None:
        self.game = game

    def update(self) -> None:
        action = self.ai.get_action(self.game.board.tiles, self.game.piece)
        self.game.actionPressed[action] = True
