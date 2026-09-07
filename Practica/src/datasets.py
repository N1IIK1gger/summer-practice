import random
from typing import List


SIZES = [10, 500, 1000, 50000, 1000000]


def generate_random(n: int) -> List[int]:
    return [random.randint(0, 10**6) for _ in range(n)]


def generate_sorted(n: int) -> List[int]:
    return sorted(generate_random(n))


def generate_reversed(n: int) -> List[int]:
    return list(reversed(generate_sorted(n)))


def generate_almost_sorted(n: int, shuffle_ratio: float = 0.05) -> List[int]:
    arr = generate_sorted(n)
    k = int(n * shuffle_ratio)
    indices = random.sample(range(n), k)
    for i in indices:
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


DATA_GENERATORS = {
    "Random": generate_random,
    "Sorted": generate_sorted,
    "Reversed": generate_reversed,
    "Almost Sorted": generate_almost_sorted,
}