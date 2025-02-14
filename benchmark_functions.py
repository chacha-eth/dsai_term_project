import numpy as np

def rastrigin_function():
    def benchmark(genome):
        return 10 * len(genome) + sum([(x ** 2 - 10 * np.cos(2 * np.pi * x)) for x in genome])
    limits = {f"gene_{i}": (-5.12, 5.12) for i in range(10)}

    return benchmark, limits
def sphere_function():
    def benchmark(genome):
        return sum(x ** 2 for x in genome)
    limits = {f"gene_{i}": (-10, 10) for i in range(10)}
    return benchmark, limits

def p_peaks_function(num_peaks=5, genome_length=10):
    # Generate random peaks (each peak is a binary vector)
    peaks = [np.random.randint(0, 2, genome_length) for _ in range(num_peaks)]
    def benchmark(genome):
        """P-Peaks function: Measures closeness of genome to the nearest peak."""
        genome = np.array(genome)
        max_similarity = max(np.sum(genome == peak) for peak in peaks)
        return genome_length - max_similarity  # The goal is to minimize distance to a peak
    limits = {f"gene_{i}": (0, 1) for i in range(genome_length)}

    return benchmark, limits
def vrp_function(num_customers=10, num_vehicles=3, depot_index=0):
    # Generate a random distance matrix (symmetric)
    np.random.seed(42)
    distance_matrix = np.random.randint(10, 100, size=(num_customers + 1, num_customers + 1))
    np.fill_diagonal(distance_matrix, 0)  # Distance from a location to itself is zero

    def benchmark(routes):
        """Evaluates a VRP solution by computing total route cost."""
        total_cost = 0
        # Iterate through each vehicle route
        for route in routes:
            cost = 0
            prev_location = depot_index  # Vehicles start from the depot
            for customer in route:
                cost += distance_matrix[prev_location, customer]
                prev_location = customer
            cost += distance_matrix[prev_location, depot_index]  # Return to depot
            total_cost += cost
        
        return total_cost  # Minimize total route cost
    # Define search space limits (each customer can be assigned to any vehicle)
    limits = {f"customer_{i}": (0, num_vehicles - 1) for i in range(1, num_customers + 1)}

    return benchmark, limits