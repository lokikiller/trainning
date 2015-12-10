#!/bin/bash
##############################################
# author: hty / zby                          #
# create: 2015.11.30                         #
# fix:                                       #
# function: catch avg_load from /proc/loadavg #
##############################################

#numsCore=$(/bin/grep -c 'processor' /proc/cpuinfo)

#if [ $numsCore -eq 0 ]
#then
#    numsCore=1
#fi

catCmd=`which cat`
awkCmd=`which awk`

res=$($catCmd /proc/loadavg | $awkCmd '{print "{ \"w1_avg\": "$1", \"w5_avg\": "$2", \"w15_avg\": "$3" }" }')

echo ${res}
