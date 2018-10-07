from typing import Callable, Tuple
from threading import Timer
import _thread
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
                self._char_list[i] = get_pass_char()


def get_pass_char():
    """Get a random character for a password."""
    rnd = random.random()
    if rnd < 1/3:
        return chr(random.randint(48, 57))  # Digits
    elif rnd < 2/3:
        return chr(random.randint(65, 90))  # Uppercase letters
    else:
        return chr(random.randint(97, 122))  # Lowercase letters


def guess_password(password_hash: int, num_chars: int, hash_func: Callable[[str], int]) -> str:
    """Attempt to find the string whose hash matches the given hash via a genetic algorithm.

    :param password_hash: The hash for the original password
    :param num_chars: How many characters to put in the generated passwords
    :param hash_func: The function to be used for hashing; it should take in a string and output its hash
    :return: The optimal result produced by the genetic algorithm
    """
    def gen_passwords():
        """Generate a list of random passwords."""
        population = []
        for i in range(500):
            char_list = []
            for j in range(num_chars):
                char_list.append(get_pass_char())
            population.append(Password(char_list, password_hash, hash_func))
        return population

    # Uncomment the lines in main.py if you want to uncomment these
    #def time_out():
        #print("TIMEOUT ERROR: too much time has passed since beginning the reconstruction. This may have occurred "
              #"because you entered an improper password length.")
        #input("Press any key to exit.")
        #_thread.interrupt_main()

    #tmr = Timer(30.0, time_out)

    #tmr.start()
    best_pass = genetic_algorithm.run(gen_passwords, lambda best: best.get_fitness() < 1, 0.7, 0.04, 0.6)
    #tmr.cancel()

    return str(best_pass)
