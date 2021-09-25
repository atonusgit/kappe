#!/usr/bin/bash

echo Restart graph
killall -9 python3
nohup python3 ~/kappe/graph.py &>/dev/null &
