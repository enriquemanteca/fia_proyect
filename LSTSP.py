from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
from numpy import exp
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

def create_initial_population(pop_size, num_bits):
    population = []
    if use_nearest_neighbor == False:
        cities = []
        for i in range(num_bits):
            cities.append(i)
        population = [permutation(cities) for _ in range(pop_size)]
    else:
        for i in range(pop_size):
            population.append(nearest_neighbor_heuristic(num_nearest_neighbors))
    return population


def swap_neighborhood(solution):
    neighbors = []
    swaps = []
    num_neighbors = 0
    for i in range(len(solution)-1):
        for j in range(i+1, i+swap_range+1):
            if j < len(solution):
                neighbors.append(solution.copy())
                neighbors[num_neighbors][i], neighbors[num_neighbors][j] = (neighbors[num_neighbors][j], neighbors[num_neighbors][i])
                num_neighbors += 1
                swaps.append([i, j])
    return neighbors, swaps

def steepest_descent_hill_climbing(objective_func, initial_solution, generate_neighbors):
    current_solution = initial_solution
    current_fitness = objective_func(current_solution)
    evolution_history = []
    
    improvement_found = True
    while improvement_found == True:
        evolution_history.append(current_fitness)
        improvement_found = False
        
        neighbors, swaps = generate_neighbors(current_solution)
        neighbors_fitness = []
        for i in range(len(neighbors)):
            neighbors_fitness.append(objective_func(neighbors[i]))
        
        best_neighbor_idx = 0
        best_neighbor_fitness = neighbors_fitness[0]
        for i in range(1, len(neighbors)):
            if util.is_better(neighbors_fitness[i], best_neighbor_fitness):
                best_neighbor_idx = i
                best_neighbor_fitness = neighbors_fitness[i]
        
        if util.is_better(best_neighbor_fitness, current_fitness):
            current_solution = neighbors[best_neighbor_idx]
            current_fitness = best_neighbor_fitness
            improvement_found = True

    return [current_solution, current_fitness, evolution_history]

def multi_start_local_search(objective_func, generate_neighbors):
    evolution_history = []
    best_fitness = 0
    iteration = 0
    current_time = time.time()
    
    while iteration < max_iterations and current_time - start_time < max_time_multistart:
        initial_solution = create_initial_population()
        initial_fitness = objective_func(initial_solution)
        
        local_optimum, improved_fitness, hill_climbing_evolution = steepest_descent_hill_climbing(objective_func, initial_solution, generate_neighbors)
        
        if iteration == 0 or util.is_better(improved_fitness, best_fitness):
            best_solution = local_optimum
            best_fitness = improved_fitness
            
        print('Iteration %d: Initial solution fitness %f, Improved solution fitness %f' % (iteration, initial_fitness, improved_fitness))
        iteration = iteration + 1
        evolution_history.append([best_fitness, improved_fitness])
        
        current_time = time.time()

    return [best_solution, best_fitness, evolution_history]

# Values LS
filename="instanciasTSP/eil51.tsp"

maximize=False

swap_range=60

use_nearest_neighbor = True

num_nearest_neighbors = 3

pop_size = 100
max_iterations = 20000
max_time_multistart = 15

coordinates = []
util.read_tsp_file(filename, coordinates)
distance_matrix = []
create_distance_matrix(coordinates, distance_matrix)

start_time = time.time()
best_solution, best_fitness_value, evolution_data = multi_start_local_search(calculate_total_distance, swap_neighborhood)
end_time = time.time()

print('Execution finished! Total execution time: %f seconds' % (end_time - start_time))
print('Best solution and its fitness:')
print('f(%s) = %f' % (best_solution, best_fitness_value))
util.plot_results(evolution_data)