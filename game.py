import random
import time
import pygame

# from Tetris.ConsoleRenderer import ConsoleRenderer
from Tetris.WindowRenderer import WindowRenderer, build_screen_and_render_from_height
from Tetris.Game import Game
from Tetris.Mino import JMino, LMino, Mino, Minos, TMino, OMino, SMino, ZMino

from Input import InputHandler, OnPressRequireResetHook, OnPressRepeatingHook, OnPressRepeatDelayedHook



pygame.init()
(screen, renderer) = build_screen_and_render_from_height(500)
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 100)

input_handler = InputHandler()

game = Game()

input_handler.add_hook(OnPressRepeatDelayedHook(pygame.K_RIGHT, game.shiftRight, 30)) # 30 cycles before repeat kicks in
input_handler.add_hook(OnPressRepeatDelayedHook(pygame.K_LEFT, game.shiftLeft, 30)) # 30 cycles before repeat kicks in
input_handler.add_hook(OnPressRequireResetHook(pygame.K_UP, game.hardDrop))
input_handler.add_hook(OnPressRepeatingHook(pygame.K_DOWN, game.softDrop))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_z, game.rotateCCW))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_x, game.rotateCW))

isRunning = True
lastTime = time.time()
while isRunning:
    clock.tick(60)
        
    for event in pygame.event.get():
        # Handles exit
        if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
    
    input_handler.update(pygame.key.get_pressed())

    isRunning = game.gameTick()

    renderer.render(game)

pygame.quit()
