#!/bin/bash
declare -a linux=('debian' 'redhat' 'suse' 'centos' 'frdora')
echo ${linux[@]}

arr=(one two three)
echo ${arr[0]} ${arr[1]} ${arr[2]}

echo ${arr[*]}

arr[3]=four

echo ${arr[@]}

echo $arr

unset arr[2]
echo ${arr[@]}

unset arr
echo ${arr[@]}
