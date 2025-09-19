import sys
import math
import random
from typing import List, Tuple
import numpy as np


def round_to_nearest_integer(d: float) -> int:
    return int(math.floor(d + 0.5))


def read_file(filename: str) -> Tuple[List[int], np.ndarray]:
    """
    Reads the TSP file with format:
      n
      Id_0 x_0 y_0
      ...
      Id_{n-1} x_{n-1} y_{n-1}
    Returns:
      - ids: list of node IDs in the given order
      - coords: numpy array of shape (n, 2) with floats
    """
    ids: List[int] = []
    coords_list: List[Tuple[float, float]] = []
    with open(filename, "r", encoding="utf-8") as f:
        # Skip possible BOM/spaces and read first non-empty line as n
        first = ""
        while first.strip() == "":
            first = f.readline()
            if first == "":
                raise ValueError("Empty file or missing node count on first line.")
        n = int(first.strip())
        # Read n lines with id, x, y
        for _ in range(n):
            line = f.readline()
            if line is None or line.strip() == "":
                raise ValueError("Unexpected end of file while reading coordinates.")
            parts = line.strip().split()
            if len(parts) < 3:
                raise ValueError(f"Invalid coordinate line: {line.strip()}")
            node_id = int(float(parts[0]))
            x = float(parts[1])
            y = float(parts[2])
            ids.append(node_id)
            coords_list.append((x, y))
    coords = np.array(coords_list, dtype=np.float64)
    return ids, coords


def build_distance_matrix(coords: np.ndarray) -> np.ndarray:
    """
    Builds an integer-rounded Euclidean distance matrix using:
      w(u, v) = nint( sqrt( (x_u - x_v)^2 + (y_u - y_v)^2 ) )
    """
    # Pairwise squared distances via broadcasting
    diff = coords[:, None, :] - coords[None, :, :]
    sq = diff ** 2
    d = np.sqrt(sq.sum(axis=2))
    dm = np.floor(d + 0.5).astype(np.int64)
    # Ensure diagonal is zero
    np.fill_diagonal(dm, 0)
    return dm

def tour_length(tour: List[int], dm: np.ndarray) -> int:
    total = 0
    n = len(tour)
    for i in range(n - 1):
        total += int(dm[tour[i], tour[i + 1]])
    total += int(dm[tour[-1], tour[0]])
    return total

def nearest_neighbor_insertion(dm: np.ndarray) -> List[int]:
    """
    Start with a randomly selected city and repeatedly append
    the closest unvisited city to the last city chosen.
    """
    n = dm.shape[0]
    start = random.randrange(n)
    unvisited = set(range(n))
    unvisited.remove(start)
    tour = [start]
    current = start
    while unvisited:
        # Find nearest city to current among unvisited
        nearest = min(unvisited, key=lambda c: dm[current, c])
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    return tour


def alternative_insertion(dm: np.ndarray) -> List[int]:
    """
    Start with a randomly selected city.
    Repeatedly choose a random unvisited city and insert it after the city in the
    current tour that is closest to random_city. If multiple are tied, insert after the first encountered.
    """
    number_of_entries = dm.shape[0]
    start = random.randrange(number_of_entries)
    unvisited = list(range(number_of_entries))
    unvisited.remove(start)
    tour = [start]
    while unvisited:
        random_index = random.randrange(len(unvisited))
        random_city = unvisited.pop(random_index)
        closest_city = tour[0]
        best_dist = dm[closest_city, random_city]

        for city in tour[1:]:
            distance = dm[city, random_city]
            if distance < best_dist:
                best_dist = distance
                closest_city = city

        # Insert random_city after the first occurrence of closest_city in the tour
        i = tour.index(closest_city)
        tour.insert(i + 1, random_city)
    return tour


def random_full_tour(n: int) -> List[int]:
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def run_algorithm_multiple(
    algo_name: str,
    algo_func,
    dm: np.ndarray,
    id_map: List[int],
    n_runs: int,
) -> None:
    """
    Runs the given algorithm n_runs times, prints:
      best objective value, average objective value, and the route of the best solution (as IDs).
    """
    best_len = None
    best_tour = None
    total_len = 0
    for _ in range(n_runs):
        if algo_name == "RANDOM":
            tour = random_full_tour(dm.shape[0])
        else:
            tour = algo_func(dm)
        length = tour_length(tour, dm)
        total_len += length
        if best_len is None or length < best_len:
            best_len = length
            best_tour = tour
    avg_len = total_len / n_runs if n_runs > 0 else float("nan")
    # Map internal indices to original IDs
    best_route_ids = [id_map[i] for i in best_tour]

    print(f"{algo_name} BEST: {best_len}")
    print(f"{algo_name} AVG: {avg_len:.4f}")
    print("ROUTE:", " ".join(str(x) for x in best_route_ids))


def main():
    if len(sys.argv) < 3:
        print("Usage: python tsp.py <input filename> <nRuns>")
        sys.exit(1)
    filename = sys.argv[1]
    try:
        n_runs = int(sys.argv[2])
    except Exception:
        print("nRuns must be an integer")
        sys.exit(1)

    # Read data and build distance matrix
    ids, coords = read_file(filename)
    dm = build_distance_matrix(coords)

    run_algorithm_multiple("NEAREST_NEIGHBOR", nearest_neighbor_insertion, dm, ids, n_runs)
    run_algorithm_multiple("ALTERNATIVE_INSERTION", alternative_insertion, dm, ids, n_runs)
    run_algorithm_multiple("RANDOM", None, dm, ids, n_runs)


if __name__ == '__main__':
    main()