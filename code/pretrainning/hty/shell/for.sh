#!/bin/bash
for var in 1 2 3
do
    echo "The for loop is run $var times."
done

for file in 'ls ./*'
do
    echo $file
done

for (( i=0; i<3; i++))
do
    echo -n "* "
done

echo ""

var=1
while [ $var -le 3 ]
do
    echo "the for loop is run $var times."
    var=$((var+1))
done

while :
do
    clear
    echo "==========================="
    echo "         MAIN - MENU       "
    echo "1. Display data and time   "
    echo "2. Dislpay system info     "
    echo "3. DIsplay what doing      "
    echo "4. Exit                    "
    echo "==========================="

    read -p "Enter your choice [1 - 4]:" choice
    case $choice in
      1)
        echo "today is $(date +%Y-%m-%d)."
        echo "current time: $(date +%H:%M:%S)"
        read -p "press [Enter] key to continue..." readEnterKey
      ;;
      2)
        uname -a
        read -p "press [Enter] key to continue..." readEnterKey
      ;;
      3)
        w
        read -p "press [Enter] key to continue..." readEnterKey
      ;;
      4)
        echo "Bye!"
        break
      ;;
      *)
        echo "error"
        read -p "press [Enter] key to continue..." readEnterKey
      ;;
    esac
done
