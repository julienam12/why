#!/usr/bin/env sh
cd $MTURK_CMD_HOME/bin
./loadHITs.sh -label $2 -input $1.input -question $1.question -properties $1.properties -maxhits 1