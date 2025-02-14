# Base image: Use Ubuntu 22.04
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openmpi-bin openmpi-common openmpi-doc libopenmpi-dev \
    python3 python3-pip python3-dev \
    build-essential cmake git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    numpy scipy matplotlib mpi4py propulate watchdog

WORKDIR /app

# Default command to keep container running
CMD ["tail", "-f", "/dev/null"]
