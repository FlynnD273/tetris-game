import random
import time
import pygame

from Tetris.AI import AI
from Tetris.WindowRenderer import build_screen_and_render_from_height
from Tetris.Game import Game

pygame.init()
(screen, renderer) = build_screen_and_render_from_height(500)
clock = pygame.time.Clock()

game = Game()

isRunning = True
lastTime = time.time()
ai = AI()
ai.model.load_weights("./models/test.keras")
game.linesCleared = 200
while isRunning:
    clock.tick(60)

    for event in pygame.event.get():
        # Handles exit
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                raise SystemExit

    action = ai.get_action(game.board.tiles, game.piece)
    game.actionPressed[action] = True
    isRunning = game.gameTick()

    renderer.render(game)

pygame.quit()
