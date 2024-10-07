from Tetris.Trainer import Trainer
import sys

if len(sys.argv) > 1:
    trainer = Trainer(sys.argv[1])
else:
    trainer = Trainer()
trainer.train("test", 20, 20000, game_duration=500)

