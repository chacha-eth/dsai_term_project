import numpy as np

def vrp_fitness(route, distance_matrix):
    return np.sum([distance_matrix[route[i], route[i+1]] for i in range(len(route)-1)])

def generate_vrp_problem(num_customers=50):
    distance_matrix = np.random.rand(num_customers, num_customers) * 100  # Random distances
    np.fill_diagonal(distance_matrix, 0)  # No self-loops
    return lambda route: vrp_fitness(route, distance_matrix)
