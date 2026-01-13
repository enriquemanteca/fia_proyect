import random
from distance import build_distance_matrix
from noise import add_noise
from asymetry import add_asymetry
import json
from tsplib_reader import read_tsplib

def generate_cities(n, seed=2026, size=100):
    random.seed(seed)
    cities = []
    for _ in range(n):
        x = random.uniform(0, size)
        y = random.uniform(0, size)
        cities.append((x, y))
    return cities

def generate_instance(n, sigma=0.1, delta=0.05, seed=2026):
    cities = generate_cities(n, seed)
    base = build_distance_matrix(cities)
    noisy = add_noise(base, sigma, seed)
    final = add_asymetry(noisy, delta, seed)

    return {
        "cities": cities,
        "distance_matrix": final
    }

def generate_instance_from_tsplib(filepath, sigma=0.1, delta=0.05, seed=2026):
    cities = read_tsplib(filepath)
    base_matrix = build_distance_matrix(cities)
    noisy_matrix = add_noise(base_matrix, sigma, seed)
    final_matrix = add_asymetry(noisy_matrix, delta, seed)

    return {
        "cities": cities,
        "distance_matrix": final_matrix
    }

def save_instance(instance, filename):
    with open(filename, "w") as f:
        json.dump(instance, f, indent=2)

if __name__ == "__main__":
    sizes = [20, 50, 100]
    sigmas = [0.0, 0.1]
    deltas = [0.0, 0.05]

    for n in sizes:
        for s in sigmas:
            for d in deltas:
                instance = generate_instance(n, s, d, seed=2026)
                filename = f"data/generated/tsp_{n}_noise{s}_asym{d}.json"
                save_instance(instance, filename)
                print(f"Generated {filename}")

    tsplib_files = [
        "data/tsplib/ulysses22.tsp",
        "data/tsplib/berlin52.tsp",
        "data/tsplib/kroA100.tsp"
    ]

    for path in tsplib_files:
        base_name = path.split("/")[-1].replace(".tsp", "")
        for s in sigmas:
            for d in deltas:
                inst = generate_instance_from_tsplib(path, s, d, seed=2026)
                filename = f"data/generated/{base_name}_noise{s}_asym{d}.json"
                save_instance(inst, filename)
                print(f"Generated {filename}")
