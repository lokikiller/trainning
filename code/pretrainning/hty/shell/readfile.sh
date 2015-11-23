#!/bin/bash
if [  $# -ne 1 ]
then
	echo "usage: $0 filepath"
	exit
fi

file=$1

{
	read line1
	read line2	
} < $file

echo "first line in $file is:"
echo "$line1"
echo "second line in $file is:"
echo "$line2"

count=0

while read LINE
do
	let count++
	echo "$count $LINE"
done < $file

echo -e "\nTotal $count lines read."

exit 0
