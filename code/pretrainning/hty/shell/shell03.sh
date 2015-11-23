#!/bin/bash
function checkpid() {
    local i
    for i in $*
    do
      [ -d "/proc/$i" ] && return 0
    done

    return 1
}

if ( checkpid $1 )
then
    echo "running"
else
    echo "stoping"
fi
