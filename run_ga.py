"""Simple island model example script."""

import pathlib
import random
import os
import numpy as np
from mpi4py import MPI

from propulate import Islands
from propulate.propagators import SelectMax, SelectMin
from propulate.utils import get_default_propagator, set_logger_config
from propulate.utils.benchmark_functions import (
    get_function_search_space,
    parse_arguments,
)
from migration_topologies import fully_connected_topology,one_way_chain_topology,ring_topology

if __name__ == "__main__":
    comm = MPI.COMM_WORLD

    # Parse command-line arguments.
    config, _ = parse_arguments(comm)
    config.num_islands = 4  # Total number of islands
    config.num_migrants = 2  # Number of individuals migrating per event
    config.generations = 100  # Run for 100 generations
    config.migration_probability = 0.5  # 50% probability of migration occurring
    config.pop_size = 100  # Population size per island
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
        log_rank=True,  # Do not prepend MPI rank to logging messages.
        colors=True,  # Use colors.
    )

    rng = random.Random(config.seed + comm.rank)  # Separate random number generator for optimization.
   
    benchmark_function, limits = get_function_search_space(config.function)  # Get callable function + search-space limits.

    # Set up evolutionary operator.
    propagator = get_default_propagator(  # Get default evolutionary operator.
        pop_size=config.pop_size,  # Breeding pool size
        limits=limits,  # Search-space limits
        crossover_prob=config.crossover_probability,  # Crossover probability
        mutation_prob=config.mutation_probability,  # Mutation probability
        random_init_prob=config.random_init_probability,  # Random-initialization probability
        rng=rng,  # Separate random number generator for Propulate optimization
    )

   
    migration_topology=one_way_chain_topology(config.num_islands,config.num_migrants)
    np.fill_diagonal(migration_topology, 0)  # An island does not send migrants to itself.        
    print(migration_topology)
    
    # Set up island model.
    # islands = Islands(
    #     loss_fn=benchmark_function,
    #     propagator=propagator,
    #     rng=rng,
    #     generations=config.generations,
    #     num_islands=config.num_islands,
    #     migration_topology=migration_topology,
    #     migration_probability=config.migration_probability,
    #     emigration_propagator=SelectMin,
    #     immigration_propagator=SelectMax,
    #     pollination=config.pollination,
    #     checkpoint_path=config.checkpoint,
    # )

    # # Run actual optimization.
    # islands.propulate(
    #     logging_interval=config.logging_interval,
    #     debug=config.verbosity,
    # )
    # islands.summarize(config.top_n, debug=config.verbosity)