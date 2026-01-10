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

def selection(population, fitness_values, tournament_size):
    chosen_index = randint(len(population))
    for i in randint(0, len(population), tournament_size-1):
        if is_better(fitness_values[i], fitness_values[chosen_index]):
            chosen_index = i
    return population[chosen_index]

def crossover(p1, p2, crossover_prob):
    c1, c2 = p1.copy(), p2.copy()
    if rand() < crossover_prob:
        point_min = randint(0, len(p1))
        point_max = randint(0, len(p1))
        while point_min == point_max:
            point_max = randint(0, len(p1))
        if point_min > point_max:
            point_min, point_max = point_max, point_min
        
        pointer_p1 = 0
        pointer_p2 = 0
        
        for i in range(len(p1)):
            if i < point_min or i > point_max:
                while p2[pointer_p2] in c1[point_min:point_max+1]:
                    pointer_p2 += 1
                c1[i] = p2[pointer_p2]
                pointer_p2 += 1
                
                while p1[pointer_p1] in c2[point_min:point_max+1]:
                    pointer_p1 += 1
                c2[i] = p1[pointer_p1]
                pointer_p1 += 1
    return [c1, c2]


def get_stats(fitness_values):
    best_chromosome_idx, best_fitness, worst_fitness = 0, fitness_values[0], fitness_values[0]
    avg_fitness = 0
    for i in range(pop_size):
        avg_fitness += fitness_values[i]
        if util.is_better(fitness_values[i], best_fitness):
            best_chromosome_idx, best_fitness = i, fitness_values[i]
        if util.is_better(worst_fitness, fitness_values[i]):
            worst_fitness = fitness_values[i]
    avg_fitness = avg_fitness / pop_size
    return [best_chromosome_idx, best_fitness, avg_fitness, worst_fitness]

def genetic_algorithm(objective_func, num_bits, max_generations, pop_size, crossover_prob, mutation_prob):
    generation = 0
    evolution_history = []

    population = create_initial_population(pop_size, num_bits)
    fitness_values = [objective_func(c) for c in population]

    best_chromosome_idx, best_fitness, avg_fitness, worst_fitness = get_stats(fitness_values)
    print(">Generation %d: Worst: %.3f Average: %.3f Best: %.3f" % (generation, worst_fitness, avg_fitness, best_fitness))
    evolution_history.append([best_fitness, avg_fitness, worst_fitness])





# Values GA
filename="D:/Ingenieria de Datos/Erasmus/Fondamenti/instanciasTSP/eil51.tsp"

pop_size = 100
tournament_size = 4
crossover_prob = 0.9
mutation_prob = 0.1
elitism = True

max_time = 60
max_generations = 200





# Program
coordinates = []
util.read_tsp_file(filename, coordinates)
distance_matrix = []
create_distance_matrix(coordinates, distance_matrix)