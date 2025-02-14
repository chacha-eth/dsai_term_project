# dsai_term_project
# check mpirun runns inside each container 
-  first enter to the container,you can also check with out entering to the container,which i did not set in my 
   conttainers
   - mpirun --allow-run-as-root -np 4 echo "MPI Test
## note when excedding the number of processors 
here are not enough slots available in the system to satisfy the 7
slots that were requested by the application:

  python3

Either request fewer slots for your application, or make more slots
available for use.

A "slot" is the Open MPI term for an allocatable unit where we can
launch a process.  The number of slots available are defined by the
environment in which Open MPI processes are run:

  1. Hostfile, via "slots=N" clauses (N defaults to number of
     processor cores if not provided)
  2. The --host command line parameter, via a ":N" suffix on the
     hostname (N defaults to 1 if not provided)
  3. Resource manager (e.g., SLURM, PBS/Torque, LSF, etc.)
  4. If none of a hostfile, the --host command line parameter, or an
     RM is present, Open MPI defaults to the number of processor cores

In all the above cases, if you want Open MPI to default to the number
of hardware threads instead of the number of processor cores, use the
--use-hwthread-cpus option.

Alternatively, you can use the --oversubscribe option to ignore the
number of available slots when deciding the number of processes to
launch.

# testing mpi code inside container 
  - mpirun -np 6 --allow-run-as-root python3 mpi_hello.py

# ssh install and solution to the problem i faced 
      - apt update && apt install -y openssh-server
      - ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa   (create key in one of the nodes)
      - ssh-copy-id root@node2    (copy key to each node,allows sshing without password but asks first time)
      - cat ~/.ssh/id_rsa.pub | ssh root@node2 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"  (it does not ask password for copy)

# running 
  - mpirun --hostfile hostfile -np 24 --mca hwloc_base_binding_policy none python3 mpi_hello.py
# to use host computer 
   1.addes on sudo nano /etc/hosts this 
                172.19.0.2 nod1
                172.19.0.3 nod2
                172.19.0.4 nod3
                172.19.0.5 nod4
# set environment variables important
  export OMPI_ALLOW_RUN_AS_ROOT=1
  export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1