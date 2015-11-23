#!/bin/bash
LOGFILE=/tmp/logfile.txt
exec 6>&1
exec > $LOGFILE
echo -n "Logfile: "

date
echo "------------------"
echo

echo "output of \"uname -a\" command"
echo

uname -a
echo;echo
echo "output of \"df\" command"
echo
df

exec 1>&6 6>&-

echo
echo "== stdout now restored to default =="
echo
uname -a
echo

exit 0
