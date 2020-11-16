from src.chromosome import Chromosome
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
        new_x = (a_partner.x + b_partner.x) / 2
        new_y = (a_partner.y + b_partner.y) / 2
        return Chromosome(new_x, new_y)
