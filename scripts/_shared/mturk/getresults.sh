#!/usr/bin/env sh
HERE=`pwd`
cd $MTURK_CMD_HOME/bin
./getResults.sh -successfile $HERE/$1.success -outputfile $HERE/$1.results