#!/bin/bash
#########################################
# author: hty / zby                     #
# create: 2015.11.30                    #
# fix:                                  #
# function: catch cpu usage             #
#########################################

sedCmd=`which sed`
awkCmd=`which awk`

cpu=(`$sedCmd -n 's/^cpu\s//p' /proc/stat`)
total=0

for value in "${cpu[@]}"
do
   let total=$total+$value
done

res=$($awkCmd 'BEGIN{print "{ \"user\": "('${cpu[0]}'/'${total}')*100", \"nice\": "('${cpu[1]}'/'${total}')*100", \"system\": "('${cpu[2]}'/'${total}')*100", \"idle\": "('${cpu[3]}'/'${total}')*100", \"iowait\": "('${cpu[4]}'/'${total}')*100", \"irq\": "('${cpu[5]}'/'${total}')*100", \"softirq\": "('${cpu[6]}'/'${total}')*100", \"steal\": "('${cpu[7]}'/'${total}')*100", \"guest\": "('${cpu[8]}'/'${total}')*100", \"guest_nice\": "('${cpu[9]}'/'${total}')*100" }"}')

echo ${res}
