#!/bin/bash

PSTART=${1:-50000}
PEND=${2:-50050}
# Just a basic script to spin up listening servers on different ports in dynamic port range
PORTS=$(seq ${PSTART} ${PEND})

IP=127.0.0.1
COUNT=0
((NUM_PORTS=${PEND}-${PSTART}))

echo $NUM_PORTS
export PYTHONPATH=../../src/main/py

port=$PSTART

while [ ${COUNT} -lt ${NUM_PORTS} ]
do
  #Check for Open ports, if open then OK, else continue
  if ! netstat -apn | grep -q "$IP:$port" 
  then
    echo "Starting on port $port"
    python3 -m sample_module.udp_server ${port} &
    echo "$port" >> port_list.txt
    ((port++))
    ((COUNT++))
  else
    echo "Port $port already bound"
    ((port++))
  fi
done
