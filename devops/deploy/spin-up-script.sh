#!/bin/sh

# Just a basic script to spin up listening servers on different ports
PORTS=$(seq 30000 30050)

export PYTHONPATH=src/main/py

for port in ${PORTS}
do
  echo "Starting on port $port"
  python3 -m sample_module.udp_server ${port} &
done

