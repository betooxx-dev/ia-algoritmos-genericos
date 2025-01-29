from typing import List
import numpy as np

class LinearRegressionGA:
    def __init__(self, population_size: int = 100, generations: int = 50, mutation_rate: float = 0.1):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.n_features = None
        self.elite_size = int(population_size * 0.1)
        
    def normalize_data(self, X: np.ndarray) -> tuple:
        self.X_mean = np.mean(X, axis=0)
        self.X_std = np.std(X, axis=0)
        return (X - self.X_mean) / (self.X_std + 1e-8)
    
    def initialize_population(self, n_features: int) -> List[dict]:
        self.n_features = n_features
        population = []
        for _ in range(self.population_size):
            individual = {
                'coefs': np.random.uniform(-1, 1, n_features),
                'b': np.random.uniform(-1, 1)
            }
            population.append(individual)
        return population
    
    def fitness(self, individual: dict, X: np.ndarray, Y: np.ndarray) -> float:
        predictions = np.dot(X, individual['coefs']) + individual['b']
        mse = np.mean((predictions - Y) ** 2)
        r2 = 1 - (np.sum((Y - predictions) ** 2) / np.sum((Y - np.mean(Y)) ** 2))
        return -mse * (0.8 + 0.2 * r2)
        
    def crossover(self, parent1: dict, parent2: dict) -> dict:
        alpha = np.random.random()
        child_coefs = alpha * parent1['coefs'] + (1 - alpha) * parent2['coefs']
        child_b = alpha * parent1['b'] + (1 - alpha) * parent2['b']
        return {'coefs': child_coefs, 'b': child_b}
        
    def mutate(self, individual: dict) -> dict:
        if np.random.random() < self.mutation_rate:
            mutation = np.random.normal(0, 0.1, self.n_features)
            individual['coefs'] += mutation
        if np.random.random() < self.mutation_rate:
            individual['b'] += np.random.normal(0, 0.1)
        return individual
        
    def evolve(self, X: np.ndarray, Y: np.ndarray):
        X_norm = self.normalize_data(X)
        population = self.initialize_population(X.shape[1])
        best_solution = None
        best_fitness = float('-inf')
        
        for _ in range(self.generations):
            fitness_values = [(ind, self.fitness(ind, X_norm, Y)) for ind in population]
            fitness_values.sort(key=lambda x: x[1], reverse=True)
            
            elites = [ind for ind, _ in fitness_values[:self.elite_size]]
            current_best = fitness_values[0][0]
            current_fitness = fitness_values[0][1]
            
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_solution = current_best.copy()
            
            selected = [ind for ind, _ in fitness_values[:self.population_size//2]]
            
            new_population = elites.copy()
            while len(new_population) < self.population_size:
                parent1 = np.random.choice(selected)
                parent2 = np.random.choice(selected)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            population = new_population
        
        return best_solution