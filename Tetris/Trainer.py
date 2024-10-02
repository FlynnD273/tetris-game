from tensorflow import keras
import pygad.kerasga
import numpy
import pygad

from .Game import Game
from .AI import AI


##from pygad
class Trainer:

    def __init__(self) -> None:
        self.ai = AI()

    def _run_tetris(self, _ga, solution, _sol_idx):

        model_weights_matrix = pygad.kerasga.model_weights_as_matrix(
            model=self.ai.model, weights_vector=solution
        )

        self.ai.model.set_weights(weights=model_weights_matrix)

        game = Game()
        while game.isRunning:
            action = self.ai.get_action()
            game.actionPressed[action] = True
            game.gameTick()

        return game.ticks

    def _callback(ga):
        print(f"Generation = {ga.generations_completed}")
        print(f"Fitness    = {ga.best_solution()[1]}")

    """run the genetic algorithm"""

    def train(self, file_name):

        # Create an instance of the pygad.kerasga.KerasGA class to build the initial population.
        keras_ga = pygad.kerasga.KerasGA(model=self.ai.model, num_solutions=10)

        # Prepare the PyGAD parameters. Check the documentation for more information: https://pygad.readthedocs.io/en/latest/pygad.html#pygad-ga-class
        num_generations = 25  # Number of generations.
        num_parents_mating = (
            5  # Number of solutions to be selected as parents in the mating pool.
        )
        initial_population = (
            keras_ga.population_weights
        )  # Initial population of network weights.

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

        # After the generations complete, some plots are showed that summarize how the outputs/fitness values evolve over generations.
        ga_instance.plot_fitness(title="Iteration vs. Fitness", linewidth=4)

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
        self.ai.model.save(file_name)
