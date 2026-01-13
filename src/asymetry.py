import random

def add_asymetry(matrix, delta=0.05, seed=2026):
    random.seed(seed)
    n = len(matrix)
    asym = [[0.0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                alpha = random.uniform(-delta, delta)
                asym[i][j] = matrix[i][j] * (1 + alpha)
    return asym
