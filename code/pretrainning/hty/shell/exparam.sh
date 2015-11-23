#!/bin/bash

#1. indirect parameter
PARAMETER=TEMP
TEMP="It is test"
echo ${!PARAMETER}
echo ${PARAMETER}

#2. list prefix
echo ${!PA*}

FILENAME=linux_bash.txt

#3. remove extension name
echo ${FILENAME%.*}

#   remove filename
echo ${FILENAME##*.}

FILENAME=/home/hty/linux_bash.txt

#   remove filename
echo ${FILENAME%/*}

#   remove pathname
echo ${FILENAME##*/}

#4. search and replace
MYSTRING="This is used for replacing string or removing string"
echo ${MYSTRING/string/characters}
echo ${MYSTRING//string/characters}
echo ${MYSTRING/string}
echo ${MYSTRING//string}

#5. length of parameter
echo ${#MYSTRING}

#6. substring of parameter
echo ${MYSTRING:8}
echo ${MYSTRING:8:10}
