from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
from numpy import exp

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