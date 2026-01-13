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
    if use_nearest_neighbor == False:
        cities = []
        for i in range(num_bits):
            cities.append(i)
        population = [permutation(cities) for _ in range(pop_size)]
    else:
        for i in range(pop_size):
            population.append(nearest_neighbor_heuristic(num_nearest_neighbors_count))
    return population

def nearest_neighbor_heuristic(num_candidates):
    solution = []
    cities_to_visit = []
    for i in range(len(distance_matrix)):
        cities_to_visit.append(i)
    
    chosen_city = randint(len(distance_matrix))
    solution.append(chosen_city)
    cities_to_visit.remove(chosen_city)

    while len(solution) < len(distance_matrix):
        candidates = []
        counter = 0
        while len(candidates) < num_candidates and len(candidates) < len(cities_to_visit):
            candidates.append(cities_to_visit[counter])
            counter += 1
        
        furthest_index = 0
        for i in range(len(candidates)):
            if distance_matrix[solution[-1]][candidates[i]] > distance_matrix[solution[-1]][candidates[furthest_index]]:
                furthest_index = i
        
        while counter < len(cities_to_visit):
            if distance_matrix[solution[-1]][cities_to_visit[counter]] < distance_matrix[solution[-1]][candidates[furthest_index]]:
                candidates[furthest_index] = cities_to_visit[counter]
                furthest_index = 0
                for i in range(len(candidates)):
                    if distance_matrix[solution[-1]][candidates[i]] > distance_matrix[solution[-1]][candidates[furthest_index]]:
                        furthest_index = i
            counter += 1
        
        chosen = randint(0, len(candidates))
        solution.append(candidates[chosen])
        cities_to_visit.remove(candidates[chosen])
    
    return solution

def selection(population, fitness_values, tournament_size):
    chosen_index = randint(len(population))
    for i in randint(0, len(population), tournament_size-1):
        if util.is_better(fitness_values[i], fitness_values[chosen_index]):
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

def mutation(chromosome, mutation_prob):
    if rand() < mutation_prob:
        point1 = randint(0, len(chromosome))
        point2 = randint(0, len(chromosome))
        chromosome[point1], chromosome[point2] = (chromosome[point2], chromosome[point1])

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

    current_time = time.time()

    while generation < max_generations and current_time - start_time < max_time:
        generation += 1
        selected_parents = [selection(population, fitness_values, tournament_size) for _ in range(pop_size)]
        
        offspring = list()
        if elitism == True:
            offspring.append(population[best_chromosome_idx])
        
        for i in range(0, pop_size, 2):
            p1, p2 = selected_parents[i], selected_parents[i+1]
            for child in crossover(p1, p2, crossover_prob):
                mutation(child, mutation_prob)
                if len(offspring) < pop_size:
                    offspring.append(child)
        
        population = offspring
        fitness_values = [objective_func(c) for c in population]
        
        best_chromosome_idx, best_fitness, avg_fitness, worst_fitness = get_stats(fitness_values)
        print(">Generation %d: Worst: %.3f Average: %.3f Best: %.3f" % (generation, worst_fitness, avg_fitness, best_fitness))
        evolution_history.append([best_fitness, avg_fitness, worst_fitness])
        
        current_time = time.time()

    return [population[best_chromosome_idx], fitness_values[best_chromosome_idx], evolution_history]



# Values GA
# filename="instanciasTSP/eil51.tsp"
import json
with open("data/generated/berlin52_noise0.1_asym0.05.json") as f:
    instance = json.load(f)

distance_matrix = instance["distance_matrix"]

use_nearest_neighbor = True
num_nearest_neighbors_count = 5

pop_size = 100
tournament_size = 4
crossover_prob = 0.8
mutation_prob = 0.2
elitism = True

max_time = 30
max_generations = 200000





# Program
# coordinates = []
# util.read_tsp_file(filename, coordinates)
# distance_matrix = []
# create_distance_matrix(coordinates, distance_matrix)

start_time = time.time()
best_solution, best_fitness_value, evolution_data = genetic_algorithm(calculate_total_distance, len(distance_matrix), max_generations, pop_size, crossover_prob, mutation_prob)
end_time = time.time()

print('Execution finished! Total execution time: %f seconds' % (end_time - start_time))
print('Best solution and its fitness:')
print('f(%s) = %f' % (best_solution, best_fitness_value))
util.plot_results(evolution_data)