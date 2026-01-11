from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
import matplotlib.pyplot as plt

def read_tsp_file(filename, coordinates):
    f = open(filename, "r")
    f.readline()
    f.readline()
    f.readline()
    numlines = int(f.readline().split()[1])
    f.readline()
    f.readline()
    for i in range(numlines):
        line = f.readline()
        parts = line.split()
        coord = [float(parts[1]), float(parts[2])]
        coordinates.append(coord)

def is_better(a, b):
    return a < b



def plot_results(evolution_history):
    plt.plot(evolution_history)
    plt.legend(["Best", "Average", "Worst"])
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Evolution")
    plt.show()
