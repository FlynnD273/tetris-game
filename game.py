import random
import time
import pygame

# from Tetris.ConsoleRenderer import ConsoleRenderer
from Tetris.WindowRenderer import WindowRenderer, build_screen_and_render_from_width
from Tetris.Game import Game
from Tetris.Mino import JMino, LMino, Mino, Minos, TMino, OMino, SMino, ZMino


pygame.init()
(screen, renderer) = build_screen_and_render_from_width(800)
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 100)

game = Game()

isRunning = True
lastTime = time.time()
while isRunning:
    clock.tick(60)
    keys = []
        
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys.append(event.key)
        # Handles exit
        if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

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
