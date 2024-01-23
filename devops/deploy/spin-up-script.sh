#!/bin/bash

# Just a basic script to spin up listening servers on different ports in dynamic port range
# Setting up variables
PSTART=${1:-50000}
PEND=${2:-50050}
PEER_FILE="peer_list.txt"
IP=127.0.0.1
COUNT=0
((NUM_PORTS=${PEND}-${PSTART}))

# Making keys directory to hold public/private keys if not exist
if [ -d keys/ ]
then
	echo "Directory keys exists."
else
	mkdir keys/
fi

echo "Total number of ports: $NUM_PORTS"
export PYTHONPATH=../../src/main/py

port=$PSTART

# Loop for spinning up
while [ ${COUNT} -le ${NUM_PORTS} ]
do
  #Check for Open ports, if open then OK, else continue
  if ! netstat -apn | grep -q "$IP:$port" 
  then
    # Generating keys
    ssh-keygen -t ed25519 -f "keys/node${COUNT}" -N ""

    # Cutting the keys from the key files
    private_key=$(cat keys/node${COUNT} | awk -F '-----' '{print $1}' | tr -d '\n')
    public_key=$(cat keys/node${COUNT}.pub | awk -F '-----' '{print $1}' | tr -d '\n')
    
    # Handling putting the port information and the keys into the peer list
    echo "Starting on port $port"
    echo "${COUNT} ,${port} ,${private_key} ,${public_key}" >> $PEER_FILE

    # Calling server
    python3 -m sample_module.udp_server ${port} &
    ((port++))
    ((COUNT++))
  else
    echo "Port $port already bound"
    ((port++))
  fi
done
