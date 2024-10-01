import random
import time
import pygame

from Tetris.WindowRenderer import build_screen_and_render_from_height
from Tetris.Game import Game

from Input import (
    InputHandler,
    OnPressRequireResetHook,
    OnPressRepeatingHook,
    OnPressRepeatDelayedHook,
)


pygame.init()
(screen, renderer) = build_screen_and_render_from_height(500, 2)
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 100)

input_handler = InputHandler()

game1 = Game()
game2 = Game()

input_handler.add_hook(OnPressRepeatDelayedHook(pygame.K_d, game1.shiftRight, 15))
input_handler.add_hook(OnPressRepeatDelayedHook(pygame.K_a, game1.shiftLeft, 15))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_w, game1.hardDrop))
input_handler.add_hook(OnPressRepeatingHook(pygame.K_s, game1.softDrop))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_q, game1.rotateCCW))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_e, game1.rotateCW))

input_handler.add_hook(OnPressRepeatDelayedHook(pygame.K_l, game2.shiftRight, 15))
input_handler.add_hook(OnPressRepeatDelayedHook(pygame.K_j, game2.shiftLeft, 15))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_i, game2.hardDrop))
input_handler.add_hook(OnPressRepeatingHook(pygame.K_k, game2.softDrop))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_u, game2.rotateCCW))
input_handler.add_hook(OnPressRequireResetHook(pygame.K_o, game2.rotateCW))

isRunning = True
lastTime = time.time()
while isRunning:
    clock.tick(60)

    for event in pygame.event.get():
        # Handles exit
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                raise SystemExit

    input_handler.update(pygame.key.get_pressed())

    isRunning = game1.gameTick() and game2.gameTick()

    renderer.clear_screen()
    renderer.render_all([game1, game2])
    pygame.display.flip()

pygame.quit()
