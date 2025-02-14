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

if __name__ == "__main__":
    comm = MPI.COMM_WORLD

    # Parse command-line arguments.
    config, _ = parse_arguments(comm)
    config.num_islands=4
    config.num_migrants=2
    # ✅ Set a single folder for all checkpoint files
    checkpoint_dir = "checkpoints"
    os.makedirs(checkpoint_dir, exist_ok=True)  # Ensure the directory exists
    config.checkpoint = checkpoint_dir  # Set checkpoint path to the directory
    # Set up separate logger for Propulate optimization.
    set_logger_config(
        level=config.logging_level,  # Logging level
        log_file=f"{config.checkpoint}/{pathlib.Path(__file__).stem}.log",  # Logging path
        log_to_stdout=True,  # Print log on stdout.
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

    # Set up migration topology.[fully connected topology]
    # migration_topology = config.num_migrants * np.ones(  # Set up fully connected migration topology.
    #     (config.num_islands, config.num_islands), dtype=int
    # )
    # np.fill_diagonal(migration_topology, 0)  # An island does not send migrants to itself.
    
    # Set up migration topology [ring topology]
    migration_topology = np.zeros((config.num_islands, config.num_islands), dtype=int)
    # Set migration to left and right neighbors in a ring structure
    for i in range(config.num_islands):
        migration_topology[i, (i - 1) % config.num_islands] = config.num_migrants  # Left neighbor
        migration_topology[i, (i + 1) % config.num_islands] = config.num_migrants  # Right neighbor
    np.fill_diagonal(migration_topology, 0)  # An island does not send migrants to itself.
    
        
    print(migration_topology)
    # Set up island model.
    # islands = Islands(
    #     checkpoint_path=config.checkpoint
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