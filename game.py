import random
import time
import pygame

from Tetris.ConsoleRenderer import ConsoleRenderer
from Tetris.Game import Game
from Tetris.Mino import JMino, LMino, Mino, Minos, TMino, OMino, SMino, ZMino

renderer = ConsoleRenderer()
game = Game()

pygame.init()
clock = pygame.time.Clock()

hasLost = False
lastTime = time.time()
while not hasLost:
    clock.tick(60)
    choice = random.randint(1, 50)
    match choice:
        case 1:
            game.rotateCW()
        case 2:
            game.rotateCCW()
        case 3:
            game.hardDrop()
        case 4:
            game.shiftLeft()
        case 5:
            game.shiftRight()
        case 6:
            game.softDrop()
    hasLost = not game.gameTick()
    renderer.render(game)


def demoMino(mino: Mino) -> None:
    print("-" * 5)
    renderer.renderMino(mino)
    mino.rotateCW(game.board)
    print("-" * 5)
    renderer.renderMino(mino)
    mino.rotateCW(game.board)
    print("-" * 5)
    renderer.renderMino(mino)
    mino.rotateCW(game.board)
    print("-" * 5)
    renderer.renderMino(mino)


# for m in Minos:
#     demoMino(m)
