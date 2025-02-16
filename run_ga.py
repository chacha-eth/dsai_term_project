"""Simple island model example script."""

import pathlib
import random
import os
import numpy as np
from mpi4py import MPI
import argparse
import time
import csv
from propulate import Islands
from propulate.propagators import SelectMax, SelectMin
from propulate.utils import get_default_propagator, set_logger_config
from propulate.utils.benchmark_functions import (
    get_function_search_space,
    parse_arguments,
)
from migration_topologies import fully_connected_topology,bidirectional_ring_topology,unidirectional_ring_topology
from benchmark_functions import sphere_function,rastrigin_function,p_peaks_function,vrp_function

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    # Parse command-line arguments.
    config, _ = parse_arguments(comm)
    
    config.num_islands = 4  # Total number of islands
    config.num_migrants = 1  # Number of individuals migrating per event
    config.generations = 1024  # Run for 100 generations
    config.migration_probability = 0.5  # 50% probability of migration occurring
    config.pop_size = 256  # Population size per island
    config.crossover_probability = 0.8  # Crossover rate
    config.mutation_probability = 0.05  # Mutation rate
    config.random_init_probability = 0.1  # Random initialization probability
    config.logging_interval = 10  # Log every 10 generations
    config.verbosity = False  # Reduce verbosity for clean output
    config.top_n = 1  # Number of top solutions to summarize
    
    # save log and checkpoint files
    checkpoint_dir = "checkpoints"
    os.makedirs(checkpoint_dir, exist_ok=True) 
    config.checkpoint = checkpoint_dir  
   
   
    set_logger_config(
        level=config.logging_level,  
        log_file=f"{config.checkpoint}/{pathlib.Path(__file__).stem}.log", 
        log_to_stdout=True,  
        log_rank=False,  # Do not prepend MPI rank to logging messages.
        colors=True,  # Use colors.
    )

    rng = random.Random(config.seed + comm.rank)  # Separate random number generator for optimization.
  
    benchmark_function, limits = p_peaks_function(num_peaks=20, genome_length=100)
   
    propagator = get_default_propagator(  # Get default evolutionary operator.
        pop_size=config.pop_size,  # Breeding pool size
        limits=limits,  # Search-space limits
        crossover_prob=config.crossover_probability,  # Crossover probability
        mutation_prob=config.mutation_probability,  # Mutation probability
        random_init_prob=config.random_init_probability,  # Random-initialization probability
        rng=rng,  # Separate random number generator for Propulate optimization
    )

    topology="fully_connected"
    if topology == "fully_connected":
        migration_topology = fully_connected_topology(config.num_islands, config.num_migrants)
    elif topology == "bidirection_ring":
        migration_topology = bidirectional_ring_topology(config.num_islands, config.num_migrants)
    elif topology == "unidirection_ring":
        migration_topology = unidirectional_ring_topology(config.num_islands, config.num_migrants)
    np.fill_diagonal(migration_topology, 0)  
    
    # Set up island model.
    islands = Islands(
        loss_fn=benchmark_function,
        propagator=propagator,
        rng=rng,
        generations=config.generations,
        num_islands=config.num_islands,
        migration_topology=migration_topology,
        migration_probability=config.migration_probability,
        emigration_propagator=SelectMin,
        immigration_propagator=SelectMax,
        pollination=config.pollination,
        checkpoint_path=config.checkpoint,
    )

    # ✅ Run the optimization and measure time
    start_time = time.time()
    islands.propulate(
        logging_interval=config.logging_interval, 
        debug=config.verbosity
        )
    end_time = time.time()
    islands.summarize(top_n=1,debug=2)  # Print top-n best individuals on each island in summary.)
    convergence_time = end_time - start_time  # Compute time taken
    print(f"Total execution time: {convergence_time:.2f} seconds")
  