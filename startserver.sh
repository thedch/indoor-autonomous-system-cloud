#!/bin/bash

if ! [ $(id -u) = 0 ]; then
	echo "This script must be run as root"
	exit 1
fi

source /root/ians_cloud/app/venv/bin/activate
python /root/ians_cloud/app/server.py & 
deactivate
mosquitto &

