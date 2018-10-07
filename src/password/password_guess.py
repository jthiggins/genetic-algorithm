from typing import Callable, Tuple
import genetic_algorithm
import random


class Password(genetic_algorithm.Individual):
    def __init__(self, char_list: list, goal_hash: int, hash_func: Callable[[str], int]):
        self._char_list = char_list
        self._goal_hash = goal_hash
        self._hash_func = hash_func
        self._fitness = None

    def __str__(self):
        return "".join(self._char_list)

    def get_fitness(self) -> float:
        if self._fitness is not None and self._fitness != 1:
            return self._fitness
        diff = abs(self._hash_func(str(self)) - self._goal_hash)
        if diff == 0:
            self._fitness = 1
        else:
            self._fitness = 1/diff
        return self._fitness

    def crossover(self, other: 'Password', p_c: float) -> Tuple['Password', 'Password']:
        child_1 = Password(self._char_list, self._goal_hash, self._hash_func)
        child_2 = Password(other._char_list, other._goal_hash, other._hash_func)
        min_length = min(len(self._char_list), len(other._char_list))
        for i in range(min_length):
            if random.random() <= p_c:
                tmp = child_2._char_list[i]
                child_2._char_list[i] = child_1._char_list[i]
                child_1._char_list[i] = tmp
        return child_1, child_2

    def mutate(self, p_m: float):
        for i in range(len(self._char_list)):
            if random.random() <= p_m:
                self._char_list[i] = chr(random.randint(97, 122))


def guess_password(password_hash: int, min_fitness: float, num_chars: int, hash_func: Callable[[str], int]) -> str:
    """
    Attempts to find the string whose hash matches the given hash via a genetic algorithm.

    :param password_hash: The hash for the original password
    :param min_fitness: The minimum fitness permitted for the best individual in the final generation
    :param num_chars: How many characters to put in the generated passwords
    :param hash_func: The function to be used for hashing; it should take in a string and output its hash
    :return: The optimal result produced by the genetic algorithm
    """
    def gen_passwords():
        population = []
        for i in range(500):
            char_list = []
            for j in range(num_chars):
                char_list.append(chr(random.randint(97, 122)))
            population.append(Password(char_list, password_hash, hash_func))
        return population

    best_gen = genetic_algorithm.run(gen_passwords, min_fitness, 0.7, 0.04, 0.0)
    best_pass = best_gen[0]
    for pw in best_gen:
        if pw.get_fitness() > best_pass.get_fitness():
            best_pass = pw

    return str(best_pass)
