import random
import time
import pygame

from Tetris.ConsoleRenderer import ConsoleRenderer
from Tetris.Game import Game
from Tetris.Mino import JMino, LMino, Mino, Minos, TMino, OMino, SMino, ZMino

renderer = ConsoleRenderer()
game = Game()

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 100)

isRunning = True
lastTime = time.time()
while isRunning:
    clock.tick(60)
    keys = []
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys.append(event.key)
    if pygame.K_RIGHT in keys:
        game.shiftRight()
    elif pygame.K_LEFT in keys:
        game.shiftLeft()
    elif pygame.K_UP in keys:
        game.hardDrop()
    elif pygame.K_z in keys:
        game.rotateCCW()
    elif pygame.K_x in keys:
        game.rotateCW()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        game.softDrop()

    isRunning = game.gameTick()
    renderer.render(game)

pygame.quit()


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
