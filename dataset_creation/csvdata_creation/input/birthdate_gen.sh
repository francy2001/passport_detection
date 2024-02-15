#!/bin/bash
for i in {1..3000}; do
	echo $(( 1 + $RANDOM % 28 ))/$(( 1 + $RANDOM % 13 ))/$(( 1900 + $RANDOM % 111 )) >> birthdates.txt 
done
