from Tetris import Game, ConsoleRenderer
import random

renderer = ConsoleRenderer()
game = Game()

game.board.fillRandom(0.9)
renderer.render(game)
print(game.board.clearLines())
renderer.render(game)
