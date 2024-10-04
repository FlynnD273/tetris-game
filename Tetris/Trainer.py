from .Tile import Tile
from .Game import Game
from .AI import AI

import pygad.kerasga
import pygad


##from pygad
class Trainer:
    """The Trainer for the AI"""

    def __init__(self) -> None:
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
        while game.isRunning and game.ticks < 2000:
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
        return game.ticks + 100 * game.score + 100 * max_height

    def _callback(self, ga):
        """print generation data"""
        print(f"Generation = {ga.generations_completed}/{self.generations}")
        print(f"Best Steps = {ga.best_solution()[1]}")

    def train(
        self, file_name, num_solutions=10, num_generations=25, num_parents_mating=5
    ):
        """run the genetic algorithm and save results to file_name"""
        self.generations = num_generations

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
        self.ai.model.save(f"{file_name}.keras")
