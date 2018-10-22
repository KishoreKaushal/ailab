# Genetic algorithm: generating target string from random string

import random
import numpy as np

POPULATION_SIZE = 200

# valid characters(genes)
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .!@#$%^&*()'''
# target string(genome)
TARGET = 'Madness is like gravity.'

class Individual(object):
    '''
        This class represents individual in the population
    '''

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()
    
    @classmethod
    def mutate(self):
        '''
            generating random genes for the mutation
        '''
        global GENES
        return random.choice(GENES)

    @classmethod
    def create_gnome(self):
        '''
            create string of genes
        '''
        global TARGET
        return [self.mutate() for _ in range(len(TARGET))] 

    def mate(self, par2):
        '''
            Mate and reproduce new offspring
        '''

        # chromosome for offspring
        child_chromosome = []

        for gp1,gp2 in zip(self.chromosome , par2.chromosome):
            # random probability
            # probability = random.random()

            # # if probability is less than 0.45
            # # insert gene from parent 1 
            # if probability < 0.45:
            #     child_chromosome.append(gp1)
            
            # # if probability is less than 0.90 and greater than 0.45
            # # insert gene from parent 2 
            # elif probability < 0.90:
            #     child_chromosome.append(gp2)

            # # otherwise maintain the diversity
            # else:
            #     child_chromosome.append(self.mutate())
            
            probability_of_crossover = random.random()

            if (probability_of_crossover > 0.1):
                # do crossover
                probability_of_p1_gene = random.random()
                if probability_of_p1_gene > 0.5:
                    child_chromosome.append(gp1)
                else:
                    child_chromosome.append(gp2)
            else:
                # do mutation
                child_chromosome.append(self.mutate())

        
        # create new Individial(offspring) using 
        # generated chromosome for offspring
        return Individual(child_chromosome)


    def calculate_fitness(self):
        '''
            What is fitness?
            Calculate fittness score, it is the number of
            characted in string which differ from target string.
        '''
        global TARGET
        fitness = 0
        for gs,gt in zip(self.chromosome, TARGET):
            if gs!=gt:
                fitness+=1
        return fitness


def main():
    global POPULATION_SIZE
    global TARGET
    TARGET = input("Target String , characters allowed:  [a-zA-Z .!@#$%^&*()]  \n")
    # current generation
    generation = 1

    found = False
    population = []

    # create initial population
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    while not found:
        
        # sort the population in increasing order of fitness score
        population = sorted(population, key = lambda x:x.fitness)

        # a fitness score of 0 means that the TARGET string is
        # reached and hence break the loop
        if population[0].fitness <= 0:
            found = True
            break

        # Otherwise generate new offsprings for new generation
        new_generation = []

        # Perform Elitism, that mean 10% of fittest population
        # goes to the next generation
        s = int(0.10*POPULATION_SIZE)
        new_generation.extend(population[:s])

        # from 30% of the fittest population, Individuals 
        # will mate to produce offspring
        s = int(0.90*POPULATION_SIZE) 
        for _ in range(s):
            parent1 = random.choice(population[:30])
            parent2 = random.choice(population[:30])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        print("Gen: {} Str: {} Fit: {}".format(generation, "".join(population[0].chromosome), population[0].fitness))

        generation += 1
    
    print("Gen: {} Str: {}\tFit: {}".format(generation, "".join(population[0].chromosome), population[0].fitness))

if __name__ == "__main__":
    main()