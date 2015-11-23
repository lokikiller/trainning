#!/bin/bash
ARG_B=0
eval set -- `getopt -o a::bc: --long arga::,argb,argc: -n 'getopt_longopt.sh' -- "$@"`
while true
do
	case "$1" in
	  -a|--arga)
	  	case "$2" in
		  "")
			ARG_A='default value'
			shift
		  ;;
		  *)
			ARG_A=$2
			shift
		  ;;
		esac
	  ;;
	  -b|--argb)
		ARG_B=1
	  ;;
	  -c|--argc)
		case "$2" in
		  "")
			shift
		  ;;
		  *)
			ARG_C=$2
			shift
		  ;;
		esac
	  ;;
	  --)
		shift
		break
	  ;;
	  *)
		echo "internal error!"
		exit 1
	  ;;
	esac
	shift
done

echo "arg_a = $ARG_A"
echo "arg_b = $ARG_B"
echo "arg_c = $ARG_C"
