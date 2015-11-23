#!/bin/bash
if [ $# -ne 1 ]
then
	echo "usage error"
	exit
fi

exec 3< $1
while read -u 3 line
do
	echo $line
	read -p "press any key: " -n 1
done

exec 3<&-
