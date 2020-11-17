from src.chromosome import Chromosome
import random
import sys
import math


def calculate_bin_length(x_boundary: list):
    binary = (x_boundary[1] - x_boundary[0]) * pow(10, 6) + 1
    m = math.log2(binary)
    return math.ceil(m)


def binary_to_float(binary_value, border_a, border_b, m):
    combined_value = ''.join(map(str, binary_value))
    x = border_a + int(combined_value, 2) * (border_b - border_a) / (pow(2, m) - 1)
    return x


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
    boundaries_x = [0, 0]
    boundaries_y = [0, 0]
    x_length = 0
    y_length = 0

    def __init__(self, target_function, mutation_rate, population_size, boundaries_x: list, boundaries_y: list):
        self.target_function = target_function
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.boundaries_x = boundaries_x
        self.boundaries_y = boundaries_y

        self.x_length = calculate_bin_length(boundaries_x)
        self.y_length = calculate_bin_length(boundaries_y)

        for i in range(population_size):
            self.population.append(Chromosome(self.x_length, self.y_length, is_random=True))

    def best_of_all_selection(self, percentage: float):
        best_chromosome_amount = round(len(self.population) * percentage)
        self.population.sort(key=lambda chromosome: chromosome.fitness, reverse=False)
        for i in range(best_chromosome_amount):
            self.mating_pool.append(self.population[i])

    def roulette_wheel_selection(self):
        fitness_sum = 0
        for i in range(len(self.population)):
            fitness_sum += self.population[i].fitness

        for i in range(len(self.population)):
            percentage_of_chance = 1 / (self.population[i].fitness / fitness_sum)
            percentage_of_chance *= 100
            percentage_of_chance = round(percentage_of_chance)
            for j in range(percentage_of_chance):
                self.mating_pool.append(self.population[i])

    def tournament_selection(self, size_of_tournament):
        available_chromosomes_indexes_list = [i for i in range(len(self.population))]

        while len(available_chromosomes_indexes_list) != 0:
            if len(available_chromosomes_indexes_list) >= size_of_tournament:
                single_tournament = random.sample(available_chromosomes_indexes_list, size_of_tournament)
            else:
                single_tournament = available_chromosomes_indexes_list

            winner_chromosome = self.population[single_tournament[0]]

            for index in single_tournament:
                if self.population[index].fitness < winner_chromosome.fitness:
                    winner_chromosome = self.population[index]

                available_chromosomes_indexes_list.remove(index)
            self.mating_pool.append(winner_chromosome)

    def calculate_fitness(self):
        for chromosome in self.population:
            x = binary_to_float(chromosome.x, self.boundaries_x[0], self.boundaries_x[1], self.x_length)
            y = binary_to_float(chromosome.y, self.boundaries_y[0], self.boundaries_y[1], self.y_length)
            chromosome.fitness = self.target_function(x, y)
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
        cut_index_x = round(self.x_length / 2)
        cut_index_y = round(self.y_length / 2)
        new_x = a_partner.x[0:cut_index_x] + b_partner.x[cut_index_x:]
        new_y = a_partner.y[0:cut_index_y] + b_partner.y[cut_index_y:]
        return Chromosome(new_x, new_y, is_random=False)
