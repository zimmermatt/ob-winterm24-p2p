#!/usr/bin/env bash

# Just a basic script to spin up listening servers on different ports in dynamic port range
# Setting up variables
PSTART=${1:-50000}
PEND=${2:-50050}
PEER_FILE="peer_list.txt"
IP="127.0.0.1"
COUNT=0
((NUM_PORTS=${PEND}-${PSTART}))

# Making keys directory to hold public/private keys if not exist
if [ -d keys/ ]
then
	echo "Directory keys exists."
else
	mkdir keys/
fi

# Making Peer file if it does not exist
if [ -f $PEER_FILE ]
then
	echo "Peer List File exists"
else
	touch $PEER_FILE
	chmod 600 $PEER_FILE
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
    echo "${COUNT},${port},${private_key},${public_key}" >> $PEER_FILE

    # Create 2 commissioning peer, while the rest as listening peer doing the commission
    if [ ${COUNT} -le 2 ]
    then
        python3 -m peer.peer ${port} "keys/node$COUNT" "${IP}:${PSTART}" < commission_input.txt &
    else
	python3 -m peer.contributing_peer ${port} "keys/node$COUNT" "${IP}:${PSTART}" &
    fi
    ((port++))
    ((COUNT++))
  else
    echo "Port $port already bound"
    ((port++))
  fi
done
