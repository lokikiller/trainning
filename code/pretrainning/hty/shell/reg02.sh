#!/bin/bash
if [ $# != 1 ]
then
	echo "usage: $0 address"
	exit 1
else
	ip=$1
fi

if [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]
then
	echo "looks like a ipv4."
elif [[ "$ip" =~ ^[A-Fa-f0-9:]+$ ]]
then
	echo "looks like a ipv6."
else
	echo "oops!"
fi
