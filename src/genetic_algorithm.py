from typing import Callable, List, Tuple
from abc import ABC, abstractmethod
import random


class Individual(ABC):
    @abstractmethod
    def mutate(self, p_m: float):
        """Mutate the individual's chromosomes.

        :param p_m: The probability for a given gene to be mutated
        """
        pass

    @abstractmethod
    def crossover(self, other: 'Individual', p_c: float) -> Tuple['Individual', 'Individual']:
        """Create two children with another individual by crossing over genes.

        :param other: The other individual to crossover with
        :param p_c: The probability that a given gene will be crossed with the other's gene
        :return: A tuple containing the children
        """
        pass

    @abstractmethod
    def get_fitness(self) -> float:
        """Calculate this individual's fitness. The fitness is a value between 0 (minimum) and 1 (maximum)."""
        pass


def calculate_fitnesses(population: List[Individual]):
    """Force all members of the given population to calculate their fitness values."""
    for individual in population:
        individual.get_fitness()


def run(generate: Callable[[], List[Individual]], p_c: float, p_m: float,
        p_avoid: float) -> Individual:
    """
    Run the genetic algorithm.

    :param generate: A function used to generate the initial population of data points
    :param p_c: The probability that an individual's gene will crossover with another individual's gene
    :param p_m: The probability that an individual's gene will be mutated
    :param p_avoid: The probability that the best individual in the population will not be selected for breeding
    :return: The best individual in the final generation
    """

    population = generate()
    best_ind = population[0]

    while best_ind.get_fitness() < 1:
        calculate_fitnesses(population)
        new_pop = []
        for j in range(len(population)//2):
            ind_1, ind_2 = select(population, p_avoid)
            child_1, child_2 = ind_1.crossover(ind_2, p_c)
            child_1.mutate(p_m)
            child_2.mutate(p_m)
            if child_1.get_fitness() > best_ind.get_fitness():
                best_ind = child_1
            if child_2.get_fitness() > best_ind.get_fitness():
                best_ind = child_2
            new_pop.append(child_1)
            new_pop.append(child_2)
        population = new_pop

    best_ind._fitness = None
    best_ind.get_fitness()
    return best_ind


def select(population: List[Individual], p_avoid: float) -> Tuple[Individual, Individual]:
    """
    Select two individuals in the given population via roulette wheel selection. Attempts to avoid breeding individual
    with the highest fitness at a rate given by p_avoid.

    :param population: The population to search
    :param p_avoid: The probability that the individual with the highest fitness will not be selected
    :return: A tuple containing the selected individuals
    """
    ind_1, ind_2 = None, None

    # Calculate the total fitness of the population
    total_fitness, highest_fitness = 0, 0
    best_ind = None
    for individual in population:
        total_fitness += individual.get_fitness()
        if individual.get_fitness() > highest_fitness:
            best_ind = individual

    # Select individuals
    while ind_2 is None:
        for individual in population:
            if random.random() <= individual.get_fitness()/total_fitness:
                if individual == best_ind and random.random() <= p_avoid:
                    continue
                if ind_1 is None:
                    ind_1 = individual
                else:
                    ind_2 = individual
                    break

    return ind_1, ind_2
