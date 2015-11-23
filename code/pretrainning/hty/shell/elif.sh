#!/bin/bash
if [ $# -eq 0 ]
then
    echo "$0 : you must give one integers."
    exit 1
fi

if [ $1 -gt 0 ]
then
    echo "the number is positive."
elif [ $1 -lt 0 ]
then
    echo "the number is negative."
elif [ $1 -eq 0 ]
then
    echo "the number is 0."
else
    echo "opps! $1 is not number."
fi
