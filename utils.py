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




def plot_results(coordinates, route, evolution=[]):
    x = []
    y = []
    for i in route:
        x.append(coordinates[i][0])
        y.append(coordinates[i][1])
    
    plt.figure(figsize=(11, 5))
    
    plt.subplot(121)
    plt.plot(x, y, 'bo', markersize=4.0)
    
    a_scale = float(max(x)) / float(100)
    
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale, color='r', length_includes_head=True)
    
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width=a_scale, color='r', length_includes_head=True)
        
    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Best Route Found")
    
    plt.subplot(122)
    plt.plot(evolution)
    
    plt.legend("Best route")
        
    plt.ylabel("Fitness")
    plt.title("Evolution")
    plt.show()