from src.population import Population
from src.example_functions import *


def genetic_algorithm_main():
    population_size = 100
    generations = 20
    mutation_rate = 0.01
    x_boundaries = [-100, 100]
    y_boundaries = [-100, 100]

    population = Population(booth_function, mutation_rate, population_size, x_boundaries, y_boundaries)
    population.calculate_fitness()
    while generations != population.generations:

        # population.best_of_all_selection(percentage=0.3)
        # population.roulette_wheel_selection()
        population.tournament_selection(3)
        population.generate_new_population()
        population.calculate_fitness()
        print(population.generations)
        for i in population.population:
            print(f'x: {i.x} y: {i.y} f(x,y): {i.fitness}')


if __name__ == "__main__":
    genetic_algorithm_main()
