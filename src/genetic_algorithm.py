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
    def crossover(self, other: 'Individual', p_c: float):
        """Crossover genes with another individual.

        :param other: The other individual to crossover with
        :param p_c: The probability that a given gene will be crossed with the other's gene
        """
        pass

    @abstractmethod
    def get_fitness(self) -> float:
        """Calculate this individual's fitness. The fitness is a value between 0 (minimum) and 1 (maximum)."""
        pass


def run(generate: Callable[[], List[Individual]], num_iterations: int, p_c: float, p_m: float,
        p_avoid: float) -> List[Individual]:
    """
    Run the genetic algorithm for the specified number of iterations.

    :param generate: A function used to generate the initial population of data points
    :param num_iterations: The number of iterations the genetic algorithm will run for
    :param p_c: The probability that an individual's gene will crossover with another individual's gene
    :param p_m: The probability that an individual's gene will be mutated
    :param p_avoid: The probability that the best individual in the population will not be selected for breeding
    :return: The last generation of data points
    """

    population = generate()

    for i in range(num_iterations):
        ind_1, ind_2 = select(population, p_avoid)
        ind_1.crossover(ind_2, p_c)
        ind_1.mutate(p_m)
        ind_2.mutate(p_m)

    return population


def select(population: List[Individual], p_avoid: float) -> Tuple[Individual, Individual]:
    """
    Select two individuals in the given population via roulette wheel selection. Attempts to avoid breeding individual
    with the highest fitness at a rate given by p_avoid.

    :param population: The population to search
    :param p_avoid: The probability that for any given individual
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
