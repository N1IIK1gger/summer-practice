import csv
from collections import defaultdict
from typing import Dict, List

import matplotlib.pyplot as plt

interp_filter = "CPython 3.13.7"
os_filter = "Windows"

def load_results(path: str = "results.csv") -> List[Dict[str, str]]:
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def plot_time_by_n_for_alg(rows: List[Dict[str, str]], os_filter: str, interp_filter: str):
    data = defaultdict(lambda: defaultdict(list))

    for r in rows:
        if r["os"] != os_filter or r["interpreter"] != interp_filter:
            continue
        if r["data_type"] != "Random":
            continue

        alg = r["algorithm"]
        n = int(r["n"])
        t = float(r["time_ms"])

        data[alg]["n"].append(n)
        data[alg]["t"].append(t)

    plt.figure(figsize=(10, 6))
    for alg, vals in data.items():
        plt.plot(vals["n"], vals["t"], marker="o", label=alg)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("N (log scale)")
    plt.ylabel("Time, ms (log scale)")
    plt.title(f"Time vs N (Random data) — {os_filter}, {interp_filter}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("img/time_vs_n_random.png")


def plot_memory_by_n_for_alg(rows: List[Dict[str, str]], os_filter: str, interp_filter: str):
    data = defaultdict(lambda: defaultdict(list))

    for r in rows:
        if r["os"] != os_filter or r["interpreter"] != interp_filter:
            continue
        if r["data_type"] != "Random":
            continue

        alg = r["algorithm"]
        n = int(r["n"])
        m = float(r["mem_kb"])

        data[alg]["n"].append(n)
        data[alg]["m"].append(m)

    plt.figure(figsize=(10, 6))
    for alg, vals in data.items():
        plt.plot(vals["n"], vals["m"], marker="o", label=alg)

    plt.xscale("log")
    plt.xlabel("N (log scale)")
    plt.ylabel("Peak memory, KB")
    plt.title(f"Memory vs N (Random data) — {os_filter}, {interp_filter}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("img/mem_vs_n_random.png")


def main():
    rows = load_results("D:/Прога/Practica/results.csv")

    # ✔ Исправлено: теперь совпадает с CSV
    os_filter = "Windows"
    interp_filter = "CPython 3.13.7"

    plot_time_by_n_for_alg(rows, os_filter, interp_filter)
    plot_memory_by_n_for_alg(rows, os_filter, interp_filter)


if __name__ == "__main__":
    main()