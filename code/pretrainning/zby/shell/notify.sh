#! /bin/bash

if [[ $# != 1 ]]; then 
    echo "need one param"
    exit 1
fi

while true
do	
    CONNECTED=`ping -c 1 $1|grep PING`
    if [[ -n $CONNECTED ]]; then
        echo -en '\07'
    fi
done
