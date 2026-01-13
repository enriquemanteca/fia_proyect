import random

def add_noise(matrix, sigma=0.1, seed=2026):
    random.seed(seed)
    n = len(matrix)
    noisy = [[0.0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                epsilon = random.gauss(0, sigma)
                noisy[i][j] = max(0.0001, matrix[i][j] * (1 + epsilon))
    return noisy
