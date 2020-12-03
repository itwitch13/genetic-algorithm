import math
import random
import numpy as np


def calculate_bin_length(x_boundary: list):
    binary = (x_boundary[1] - x_boundary[0]) * pow(10, 6) + 1
    m = math.log2(binary)
    return math.ceil(m)


class Chromosome:
    x = 0
    y = 0
    genes = []
    fitness = 0

    def __init__(self, *args, is_random: bool, is_in_real_value: bool):
        if not is_in_real_value:
            if is_random:
                self.x = [random.randint(0, 1) for i in range(args[0])]
                self.y = [random.randint(0, 1) for i in range(args[1])]
            else:
                self.x = args[0]
                self.y = args[1]

        if is_in_real_value:
            if is_random:
                self.x = random.randint(args[0][0], args[0][1])
                self.y = random.randint(args[1][0], args[1][1])
            else:
                self.x = args[0]
                self.y = args[1]

    def mutate(self, mutation_rate):
        mutated = False
        for i in range(len(self.x)):
            chance = random.uniform(0, 1)
            if chance < mutation_rate:
                self.x[i] = 1 if self.x[i] == 0 else 0
                self.y[i] = 1 if self.y[i] == 0 else 0
                mutated = True
            if mutated:
                break

    def edge_mutation(self):
        self.x[-1] = 1 if self.x[-1] == 0 else 0
        self.y[-1] = 1 if self.y[-1] == 0 else 0

    def one_point_mutation(self):
        random_point_x = random.randint(0, len(self.x) - 1)
        random_point_y = random.randint(0, len(self.y) - 1)
        self.x[random_point_x] = 1 if self.x[random_point_x] == 0 else 0
        self.y[random_point_y] = 1 if self.y[random_point_y] == 0 else 0

    def two_points_mutation(self):
        random_point_x_first = random.randint(0, len(self.x) - 1)
        random_point_x_second = random.randint(0, len(self.x) - 1)
        random_point_y_first = random.randint(0, len(self.y) - 1)
        random_point_y_second = random.randint(0, len(self.y) - 1)

        self.x[random_point_x_first] = 1 if self.x[random_point_x_first] == 0 else 0
        self.x[random_point_x_second] = 1 if self.x[random_point_x_second] == 0 else 0
        self.y[random_point_y_first] = 1 if self.y[random_point_y_first] == 0 else 0
        self.y[random_point_y_second] = 1 if self.y[random_point_y_second] == 0 else 0

    def inversion_mutation(self):
        random_point_x_first = random.randint(0, len(self.x) - 1)
        random_point_x_second = random.randint(0, len(self.x) - 1)
        random_point_y_first = random.randint(0, len(self.y) - 1)
        random_point_y_second = random.randint(0, len(self.y) - 1)

        self.inversion('x', random_point_x_first, random_point_x_second)
        self.inversion('y', random_point_y_first, random_point_y_second)

    def real_values_uniform_mutation(self, boundaries_x: list, boundaries_y: list):
        choosen_gene = random.randint(0, 1)
        if choosen_gene == 0:
            self.x = random.randint(boundaries_x[0], boundaries_x[1])
        elif choosen_gene == 1:
            self.y = random.randint(boundaries_y[0], boundaries_y[1])

    def inversion(self, chromo, point1, point2):
        if chromo == 'x':
            if point1 < point2:
                self.x[point1:point2] = self.x[point1:point2][::-1]
            else:
                self.x[point2:point1] = self.x[point2:point1][::-1]

        elif chromo == 'y':
            if point1 < point2:
                self.y[point1:point2] = self.y[point1:point2][::-1]
            else:
                self.y[point2:point1] = self.y[point2:point1][::-1]
