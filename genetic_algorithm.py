import numpy as np
import math

class GeneticAlgorithm:
    def __init__(self, function, x_min, x_max, dx, min_population, max_population, generations, crossover_prob, mutation_prob, bit_mutation_prob):
        self.function = function
        self.x_min = x_min
        self.x_max = x_max
        self.dx = dx
        self.min_population = min_population
        self.max_population = max_population
        self.population_size = max_population
        self.generations = generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.bit_mutation_prob = bit_mutation_prob
        self.setup_parameters()

    def setup_parameters(self):
        self.n_points = int((self.x_max - self.x_min) / self.dx) + 1
        self.n_bits = math.ceil(math.log2(self.n_points))
        self.dx_system = (self.x_max - self.x_min) / (2**self.n_bits - 1)

    def initialize_population(self):
        return [''.join(np.random.choice(['0', '1']) for _ in range(self.n_bits)) 
                for _ in range(self.population_size)]

    def fitness(self, individual):
        decimal = int(individual, 2)
        x = self.x_min + decimal * self.dx_system
        return self.function(x)

    def get_population_stats(self, population):
        x_values = []
        fitness_values = []
        for individual in population:
            x, fx = self.decode_solution(individual)
            x_values.append(x)
            fitness_values.append(fx)
        return x_values, fitness_values

    def select_best(self, population):
        fitness_values = [(individual, self.fitness(individual)) for individual in population]
        population_sorted = [ind for ind, _ in sorted(fitness_values, key=lambda x: x[1], reverse=True)]
        n_selected = max(self.min_population, len(population) // 2)
        return population_sorted[:n_selected]

    def crossover(self, population):
        fitness_values = [(individual, self.fitness(individual)) for individual in population]
        population_sorted = [ind for ind, _ in sorted(fitness_values, key=lambda x: x[1], reverse=True)]
        
        new_population = []
        pairs = []
        
        for i in range(len(population_sorted)):
            if np.random.random() <= self.crossover_prob:
                j = np.random.randint(0, i+1)
                pairs.append((i, j))
                
                parent1 = population_sorted[i]
                parent2 = population_sorted[j]
                
                crossover_point = np.random.randint(1, self.n_bits)
                
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
                
                new_population.extend([child1, child2])
            else:
                new_population.append(population_sorted[i])
        
        return new_population, len(pairs)

    def prune_population(self, population):
        if not population:
            return population
            
        fitness_values = [(ind, self.fitness(ind)) for ind in population]
        
        seen_individuals = {}
        unique_population = []
        
        for ind, fitness in sorted(fitness_values, key=lambda x: x[1], reverse=True):
            if ind not in seen_individuals:
                seen_individuals[ind] = True
                unique_population.append(ind)
        
        if len(unique_population) <= self.max_population:
            return unique_population
            
        return unique_population[:self.max_population]

    def mutate(self, population):
        mutated_population = []
        total_mutations = 0
        total_mutated_bits = 0
        
        for individual in population:
            mutated_individual = list(individual)
            individual_mutated = False
            
            if np.random.random() <= self.mutation_prob:
                for i in range(self.n_bits):
                    if np.random.random() <= self.bit_mutation_prob:
                        mutated_individual[i] = '1' if mutated_individual[i] == '0' else '0'
                        total_mutated_bits += 1
                        individual_mutated = True
                
                if individual_mutated:
                    total_mutations += 1
            
            mutated_population.append(''.join(mutated_individual))
        
        return mutated_population, total_mutations, total_mutated_bits

    def get_best_and_worst(self, population):
        fitness_values = [(individual, self.fitness(individual)) for individual in population]
        sorted_individuals = sorted(fitness_values, key=lambda x: x[1], reverse=True)
        return sorted_individuals[0][0], sorted_individuals[-1][0]

    def decode_solution(self, binary_string):
        decimal = int(binary_string, 2)
        x = self.x_min + decimal * self.dx_system
        fx = self.fitness(binary_string)
        return x, fx