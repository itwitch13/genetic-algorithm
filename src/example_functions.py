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
