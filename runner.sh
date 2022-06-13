#!/bin/bash

while true
do
	./run.sh 1 2
	target=$(date -d "+1 day")
	echo -e "next run time: $target"
	echo -e "sleeping..."
	sleep 86400
done
