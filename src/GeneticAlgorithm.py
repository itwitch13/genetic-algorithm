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
    return sqrt(sin(3*x*pi)) + sqrt(x-1)*(1+sqrt(sin(3*y*pi))) + sqrt(y-1)*(1+sqrt(2*y*pi))

