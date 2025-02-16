# **Project Setup Instructions**

## **Getting Started**

1. **Build the Docker Image**  
   Ensure the Docker image is built before running the containers:
   ```bash
   docker build -t my_experiment .
   ```

2. **Run the Docker Containers**  
   Execute the script to create **4 containers**, each with **specific CPU cores and RAM**:
   ```bash
   bash run_container.sh
   ```
   This script:
   - Starts **4 separate containers**.
   - Assigns **specific CPU cores and RAM** to each container.
   - Ensures **isolation** between experiment runs.

---

## **Setting Up SSH in Each Container**  
(Automation for this step is planned for future updates.)

3. **Manually configure SSH inside each container**:
   ```bash
   apt-get update && apt-get install -y openssh-server
   ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa   (create key in one of the nodes)
   cat ~/.ssh/id_rsa.pub | ssh root@node2 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys" ,repeat for node3,node4
   service ssh start
   ```

4. **Verify SSH connectivity**:
   ```bash
   ssh root@[node2,node3,node4]
   ```

---

## **Running the MPI-Based Genetic Algorithm**

5. **Set up MPI on the Master Node**  
   Run the following commands to **allow MPI execution as root**:
   ```bash
   export OMPI_ALLOW_RUN_AS_ROOT=1
   export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
   ```

6. **Run the Genetic Algorithm across all containers**:
   ```bash
   mpirun --hostfile hostfile -np 24 python3 run_ga.py
   ```
   This command:
   - Uses `mpirun` for **multi-container execution**.
   - Reads available hosts from **`hostfile`**.
   - Runs **24 parallel processes** (`-np 24`).
   - Executes **`run_ga.py`**, the genetic algorithm script.

---

## **Post-Experiment Cleanup**

7. **Stop and remove all running containers**:
   ```bash
   docker stop $(docker ps -q)
   docker rm $(docker ps -aq)
   ```

8. **(Optional) Remove the Docker image**:
   ```bash
   docker rmi my_experiment
   ```

---

## **Conclusion**  
This guide ensures **efficient parallel execution** of the genetic algorithm across **multiple Docker containers** using **MPI**. Future updates will include **automated SSH setup** for better scalability.

---



