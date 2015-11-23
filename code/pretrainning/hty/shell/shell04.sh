#!/bin/bash
function progress() {
	echo -n "$0: please wait..."
	while true
	do
		echo -n "."
		sleep 5
	done
}

function dobackup() {
	for (( i=0; i<10000; i++ ))
	do
		if [ $i -lt 10000 ]
		then
			continue
		fi	
	done
}

progress &

MYSELF=$!

dobackup

kill $MYSELF > /dev/null 2>&1
echo -n "...done."
echo
