#!/bin/bash
test -e ./shell01.sh && echo "the file $_ found" || echo "the file $_ not found"

test -f ./shell01.sh && echo "the file $_ found" || echo "the file $_ not found"

test -d /usr/local && echo "the dir $_ is exit" || echo "the dir $_ is not exit"

test -r ./shell01.sh && echo "the file $_ is readable" || echo "the file $_ is not readable"

test -w ./shell01.sh && echo "the file $_ is writable" || echo "the file $_ is not writable"

test -x ./shell01.sh && echo "the file $_ is executable" || echo "the file $_ is not executable"

test -s ./shell01.sh && echo "the file $_ is not empty" || echo "the file $_ is empty"

test "abc" = "cde"; echo $?

test "abc" != "cde"; echo $?

[ -z "" ]; echo $?
[ -n "" ]; echo $?

[ 5 -eq 5 ] && echo yes || echo no
[ 5 -ne 4 ] && echo yes || echo no
[ 5 -ge 4 ] && echo yes || echo no
[ 5 -le 6 ] && echo yes || echo no
[ 5 -lt 6 ] && echo yes || echo no
[ 5 -gt 4 ] && echo yes || echo no
