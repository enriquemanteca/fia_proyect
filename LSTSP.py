from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
from numpy import exp
import time
import utils as util


def calculate_total_distance(route):
    total_distance = sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
    total_distance = total_distance + distance_matrix[route[len(route)-1]][route[0]]

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

def create_initial_solution():
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
        while len(candidates) < num_nearest_neighbors and len(candidates) < len(cities_to_visit):
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

swap_range=60
distance_marix=[]