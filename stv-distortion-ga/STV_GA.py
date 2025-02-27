"""
This is a GA to find max distortion scenarios for STV
"""
import random

class STV_GA:
    def __init__(self, m: int = 3, n: int = 4, population_size: int = 25):
        self.num_of_candidates = m
        self.num_of_voters = n
        self.population_size = population_size
        self.population = self.generate_population(population_size)
        self.population_fitness = {}
        self.allele_length = 128

    def generate_population(self, population_size: int = 10):
        """
        Generate a population of size population_size
        """
        population = []
        for i in range(population_size):
            population.append(self.generate_individual())
        return population
    
    def generate_individual(self):
        """
        Generate a single individual
        """
        individual = []
        for i in range(self.num_of_voters+self.num_of_candidates):
            individual.append(random.randint(1,self.allele_length))
        return individual

    def fitness(self, individual):
        """
        Calculate fitness of an individual
        """
        return sum(individual)

    def crossover(self, parent1, parent2):
        """
        Crossover two parents to produce a child
        """
        child = []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def mutate(self, individual):
        """
        Mutate an individual
        """
        for i in range(len(individual)):
            if random.random() < 0.01:
                individual[i] = (random.randint(-5,5) + individual[i]) % self.allele_length
        return individual

    def build_next_generation(self):
        """
        Build the next generation
        """
        next_generation = []
        for i in range(self.population_size):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            next_generation.append(child)
        self.population = next_generation

    
    

def main():
    stv = STV_GA()
    print(stv.population)

if __name__ == "__main__":
    main()