from src.population import Population
from src.example_functions import *
import numpy as np


def binary_to_float(binary_value, border_a, border_b, m):
    combined_value = ''.join(map(str, binary_value))
    x = border_a + int(combined_value, 2) * (border_b - border_a) / (pow(2, m) - 1)
    return x


def genetic_algorithm_main():
    population_size = 50
    generations = 200
    mutation_probability = 0.01
    crossover_probability = 0.9
    # amount of best records to be moved to next population
    elite_strategy_amount = 2
    x_boundaries = [-10, 10]
    y_boundaries = [-10, 10]

    percentage_selection = 0.01
    size_of_tournament = 2

    population = Population(booth_function, mutation_probability, crossover_probability, elite_strategy_amount,
                            population_size, x_boundaries,
                            y_boundaries)
    population.calculate_fitness()
    while generations != population.generations:

        # population.best_of_all_selection(percentage=0.3)
        # population.roulette_wheel_selection()
        population.selection('roulette_wheel_selection', configuration_parameter=0)
        # population.tournament_selection(3)
        population.generate_new_population()
        population.calculate_fitness()
        print(population.generations)
        for i in population.population:
            print(
                f'x: {binary_to_float(i.x, x_boundaries[0], x_boundaries[1], len(i.x))} \
                y: {binary_to_float(i.y, y_boundaries[0], y_boundaries[1], len(i.y))} \
                f(x,y): {i.fitness}')


if __name__ == "__main__":
    genetic_algorithm_main()
