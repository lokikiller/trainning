#!/bin/bash

if [  $# -ne 1 ]
then
    echo "Usage: `basename $0` param"
fi

while true
do
    if [[ -n `ping $1 -c 1 | grep "ttl="` ]]
    then
        for i in `seq 1 100`
        do
            echo -en '\a'
        done
        break
    fi
done
