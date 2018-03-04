#!/bin/bash

sudo kill $(ps -e | grep python | awk '{print $1}')
