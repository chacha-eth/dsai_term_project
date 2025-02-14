#!/bin/bash
CPUS=("0-5" "6-11" "12-17" "18-23")
NODES=("node1" "node2" "node3" "node4")
MEMORY="6g"
docker network create mpi-net || true

# Start containers
for i in {0..3}; do
    echo "🚀 Starting ${NODES[$i]} with CPU cores ${CPUS[$i]} and memory $MEMORY..."
    docker run -dit \
        --name "${NODES[$i]}" \
        --cpuset-cpus="${CPUS[$i]}" \
        --memory="$MEMORY" \
        --network=mpi-net \
        --hostname "${NODES[$i]}" \
        -v "$(pwd):/app" \
        mpi-propulate \
        tail -f /dev/null
done

echo "✅ All containers started successfully!"
