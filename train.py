if __name__ == "__main__":
    from Tetris.Trainer import Trainer
    import sys

    if len(sys.argv) > 1:
        trainer = Trainer(sys.argv[1])
    else:
        trainer = Trainer()
    if len(sys.argv) > 2:
        trainer.train(sys.argv[2], 20, 20000, game_duration=500)
    else:
        trainer.train("test", 20, 20000, game_duration=500)

