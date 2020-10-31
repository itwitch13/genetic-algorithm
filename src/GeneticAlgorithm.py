import random
from math import *

# levy function
# x <-10,10>
# f(x)=0, dla x=(1,1)

size = 9
x_boundaries = [-10,10]


def generate_population(size, x_boundaries, y_boundaries):
    lower_x_boundary, upper_x_boundary = x_boundaries
    lower_y_boundary, upper_y_boundary = y_boundaries

    population = []
    for i in range(size):
        individual = {
            "x": random.uniform(lower_x_boundary, upper_x_boundary),
            "y": random.uniform(lower_y_boundary, upper_y_boundary),
        }
        population.append(individual)

    return population


def apply_function(individual):
    x = individual["x"]
    y = individual["y"]
    # TODO: gets some error, fix the function
    return sqrt(sin(3*x*pi)) + sqrt(x-1)*(1+sqrt(sin(3*y*pi))) + sqrt(y-1)*(1+sqrt(2*y*pi))

def sort_population_by_fitness(population):
    return sorted(population, key=apply_function)

# ----------------------------------

generations = 5

population = generate_population(size=10, x_boundaries=(-10, 10), y_boundaries=(-4, 4))

i = 1
while True:
    print(f"GENERATION {i}")

    for individual in population:
        print(individual)

    if i == generations:
        break

    i += 1


best_individual = sort_population_by_fitness(population)[-1]
print("\nFINAL RESULT")
print(best_individual, apply_function(best_individual))