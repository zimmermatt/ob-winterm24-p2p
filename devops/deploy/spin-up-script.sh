#!/bin/sh

PSTART=${1:-50000}
PEND=${2:-50050}
# Just a basic script to spin up listening servers on different ports in dynamic port range
PORTS=$(seq ${PSTART} ${PEND})

export PYTHONPATH=../../src/main/py

for port in ${PORTS}
do
  echo "Starting on port $port"
  python3 -m sample_module.udp_server ${port} &
done

