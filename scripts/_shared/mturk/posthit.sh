#!/usr/bin/env sh
HERE=`pwd`
cd $MTURK_CMD_HOME/bin
./loadHITs.sh -label $HERE/$1 -input $HERE/$1.input -question $HERE/$1.question -properties $HERE/$1.properties -maxhits 1