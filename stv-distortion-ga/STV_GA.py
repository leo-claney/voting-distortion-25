"""
This is a GA to find max distortion scenarios for STV
"""
import random

class STV_GA:
    def __init__(self, m: int = 2, n: int = 3, population_size: int = 10):
        self.num_of_candidates = m
        self.num_of_voters = n
        self.population_size = population_size
        self.population = self.generate_population(population_size)

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
            individual.append(random.randint(1,64))
        return individual
    
    
    

def main():
    stv = STV_GA()
    print(stv.population)

if __name__ == "__main__":
    main()