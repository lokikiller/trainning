#!/bin/bash
old_IFS=$IFS

if [ $# -ne 1 ]
then
	echo "usage: `basename $0` filename"
	exit
fi

if [ ! -f $1 ]
then
	echo "the file $1 doesn't exist!"
	exit 1
fi

IFS=$'\n'

for line in $(cat $1)
do
	echo $line
done

IFS=$old_IFS
