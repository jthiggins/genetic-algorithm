from typing import Callable, Tuple
import genetic_algorithm
import random
import copy


class Password(genetic_algorithm.Individual):
    def __init__(self, char_list: list, goal_hash: int, hash_func: Callable[[str], int]):
        self._char_list = char_list
        self._goal_hash = goal_hash
        self._hash_func = hash_func
        self._fitness = None

    def __str__(self):
        return "".join(self._char_list)

    def clone(self):
        return Password(copy.copy(self._char_list), copy.copy(self._goal_hash), copy.copy(self._hash_func))

    def get_fitness(self) -> float:
        if self._fitness is not None:
            return self._fitness
        diff = abs(self._hash_func(str(self)) - self._goal_hash)
        if diff == 0:
            self._fitness = 1
        elif diff == 1:
            self._fitness = 0.9999
        else:
            self._fitness = 1/diff
        return self._fitness

    def crossover(self, other: 'Password', p_c: float) -> Tuple['Password', 'Password']:
        child_1 = self.clone()
        child_2 = other.clone()
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
                if random.random() <= 0.5:
                    self._char_list[i] = chr(random.randint(65, 90))
                else:
                    self._char_list[i] = chr(random.randint(97, 122))


def guess_password(password_hash: int, num_chars: int, hash_func: Callable[[str], int]) -> str:
    """
    Attempts to find the string whose hash matches the given hash via a genetic algorithm.

    :param password_hash: The hash for the original password
    :param num_chars: How many characters to put in the generated passwords
    :param hash_func: The function to be used for hashing; it should take in a string and output its hash
    :return: The optimal result produced by the genetic algorithm
    """
    def gen_passwords():
        population = []
        for i in range(500):
            char_list = []
            for j in range(num_chars):
                if random.random() <= 0.5:
                    char_list.append(chr(random.randint(65, 90)))
                else:
                    char_list.append(chr(random.randint(97, 122)))
            population.append(Password(char_list, password_hash, hash_func))
        return population

    best_pass = genetic_algorithm.run(gen_passwords, 0.7, 0.04, 0.6)

    return str(best_pass)
