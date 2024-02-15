#!/bin/bash
#cat names.txt | IFS=",\n"; while read nome tot m f; do
cat names.txt | while read row; do
	if [[ $(cut -d "," -f3 <<< $row) > $(cut -d "," -f4 <<< $row) ]]; then
		line="$(cut -d ',' -f1 <<< $row),m"
	else
		line="$(cut -d ',' -f1 <<< $row),f"
	fi
	echo $line >> names_stripped.txt
done
