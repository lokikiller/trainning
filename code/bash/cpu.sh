#!/bin/bash
#########################################
# author: hty / zby                     #
# create: 2015.11.30                    #
# fix:                                  #
# function: catch cpu usage             #
#########################################

sedCmd=`which sed`
awkCmd=`which awk`

cpu1=(`$sedCmd -n 's/^cpu\s//p' /proc/stat`)
total1=0

for value in "${cpu1[@]}"
do
   let total1=$total1+$value
done

#TODO:
sleep 1

cpu2=(`$sedCmd -n 's/^cpu\s//p' /proc/stat`)
total2=0

for value in "${cpu2[@]}"
do
    let total2=$total2+$value
done

let diff=$total2-$total1

res=$($awkCmd 'BEGIN{print "{ \"user\": "(('${cpu2[0]}' - '${cpu1[0]}')/'${diff}')*100", \"nice\": "(('${cpu2[1]}' - '${cpu1[1]}')/'${diff}')*100", \"system\": "(('${cpu2[2]}' - '${cpu1[2]}')/'${diff}')*100", \"idle\": "(('${cpu2[3]}' - '${cpu1[3]}')/'${diff}')*100", \"iowait\": "(('${cpu2[4]}' - '${cpu1[4]}')/'${diff}')*100", \"irq\": "(('${cpu2[5]}' - '${cpu1[5]}')/'${diff}')*100", \"softirq\": "(('${cpu2[6]}' - '${cpu1[6]}')/'${diff}')*100", \"steal\": "(('${cpu2[7]}' - '${cpu1[7]}')/'${diff}')*100", \"guest\": "(('${cpu2[8]}' - '${cpu1[8]}')/'${diff}')*100", \"guest_nice\": "(('${cpu2[9]}' - '${cpu1[9]}')/'${diff}')*100" }"}')

echo ${res}
