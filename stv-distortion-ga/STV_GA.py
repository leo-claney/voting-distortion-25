"""
This is a GA to find max distortion scenarios for STV
"""
import random
from vote import Vote
from election import Election

class STV_GA:
    def __init__(self, m: int = 3, n: int = 4, population_size: int = 25):
        self.num_of_candidates = m
        self.num_of_voters = n
        self.population_size = population_size
        self.allele_len = 128
        self.population_fitness = {}
        self.most_fit = None
        self.population = self.generate_population(population_size)
        self.pop_fitness()
        

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
            individual.append(random.randint(1,self.allele_len))
        return individual
    
    def run_stv(self, individual):
        """
        Run STV on an individual
        """
        candidates = individual[:self.num_of_candidates]
        voters = individual[self.num_of_candidates:]

        # Get the OPT candidate and social costs
        social_costs = {}
        minDistance = float('inf')
        OPTcandidate = candidates[0]
        for i in range(len(candidates)):
            sumDistance = 0
            for voter in voters:
                distance = abs(candidate - voter)
                sumDistance += distance
            if sumDistance < minDistance:
                minDistance = sumDistance
                OPTcandidate = candidate
            social_costs[candidate] = sumDistance

        # Generate ballots
        ballots = []
        for voter in voters:
            distances = {}
            for candidate in candidates:
                distance = abs(candidate - voter)
                distances[candidate] = distance         
            sorted_dict = sorted(distances, key = distances.get)
            ballots.append(sorted_dict)

        votes = []
        for ballot in ballots:
            vote = Vote(ballot)
            votes.append(vote)
        election = Election(votes)
        election.run_election()
        winner = election.winner

    def fitness(self, individual):
        """
        Calculate fitness of an individual
        """
        return sum(individual)
    
    def pop_fitness(self):
        """
        Calculate the fitness of each individual in the population
        """
        for i in range(self.population_size):
            self.population_fitness[i] = self.fitness(self.population[i])
            if self.most_fit is None or self.population_fitness[i] > self.population_fitness[self.most_fit]:
                self.most_fit = i

    def get_fittest(self):
        """
        Get the fittest individual
        """
        return self.population[self.most_fit], self.population_fitness[self.most_fit]

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
                # individual[i] = (random.randint(-5,5) + individual[i]) % self.allele_len
                individual[i] = random.randint(1,self.allele_len)
        return individual

    def build_next_generation(self):
        """
        Build the next generation
        """
        next_generation = [self.population[self.most_fit]]
        for i in range(self.population_size-1):
            parents = []
            j = 0
            while len(parents) < 2:
                odds = 1/(j+2)
                if random.random() < odds:
                    parents.append(self.population[j])
                j = (j+1) % self.population_size
            parent1 = parents[0]
            parent2 = parents[1]
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            next_generation.append(child)
        self.population = next_generation
        self.pop_fitness()
        return next_generation

    
    

def main():
    stv = STV_GA()
    max_fitness = 0
    best_generation = 0
    for i in range(100):
        print(f'Generation {i+1}')
        fittest, fitness = stv.get_fittest()
        print(f'Fittest individual: {fittest}')
        print(f'Fitness: {fitness}')
        if fitness > max_fitness:
            max_fitness = fitness
            best_generation = i+1
        stv.build_next_generation()
        print()
    print(f'Max fitness: {max_fitness} at generation {best_generation}')

if __name__ == "__main__":
    main()