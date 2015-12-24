#!/bin/bash
nohup python /home/code/filter.py > /dev/null 2>&1 &
python /home/code/server.py
