from src.population import Population
import math


def simple_function(chromosome):
    return pow(chromosome.x, 2) + pow(chromosome.y, 2) + 1
    # return 2 * chromosome.x + 5


def booth_function(chromosome):
    x = chromosome.x
    y = chromosome.y
    return pow(x + 2 * y - 7, 2) + pow(2 * x + y - 5, 2)


def bukin_function(chromosome):
    x = chromosome.x
    y = chromosome.y
    return 100 * (math.sqrt(abs(y - 0.01 * pow(x, 2)))) + 0.01 * abs(x + 10)


def easom_function(chromosome):
    x = chromosome.x
    y = chromosome.y
    return -math.cos(x) * math.cos(y) * math.exp(-pow(x - 3.14, 2) - pow(y - 3.14, 2))


def genetic_algorithm_main():
    population_size = 50
    generations = 20
    mutation_rate = 0.01
    x_boundaries = [-100, 100]
    y_boundaries = [-100, 100]

    population = Population(booth_function, mutation_rate, population_size, x_boundaries, y_boundaries)
    population.calculate_fitness()
    while generations != population.generations:

        population.best_of_all_selection(percentage=0.3)
        population.generate_new_population()
        population.calculate_fitness()
        print(population.generations)
        for i in population.population:
            print(f'x: {i.x} y: {i.y} f(x,y): {i.fitness}')


if __name__ == "__main__":
    genetic_algorithm_main()
