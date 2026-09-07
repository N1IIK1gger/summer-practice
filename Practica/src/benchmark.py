import csv
import platform
import sys
from time import perf_counter
import tracemalloc
from typing import Callable, List, Dict

from algorithms import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    quick_sort,
    merge_sort,
    heap_sort,
    counting_sort,
    radix_sort,
    bucket_sort,
)
from datasets import SIZES, DATA_GENERATORS



OS_NAME = platform.system()          
INTERPRETER = f"CPython {platform.python_version()}"  


AlgorithmFunc = Callable[[List[int]], List[int]]


ALGORITHMS: Dict[str, AlgorithmFunc] = {
    "Bubble": bubble_sort,
    "Selection": selection_sort,
    "Insertion": insertion_sort,
    "Quick": quick_sort,
    "Merge": merge_sort,
    "Heap": heap_sort,
    "Counting": counting_sort,
    "Radix": radix_sort,
    "Bucket": bucket_sort,
    "Built-in sorted": lambda arr: sorted(arr),
    "Built-in list.sort": lambda arr: _list_sort_wrapper(arr),
}


def _list_sort_wrapper(arr: List[int]) -> List[int]:
    a = arr.copy()
    a.sort()
    return a


def benchmark_algorithm(
    name: str,
    func: AlgorithmFunc,
    data: List[int],
) -> Dict[str, float]:
    tracemalloc.start()
    start_time = perf_counter()
    _ = func(data)
    end_time = perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time_ms = (end_time - start_time) * 1000.0
    mem_kb = peak / 1024.0
    return {"time_ms": time_ms, "mem_kb": mem_kb}


def main(output_csv: str = "results.csv") -> None:
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "os",
                "interpreter",
                "algorithm",
                "data_type",
                "n",
                "time_ms",
                "mem_kb",
            ]
        )

        for data_type, gen in DATA_GENERATORS.items():
            for n in SIZES:
                print(f"Generating data: type={data_type}, n={n}")
                data = gen(n)
                for alg_name, alg_func in ALGORITHMS.items():
                      
                      if n > 5000 and alg_name in ["Bubble", "Selection", "Insertion"]:
                        print(f"Skipping {alg_name} for n={n} (too slow)")
                        continue

                      if data_type == "Sorted" and alg_name == "Quick":
                       print(f"Skipping Quick Sort on Sorted data (worst case)")
                       continue

                      if alg_name == "Quick" and data_type in ["Sorted", "Reversed", "Almost Sorted"]:
                       print(f"Skipping Quick Sort on {data_type} (worst case)")
                       continue

                      if n == 1000000 and alg_name in ["Counting", "Radix", "Bucket"]:
                       print(f"Skipping {alg_name} for n={n} (too memory-heavy)")
                       continue
                      
                      print(f"Benchmarking {alg_name} on {data_type}, n={n}")
                      result = benchmark_algorithm(alg_name, alg_func, data)
                      writer.writerow(
                        [
                            OS_NAME,
                            INTERPRETER,
                            alg_name,
                            data_type,
                            n,
                            f"{result['time_ms']:.3f}",
                            f"{result['mem_kb']:.3f}",
                        ]
                       )


if __name__ == "__main__":
    out = "results.csv"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    main(out)