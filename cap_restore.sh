#!/bin/bash

if [ -z $HOME ]; then
	echo "$HOME should be set"
	exit -1
fi

export PYTHON=python
export SCRIPT_PATH=$HOME/code/capitalization_restoration/service.py

# Uncomment the PID_DIR if you have write permission to /var/run
# export PID_DIR=/var/run
export PID_DIR=$HOME/.pid

case $1 in
   start)
		echo $$ > $PID_DIR/cap_restore.pid;
		exec 2>&1 ${PYTHON} ${SCRIPT_PATH} & 1>/tmp/cap_restore.out 
		;;
    stop)  
		kill `cat $PID_DIR/.cap_restore.pid` ;;
    *)  
		echo "usage: cap_restore.sh {start|stop}" ;;
esac
exit 0
