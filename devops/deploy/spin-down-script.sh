#!/bin/bash

# Now fully implemented spinning down through the port_list.txt
IP=127.0.0.1
declare -a PORTS=()
while IFS= read -r line
do
	PORTS+=("$line")
done < "port_list.txt"

# Iterate through the list, killing each controlling process while looping
for port in ${PORTS[*]}
do
	echo "Killing processes at $IP:$port"
	temp=$IP:$port
	kill -15 $(netstat -anp | grep $temp | awk '{print $6}' | awk -F/ '{print $1}')
done

echo -n > "port_list.txt"
