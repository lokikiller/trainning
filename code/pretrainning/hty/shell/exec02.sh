#!/bin/bash
exec 6<&0
exec < /etc/hosts
read a1
read a2

echo
echo "following lines read form file."
echo "-------------------------------"

echo $a1
echo $a2

echo;echo;echo

exec <&6 6<&-

echo -n "enter data: "
read b1
echo "input read from stdin."
echo "----------------------"

echo "b1 = $b1"
echo
