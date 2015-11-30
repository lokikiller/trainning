#!/bin/bash
###################################
# autohr: hty / zby               #
# create: 2015.11.30              #
# fix:                            #
# function: catch mem info        #
###################################

awkCmd=`which awk`
catCmd=`which cat`
grepCmd=`which grep`

mem=`$catCmd /proc/meminfo | $grepCmd -w 'MemTotal:\|MemFree:\|Buffers:\|Cached:\|Active:\|Inactive:\|SwapTotal:\|SwapFree:'`

echo $mem | $awkCmd '{print "{ \"total\":"($2*1024)", \"used\":"(($2-$5)*1024)", \"abs_used\":"(($2-($5+$8+$11))*1024)", \"free\":"($5*1024)", \"buffers\":"($8*1024)", \"cached\":"($11*1024)", \"active\":"($14*1024)", \"inactive\":"($17*1024)", \"swap_used\":"(($20-$23)*1024)" }"}'
