from tensorflow.python.ops.gen_math_ops import cumulative_logsumexp
from .Tile import Tile
from .Game import Game
from .AI import AI

import os
import pygad.kerasga
import pygad


##from pygad
class Trainer:
    """The Trainer for the AI"""

    def __init__(self, file: str | None = None) -> None:
        if file:
            self.ai = AI(file)
        else:
            self.ai = AI()
        self.generations = 0

    def _run_tetris(self, _ga, solution, _sol_idx):
        """run the tetris game"""
        model_weights_matrix = pygad.kerasga.model_weights_as_matrix(
            model=self.ai.model, weights_vector=solution
        )

        self.ai.model.set_weights(weights=model_weights_matrix)

        game = Game()
        game.linesCleared = 300
        cumulative_height = 0
        while game.isRunning and game.ticks < self.game_duration:
            action = self.ai.get_action(game.board.tiles, game.piece)
            game.actionPressed[action] = True
            game.gameTick()
            max_height = -1
            for row in range(game.board.height):
                for col in range(game.board.width):
                    if game.board.getTile(row, col) != Tile.Clear:
                        max_height = row
                        break
                if max_height != -1:
                    break
            if max_height == -1:
                max_height = 0
            cumulative_height = game.board.height - max_height

        holes = 0
        for row in range(game.board.height):
            blocks = 0
            for col in range(game.board.width):
                if game.board.getTile(row, col) != Tile.Clear:
                    blocks += 1

            if blocks > 0:
                holes += game.board.width - blocks

        return (
            game.ticks
            + 100 * game.score
            + cumulative_height / 10
            + game.pieces_placed * 10
            - holes * 100
        )

    def _callback(self, ga: pygad.pygad.GA):
        """print generation data"""
        print(f"Generation = {ga.generations_completed}/{self.generations}")
        solution = ga.best_solution()
        print(f"Best Steps = {solution[1]}")

        best_solution_weights = pygad.kerasga.model_weights_as_matrix(
            model=self.ai.model, weights_vector=solution[0]
        )
        self.ai.model.set_weights(best_solution_weights)
        self.ai.model.save(
            os.path.join("models", f"{self.file_name}_{ga.generations_completed}.keras")
        )

    def train(
        self,
        file_name,
        num_solutions=20,
        num_generations=25,
        num_parents_mating=5,
        game_duration=1000,
    ):
        """run the genetic algorithm and save results to file_name"""
        self.generations = num_generations
        self.file_name = file_name
        self.game_duration = game_duration
        if not os.path.exists("models"):
            os.mkdir("models")

        # Create an instance of the pygad.kerasga.KerasGA class to build the initial population.
        keras_ga = pygad.kerasga.KerasGA(
            model=self.ai.model, num_solutions=num_solutions
        )
        initial_population = keras_ga.population_weights

        # Create an instance of the pygad.GA class
        ga_instance = pygad.GA(
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            initial_population=initial_population,
            fitness_func=self._run_tetris,
            on_generation=self._callback,
        )

        # Start the genetic algorithm evolution.
        ga_instance.run()

        # Returning the details of the best solution.
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        print(
            "Fitness value of the best solution = {solution_fitness}".format(
                solution_fitness=solution_fitness
            )
        )
        print(
            "Index of the best solution : {solution_idx}".format(
                solution_idx=solution_idx
            )
        )

        # Fetch the parameters of the best solution.
        best_solution_weights = pygad.kerasga.model_weights_as_matrix(
            model=self.ai.model, weights_vector=solution
        )
        self.ai.model.set_weights(best_solution_weights)
        self.ai.model.save(os.path.join("models", f"{self.file_name}.keras"))
