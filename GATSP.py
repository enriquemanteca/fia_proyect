from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
import matplotlib.pyplot as plt
import time
import utils as util


def calculate_total_distance(route):
    total_distance = sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
    total_distance = total_distance + distance_matrix[route[len(route)-1]][route[0]]
    return total_distance

def create_distance_matrix(coords, matrix):
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            dist = ((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2)**(0.5)
            row.append(dist)
        matrix.append(row)

def create_initial_population(pop_size, num_bits):
    population = []
    cities = []
    for i in range(num_bits):
        cities.append(i)
    population = [permutation(cities) for _ in range(pop_size)]
    return population



def genetic_algorithm(objective_func, num_bits, max_generations, pop_size, crossover_prob, mutation_prob):
    generation = 0
    population = create_initial_population(pop_size, num_bits)
    fitness_values = [objective_func(c) for c in population]


filename="D:/Ingenieria de Datos/Erasmus/Fondamenti/instanciasTSP/eil51.tsp"

coordinates = []
util.read_tsp_file(filename, coordinates)
distance_matrix = []
create_distance_matrix(coordinates, distance_matrix)