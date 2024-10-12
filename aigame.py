import sys
import re
import time
import pygame
import os

from Tetris.AI import AI
from Tetris.WindowRenderer import build_screen_and_render_from_height
from Tetris.Game import Actions, Game

pygame.init()
(screen, renderer) = build_screen_and_render_from_height(500)
clock = pygame.time.Clock()

game = Game()

isRunning = True
lastTime = time.time()
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    folder = "./models/"
    _, _, f = list(os.walk(folder))[0]

    num = -1
    path = ""
    for file in f:
        m = re.match(r".*_([0-9]+)\.keras", file)
        if m:
            n = int(m.groups()[0])
            if num < n:
                num = n
                path = file
    path = os.path.join(folder, path)

print(path)
ai = AI(path)
game.linesCleared = 300
last_time = time.time()
while isRunning:
    clock.tick(60)

    for event in pygame.event.get():
        # Handles exit
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                raise SystemExit

    if game.ticks % 2 == 0:
        action = ai.get_action(game.board.tiles, game.piece)
    else:
        action = Actions.SoftDrop.value
    game.actionPressed[action] = True
    isRunning = game.gameTick()

    renderer.render(game)
    t = time.time()
    print(f"\r{round(1/(t-last_time))}   ", end="")
    last_time = t

print("Final score:", game.score)
pygame.quit()

