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

res=$($awkCmd 'BEGIN{printf( "{ \"user\": %.2f, \"nice\": %.2f, \"system\": %.2f, \"idle\": %.2f, \"iowait\": %.2f, \"irq\": %.2f, \"softirq\": %.2f, \"steal\": %.2f, \"guest\": %.2f, \"guest_nice\": %.2f }", ('${cpu[0]}'/'${total}')*100, ('${cpu[1]}'/'${total}')*100, ('${cpu[2]}'/'${total}')*100, ('${cpu[3]}'/'${total}')*100, ('${cpu[4]}'/'${total}')*100, ('${cpu[5]}'/'${total}')*100, ('${cpu[6]}'/'${total}')*100, ('${cpu[7]}'/'${total}')*100, ('${cpu[8]}'/'${total}')*100, ('${cpu[9]}'/'${total}')*100 )}')

echo ${res}
