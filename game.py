import time
import pygame
from Players import InputPlayer, Player
from Tetris.WindowRenderer import WindowRenderer, build_screen_and_render_from_height
from Tetris.Game import Game

import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

parse_human = subparsers.add_parser("human", help="Singleplayer human player")

parse_ai = subparsers.add_parser("ai", help="Singleplayer AI player")
parse_ai.add_argument("-p", "--path", help="Path to keras file for AI", type=str)

parse_ai_ai = subparsers.add_parser("ai-ai", help="AI versus AI player")
parse_ai_ai.add_argument(
    "-p",
    "--path",
    help="Path to keras file for both AIs. Overrides --left-path and --right-path",
    type=str,
)
parse_ai_ai.add_argument(
    "-lp", "--left-path", help="Path to keras file for left AI", type=str
)
parse_ai_ai.add_argument(
    "-rp", "--right-path", help="Path to keras file for right AI", type=str
)

parse_human_ai = subparsers.add_parser("human-ai", help="Human versus AI player")
parse_human_ai.add_argument("-p", "--path", help="Path to keras file for AI", type=str)

args = parser.parse_args()


def generate_players() -> list[Player]:
    """ask and generate the players wanted"""
    players = []

    match args.command:
        case "human":
            players.append(InputPlayer())
        case "ai":
            from Players import AIPlayer

            players.append(AIPlayer(args.path))
        case "ai-ai":
            from Players import AIPlayer

            if args.path:
                players.append(AIPlayer(args.path))
                players.append(AIPlayer(args.path))
            else:
                players.append(AIPlayer(args.left_path))
                players.append(AIPlayer(args.right_path))
        case "human-ai":
            from Players import AIPlayer

            players.append(InputPlayer())
            players.append(AIPlayer(args.path))
        case _:
            raise ValueError(f"Option '{args.command}' not valid.")

    return players


def make_game(index: int, player: Player) -> Game:
    """return the game and call setup on player"""
    game = Game()
    first = not index
    player.setup(game, first)
    return game


def run_game(renderer: WindowRenderer, players: list[Player]):
    """run the tetris game until a player loses"""
    games = [make_game(i, x) for i, x in enumerate(players)]
    # breakpoint()

    clock = pygame.time.Clock()
    isRunning = True
    last_time = time.time()
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
        t = time.time()
        print(f"\r{round(1/(t-last_time))}   ", end="")
        last_time = t


players = generate_players()
# pygame setup
pygame.init()
pygame.key.set_repeat(200, 100)

(_, renderer) = build_screen_and_render_from_height(500, len(players))

run_game(renderer, players)


pygame.quit()

