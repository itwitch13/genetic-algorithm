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
    mutation_probability = 0
    crossover_probability = 0
    elite_strategy_amount = 0
    population_size = 0
    highest_fitness = sys.maxsize
    boundaries_x = [0, 0]
    boundaries_y = [0, 0]
    x_length = 0
    y_length = 0

    def __init__(self, target_function, mutation_probability, crossover_probability, elite_strategy_amount,
                 population_size,
                 boundaries_x: list, boundaries_y: list):
        self.target_function = target_function
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.elite_strategy_amount = elite_strategy_amount
        self.population_size = population_size
        self.boundaries_x = boundaries_x
        self.boundaries_y = boundaries_y

        self.x_length = calculate_bin_length(boundaries_x)
        self.y_length = calculate_bin_length(boundaries_y)

        for i in range(population_size):
            self.population.append(Chromosome(self.x_length, self.y_length, is_random=True))

        self.plot_x = []
        self.plot_y = []
        self.plot_fx = []

    def get_configuration(self, mutation_type, crossover_type):
        self.mutation_type = mutation_type
        self.crossover_type = crossover_type

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
        x_list, y_list, fx_list = [], [], []
        for chromosome in self.population:
            x = binary_to_float(chromosome.x, self.boundaries_x[0], self.boundaries_x[1], self.x_length)
            y = binary_to_float(chromosome.y, self.boundaries_y[0], self.boundaries_y[1], self.y_length)
            chromosome.fitness = self.target_function(x, y)
            x_list.append(x)
            y_list.append(y)
            fx_list.append(chromosome.fitness)
            if chromosome.fitness < self.highest_fitness:
                self.highest_fitness = chromosome.fitness

        self.plot_x.append(x_list)
        self.plot_y.append(y_list)
        self.plot_fx.append(fx_list)

    def get_plots_parameters(self):
        return self.plot_x, self.plot_y, self.plot_fx

    # def generate_new_population(self):
    #     for i in range(len(self.population)):
    #         a_partner_index = round(random.randint(0, len(self.mating_pool) - 1))
    #         b_partner_index = round(random.randint(0, len(self.mating_pool) - 1))
    #
    #         a_partner = self.mating_pool[a_partner_index]
    #         b_partner = self.mating_pool[b_partner_index]
    #
    #         child = self.crossover_one_point(a_partner, b_partner)
    #
    #         child.mutate(self.mutation_rate)
    #
    #         self.population[i] = child
    #
    #     self.mating_pool.clear()
    #     self.generations += 1

    def generate_new_population(self):
        amount_of_elite_strategy_individuals = 0
        for i in range(0, len(self.population), 2):
            a_partner_index = round(random.randint(0, len(self.mating_pool) - 1))
            b_partner_index = round(random.randint(0, len(self.mating_pool) - 1))

            a_partner = self.mating_pool[a_partner_index]
            a_partner_if_is_elite = self.mating_pool[a_partner_index]

            b_partner = self.mating_pool[b_partner_index]
            b_partner_if_is_elite = self.mating_pool[b_partner_index]

            crossover_chance = random.uniform(0, 1)
            if crossover_chance < self.crossover_probability:
                # a_partner, b_partner = self.crossover_two_point(a_partner, b_partner)
                a_partner, b_partner = self.crossover(a_partner, b_partner, self.crossover_type)

            a_partner = self.mutation(a_partner, self.mutation_type)
            b_partner = self.mutation(b_partner, self.mutation_type)

            if self.check_if_elite(a_partner_if_is_elite, amount_of_elite_strategy_individuals):
                self.population[i] = a_partner_if_is_elite
                amount_of_elite_strategy_individuals += 1
            else:
                self.population[i] = a_partner

            if self.check_if_elite(b_partner_if_is_elite, amount_of_elite_strategy_individuals):
                self.population[i + 1] = b_partner_if_is_elite
                amount_of_elite_strategy_individuals += 1
            else:
                self.population[i + 1] = b_partner

        self.mating_pool.clear()
        self.generations += 1

    def crossover_one_point(self, a_partner: Chromosome, b_partner: Chromosome):
        cut_index_x = round(self.x_length / 2)
        cut_index_y = round(self.y_length / 2)
        a_partner.x = a_partner.x[0:cut_index_x] + b_partner.x[cut_index_x:]
        b_partner.x = b_partner.x[0:cut_index_x] + a_partner.x[cut_index_x:]
        a_partner.y = a_partner.y[0:cut_index_y] + b_partner.y[cut_index_y:]
        b_partner.y = b_partner.y[0:cut_index_y] + a_partner.y[cut_index_y:]
        return Chromosome(a_partner.x, a_partner.y, is_random=False), Chromosome(b_partner.x, b_partner.y,
                                                                                 is_random=False)

    def crossover_two_point(self, a_partner: Chromosome, b_partner: Chromosome):
        cut_index_x, x_rest = divmod(self.x_length, 3)
        cut_index_y, y_rest = divmod(self.y_length, 3)
        a_partner.x = a_partner.x[0:cut_index_x] + b_partner.x[cut_index_x:2 * cut_index_x + x_rest] + a_partner.x[
                                                                                                       2 * cut_index_x + x_rest:]
        b_partner.x = b_partner.x[0:cut_index_x] + a_partner.x[cut_index_x:2 * cut_index_x + x_rest] + b_partner.x[
                                                                                                       2 * cut_index_x + x_rest:]
        a_partner.y = a_partner.y[0:cut_index_y] + b_partner.y[cut_index_y:2 * cut_index_y + y_rest] + a_partner.y[
                                                                                                       2 * cut_index_y + y_rest:]
        b_partner.y = b_partner.y[0:cut_index_y] + a_partner.y[cut_index_y:2 * cut_index_y + y_rest] + b_partner.y[
                                                                                                       2 * cut_index_y + y_rest:]
        return Chromosome(a_partner.x, a_partner.y, is_random=False), Chromosome(b_partner.x, b_partner.y,
                                                                                 is_random=False)

    def crossover_homogenous(self, a_partner: Chromosome, b_partner: Chromosome):
        for i in range(self.x_length):
            if i % 2 == 0:
                old_x = a_partner.x[i]
                a_partner.x[i] = b_partner.x[i]
                b_partner.x[i] = old_x

        for i in range(self.y_length):
            if i % 2 == 0:
                old_y = a_partner.y[i]
                a_partner.y[i] = b_partner.y[i]
                b_partner.y[i] = old_y

        return Chromosome(a_partner.x, a_partner.y, is_random=False), Chromosome(b_partner.x, b_partner.y,
                                                                                 is_random=False)

    def check_if_elite(self, a: Chromosome, current_count: int):
        if (a.fitness == self.highest_fitness) and (current_count <= self.elite_strategy_amount):
            return True
        else:
            return False

    def mutation(self, a: Chromosome, mutation_type: str) -> Chromosome:
        local_mutation_probability = random.uniform(0, 1)
        if local_mutation_probability < self.mutation_probability:
            if mutation_type == 'edge_mutation':
                a.edge_mutation()
            elif mutation_type == 'one_point_mutation':
                a.one_point_mutation()
            elif mutation_type == 'two_points_mutation':
                a.two_points_mutation()
            elif mutation_type == 'inversion_mutation':
                a.inversion_mutation()
        return a

    def crossover(self, a: Chromosome, b: Chromosome, crossover_type: str):
        if crossover_type == 'crossover_one_point':
            return self.crossover_one_point(a, b)
        elif crossover_type == 'crossover_two_point':
            return self.crossover_two_point(a, b)
        elif crossover_type == 'crossover_homogenous':
            return self.crossover_homogenous(a, b)

    def selection(self, selection_type: str, percentage, size_of_tournament):
        if selection_type == 'best_of_all_selection':
            self.best_of_all_selection(percentage)
        elif selection_type == 'roulette_wheel_selection':
            self.roulette_wheel_selection()
        elif selection_type == 'tournament_selection':
            self.tournament_selection(size_of_tournament)
