#!/bin/sh

# I think best to keep a list of ports open somewhere in this devops directory to pull from
# For now let's just keep it simple with the defaults
PORTS=$(seq 50000 50050)
IP=127.0.0.1

PORTLIST=$()

# Iterate through the list, killing each controlling process while looping
for port in ${PORTS}
do
	temp=$IP:$port
	kill $(netstat -anp | grep $temp | awk '{print $6}' | awk -F/ '{print $1}')
	echo $temp
done
