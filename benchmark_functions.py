import numpy as np
from typing import Dict
def rastrigin_function():
    def benchmark(params: Dict[str, float]) -> float:
        return 10 * len(params) + sum((x ** 2 - 10 * np.cos(2 * np.pi * x)) for x in params.values())
    limits = {f"gene_{i}": (-5.12, 5.12) for i in range(10)}
    return benchmark, limits


    return benchmark, limits
def sphere_function():
    def benchmark(params: Dict[str, float]) -> float:
        return sum(x ** 2 for x in params.values())  # Extract values and compute sum of squares
    # Define search space limits for each parameter
    limits = {f"gene_{i}": (-10, 10) for i in range(10)}  # 10D search space

    return benchmark, limits

def p_peaks_function(num_peaks=5, genome_length=10):
    peaks = [np.random.randint(0, 2, genome_length) for _ in range(num_peaks)]
    def benchmark(params: Dict[str, float]) -> float:
        genome = np.array(list(params.values()))
        max_similarity = max(np.sum(genome == peak) for peak in peaks)
        return genome_length - max_similarity  # The goal is to minimize distance to a peak
    limits = {f"gene_{i}": (0, 1) for i in range(genome_length)}
    
    return benchmark, limits

def vrp_function(num_customers=10, num_vehicles=3, depot_index=0):
    np.random.seed(42)
    distance_matrix = np.random.randint(10, 100, size=(num_customers + 1, num_customers + 1))
    np.fill_diagonal(distance_matrix, 0)  # Distance from a location to itself is zero
    def benchmark(params: Dict[str, float]) -> float:
        genome = np.array(list(params.values()), dtype=int)
        # Reconstruct routes from the genome assignment
        routes = {i: [] for i in range(num_vehicles)}
        for i, vehicle in enumerate(genome, start=1):
            routes[vehicle].append(i)  # Customers are indexed from 1
        total_cost = 0
        for route in routes.values():
            cost = 0
            prev_location = depot_index  # Vehicles start from the depot
            for customer in route:
                cost += distance_matrix[prev_location, customer]
                prev_location = customer
            cost += distance_matrix[prev_location, depot_index]  # Return to depot
            total_cost += cost

        return total_cost  # Minimize total route cost

    limits = {f"customer_{i}": (0, num_vehicles - 1) for i in range(1, num_customers + 1)}

    return benchmark, limits

   