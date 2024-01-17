#!/bin/sh

# I think best to keep a list of ports open somewhere in this devops directory to pull from
# For now let's just keep it simple with the defaults
PORTS=$(seq 50000 50050)
IP=127.0.0.1

PORTLIST=$()
for port in ${PORTS}
do
	temp=$IP:$port
	echo $temp
done
