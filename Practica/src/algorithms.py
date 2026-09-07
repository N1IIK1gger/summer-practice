from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def selection_sort(arr: List[int]) -> List[int]:
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr: List[int]) -> List[int]:
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def quick_sort(arr: List[int]) -> List[int]:
    a = arr.copy()
    _quick_sort(a, 0, len(a) - 1)
    return a


def _quick_sort(a: List[int], low: int, high: int) -> None:
    if low < high:
        p = _partition(a, low, high)
        _quick_sort(a, low, p - 1)
        _quick_sort(a, p + 1, high)


def _partition(a: List[int], low: int, high: int) -> int:
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heap_sort(arr: List[int]) -> List[int]:
    a = arr.copy()
    n = len(a)

    def heapify(n_, i_):
        largest = i_
        l = 2 * i_ + 1
        r = 2 * i_ + 2

        if l < n_ and a[l] > a[largest]:
            largest = l
        if r < n_ and a[r] > a[largest]:
            largest = r
        if largest != i_:
            a[i_], a[largest] = a[largest], a[i_]
            heapify(n_, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        heapify(i, 0)
    return a


def counting_sort(arr: List[int]) -> List[int]:
    if not arr:
        return []
    a = arr.copy()
    min_val = min(a)
    max_val = max(a)
    k = max_val - min_val + 1
    count = [0] * k
    for x in a:
        count[x - min_val] += 1
    idx = 0
    for i, c in enumerate(count):
        for _ in range(c):
            a[idx] = i + min_val
            idx += 1
    return a


def radix_sort(arr: List[int]) -> List[int]:
    if not arr:
        return []
    # Для простоты считаем, что числа неотрицательные
    a = arr.copy()
    max_val = max(a)
    exp = 1
    while max_val // exp > 0:
        a = _counting_sort_by_digit(a, exp)
        exp *= 10
    return a


def _counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    return output


def bucket_sort(arr: List[int], bucket_size: int = 10) -> List[int]:
    if len(arr) == 0:
        return []
    a = arr.copy()
    min_val = min(a)
    max_val = max(a)
    bucket_count = (max_val - min_val) // bucket_size + 1
    buckets = [[] for _ in range(bucket_count)]
    for x in a:
        idx = (x - min_val) // bucket_size
        buckets[idx].append(x)
    result = []
    for b in buckets:
        # внутри ведём insertion sort
        result.extend(insertion_sort(b))
    return result