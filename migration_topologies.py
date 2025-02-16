import numpy as np
def fully_connected_topology(num_islands, num_migrants):
    migration_topology = num_migrants * np.ones((num_islands, num_islands), dtype=int)
    np.fill_diagonal(migration_topology, 0)  # No self-migration
    return migration_topology

def bidirectional_ring_topology(num_islands, num_migrants):
    migration_topology = np.zeros((num_islands, num_islands), dtype=int)
    for i in range(num_islands):
        migration_topology[i, (i - 1) % num_islands] = num_migrants  # Left neighbor
        migration_topology[i, (i + 1) % num_islands] = num_migrants  # Right neighbor
    return migration_topology

def unidirectional_ring_topology(num_islands, num_migrants):
    migration_topology = np.zeros((num_islands, num_islands), dtype=int)
    for i in range(num_islands - 1):
        migration_topology[i, i + 1] = num_migrants  # Forward migration only
    migration_topology[num_islands - 1, 0] = num_migrants  # Last island to first
    return migration_topology

def star_topology(num_islands, num_migrants):
    migration_topology = np.zeros((num_islands, num_islands), dtype=int)
    for i in range(num_islands - 1):
        migration_topology[i, i + 1] = num_migrants  # Forward migration
    for i in range(1, num_islands):
        migration_topology[i, 0] = num_migrants  # All islands send to Island 0
    return migration_topology


