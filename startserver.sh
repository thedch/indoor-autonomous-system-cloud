#!/bin/bash

if ! [ $(id -u) = 0 ]; then
	echo "This script must be run as root"
	exit 1
fi

. /ians_cloud/venv/bin/activate
python ./ians_cloud/server.py & 
deactivate

