import random


class Chromosome:
    x = 0
    y = 0
    genes = []
    fitness = 0

    def __init__(self, *args):
        if len(args) == 4:
            self.x = random.uniform(args[0], args[1])
            self.y = random.uniform(args[2], args[3])

        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
            # print(f'{self.x} {self.y}')

    def mutate(self, mutation_rate):
        chance = random.uniform(0, 1)
        if chance < mutation_rate:
            self.x += random.uniform(-0.01, 0.01)
            self.y += random.uniform(-0.01, 0.01)