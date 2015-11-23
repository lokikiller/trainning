#!/bin/bash
if [ $# -lt 2 ]
then
    echo "usage : $0 signalnumber pid"
    exit
fi

case "$1" in
1)
    echo "sending sighup signal to pid $2 ."
    kill -SIGHUP $2
;;
2)
    echo "sending sigint signal to pid $2 ."
    kill -SIGINT $2
;;
3)
    echo "sending sigquit signal to pid $2 ."
    kill -SIGQUIT $2
;;
9)
    echo "sending sigkill signal to pid $2 ."
    kill -SIGKILL $2
;;
*)
    echo "signal number $1 is not processed."
;;
esac
