#!/bin/bash
read -p "input a number: " num

if [[ $num =~ ^[0-9]+$  ]]
then
	echo "it is a number"
else	
	echo "it is not a number"
fi
