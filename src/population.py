from src.Chromosome import Chromosome
import random
import sys


class Population:
    def target_function(self):
        pass

    population = []
    mating_pool = []
    generations = 0
    finished = False
    perfect_score = 1
    mutation_rate = 0
    population_size = 0
    highest_fitness = sys.maxsize

    def __init__(self, target_function, mutation_rate, population_size, x_boundaries: list, y_boundaries: list):
        self.target_function = target_function
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        for i in range(population_size):
            self.population.append(Chromosome(x_boundaries[0], x_boundaries[1], y_boundaries[0], y_boundaries[1]))

    def best_of_all_selection(self, percentage: float):
        best_chromosome_amount = round(len(self.population) * percentage)
        self.population.sort(key=lambda chromosome: chromosome.fitness, reverse=False)
        for i in range(best_chromosome_amount):
            self.mating_pool.append(self.population[i])

    def calculate_fitness(self):
        for chromosome in self.population:
            chromosome.fitness = self.target_function(chromosome)
            if chromosome.fitness < self.highest_fitness:
                self.highest_fitness = chromosome.fitness

    def generate_new_population(self):
        for i in range(len(self.population)):
            a_partner_index = round(random.randint(0, len(self.mating_pool) - 1))
            b_partner_index = round(random.randint(0, len(self.mating_pool) - 1))

            a_partner = self.mating_pool[a_partner_index]
            b_partner = self.mating_pool[b_partner_index]

            child = self.crossover(a_partner, b_partner)

            child.mutate(self.mutation_rate)

            self.population[i] = child

        self.mating_pool.clear()
        self.generations += 1

    def crossover(self, a_partner: Chromosome, b_partner: Chromosome):
        new_x = round((a_partner.x + b_partner.x) / 2)
        new_y = round((a_partner.y + b_partner.y) / 2)
        return Chromosome(new_x, new_y)

    def minimum_fitness(self):
        print(f'\n{self.highest_fitness}')