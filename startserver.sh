#!/bin/bash

if ! [ $(id -u) = 0 ]; then
	echo "This script must be run as root"
	exit 1
fi

python /root/indoor-autonomous-system-cloud/app/server.py & 
mosquitto &

