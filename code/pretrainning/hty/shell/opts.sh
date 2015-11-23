#!/bin/bash
vflag=off
filename=""
output=""

function usage() {
	echo "USAGE:"
	echo "       myscript [-h] [-v] [-f <filename>] [-o <filename>]"
	echo -1
}

while getopts :hvf:o: opt
do
	case "$opt" in
	  v)
		vflag=on
	  ;;
	  f)
		filename=$OPTARG
		if [ ! -f $filename ]
		then
			echo "the source file $filename doesn't exist!"
			exit
		fi
	  ;;
	  o)
		output=$OPTARG
		if [ ! -d `dirname $output` ]
		then
			echo "the output path `dirname $output` dosen't exist!"
			exit
		fi
	  ;;
	  h)
		usage
		exit
	  ;;
	  :)
		echo "the option -$OPTARG requires an argument."
		exit
	  ;;
	  ?)
		echo "invalid option: -$OPTARG"
		usage
		exit 2
	  ;;
	esac
done

