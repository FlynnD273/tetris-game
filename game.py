import random
import time
import pygame
from Tetris.RendererBase import *
from Tetris.Tile import Tile

from Tetris.WindowRenderer import build_screen_and_render_from_height
from Tetris.Game import Game
from Players import *


def pick_game_option() -> int:
    """ask about the game type"""
    print(
        """
        Pick a game type:
        1. Human Only
        2. AI only
        3. Two Humans
        4. Two AIs
        5. Human and AI
        """
    )
    question = "What is your choice: "
    while 1:
        try:
            game_type = int(input(question))
            if 1 <= game_type <= 5:
                return game_type
        except Exception:
            pass
        finally:
            question = "\nThat was not an option: "


def generate_players() -> list[Player]:
    """ask and generate the players wanted"""
    game_type = pick_game_option()
    players = []

    # first player
    if game_type % 2 == 0:
        players.append(AIPlayer())
    else:
        players.append(InputPlayer())

    # second player (if wanted)
    if game_type == 3:
        players.append(InputPlayer())
    elif game_type > 3:
        players.append(AIPlayer())

    return players


def make_game(index: int, player: Player) -> Game:
    """return the game and call setup on player"""
    game = Game()
    first = not index
    player.setup(game, first)
    return game


def run_game(renderer: RendererBase, players: list[Player]):
    """run the tetris game until a player loses"""
    games = [make_game(i, x) for i, x in enumerate(players)]
    # breakpoint()

    clock = pygame.time.Clock()
    isRunning = True
    while isRunning:
        clock.tick(60)

        for event in pygame.event.get():
            # Handles exit
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

        for player in players:
            player.update()

        isRunning = all(map(lambda game: game.gameTick(), games))

        renderer.clear_screen()
        renderer.render_all(games)
        pygame.display.flip()


players = generate_players()
# pygame setup
pygame.init()
pygame.key.set_repeat(200, 100)

(_, renderer) = build_screen_and_render_from_height(500, 2)

run_game(renderer, players)


pygame.quit()
