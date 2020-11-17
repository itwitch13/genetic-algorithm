import random
import numpy as np


class Chromosome:
    x = 0
    y = 0
    genes = []
    fitness = 0

    def __init__(self, *args, is_random: bool):
        if is_random:
            self.x = [random.randint(0, 1) for i in range(args[0])]
            self.y = [random.randint(0, 1) for i in range(args[1])]
        else:
            self.x = args[0]
            self.y = args[1]

    def mutate(self, mutation_rate):
        for i in range(len(self.x)):
            chance = random.uniform(0, 1)
            if chance < mutation_rate:
                self.x[i] = 1 if self.x[i] == 0 else 0
                self.y[i] = 1 if self.y[i] == 0 else 0
