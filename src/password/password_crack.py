from typing import Callable
import genetic_algorithm, random


class Password(genetic_algorithm.Individual):
    def __init__(self, char_list: list, goal_hash: int, hash_func: Callable[[str], int]):
        self._char_list = char_list
        self._goal_hash = goal_hash
        self._hash_func = hash_func

    def __str__(self):
        return "".join(self._char_list)

    def get_fitness(self) -> float:
        diff = abs(self._hash_func(str(self)) - self._goal_hash)
        if diff == 0:
            return 1
        return 1/(diff**10)

    def crossover(self, other: 'Password', p_c: float):
        min_length = min(len(self._char_list), len(other._char_list))
        for i in range(min_length):
            if random.random() <= p_c:
                tmp = other._char_list[i]
                other._char_list[i] = self._char_list[i]
                self._char_list[i] = tmp

    def mutate(self, p_m: float):
        for i in range(len(self._char_list)):
            if random.random() <= p_m:
                self._char_list[i] = chr(random.randint(97, 122))


def attempt_crack(password_hash: int, num_iterations: int, num_chars: int, hash_func: Callable[[str], int]) -> str:
    """
    Attempts to find the string whose hash matches the given hash via a genetic algorithm.

    :param password_hash: The hash for the original password
    :param num_iterations: How many iterations the genetic algorithm should run
    :param num_chars: How many characters to put in the generated passwords
    :param hash_func: The function to be used for hashing; it should take in a string and output its hash
    :return: The optimal result produced by the genetic algorithm
    """
    def gen_passwords():
        population = []
        for i in range(1000):
            char_list = []
            for j in range(num_chars):
                char_list.append(chr(random.randint(97, 122)))
            population.append(Password(char_list, password_hash, hash_func))
        return population

    best_gen = genetic_algorithm.run(gen_passwords, num_iterations, 0.6, 0.04)
    best_pass = best_gen[0]
    for pw in best_gen:
        if pw.get_fitness() > best_pass.get_fitness():
            best_pass = pw

    return str(best_pass)
