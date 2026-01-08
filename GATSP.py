from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
import matplotlib.pyplot as plt
import time
import utils as util


def create_distance_matrix(coords, matrix):
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            dist = ((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2)**(0.5)
            row.append(dist)
        matrix.append(row)




filename="D:/Ingenieria de Datos/Erasmus/Fondamenti/instanciasTSP/eil51.tsp"

coordinates = []
util.read_tsp_file(filename, coordinates)
distance_matrix = []
create_distance_matrix(coordinates, distance_matrix)