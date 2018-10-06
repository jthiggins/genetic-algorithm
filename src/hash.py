def simple_hash(s: str) -> int:
    """
    Hash a given string using a basic hashing algorithm.

    :param s: The string to hash
    :return: The hash of the given string
    """
    i, exp = 0, 0
    for c in s:
        i += ord(c) * (10**exp)
        exp += 1

    return i
