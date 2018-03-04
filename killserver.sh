#!/bin/bash

kill $(ps -e | grep python | awk '{print $1}')
kill $(ps -e | grep mosquitto | awk '{print $1}')

