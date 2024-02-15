#!/bin/bash
for i in {1..3000}; do
	echo $(( 1 + $RANDOM % 28 ))/$(( 1 + $RANDOM % 13 ))/$(( 2015 + $RANDOM % 9 )) >> issue_date.txt 
done
