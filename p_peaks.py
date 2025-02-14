import numpy as np

def p_peaks_fitness(individual, peaks):
    """Compute the fitness as the minimum Hamming distance to a peak."""
    return min([np.sum(np.abs(individual - peak)) for peak in peaks])

def generate_p_peaks_problem(num_peaks=20, genome_length=100):
    """Generate a P-PEAKS problem with random peak positions."""
    peaks = np.random.randint(0, 2, (num_peaks, genome_length))  # Random peaks
    return lambda individual: p_peaks_fitness(individual, peaks)
