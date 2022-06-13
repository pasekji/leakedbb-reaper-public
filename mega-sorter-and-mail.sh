#!/bin/bash

echo "Testing Mega.nz links and sending notice...\n"
input='mega-urls.txt'
output='mega-not-processed.txt'
history='mega-processed.txt'
lines=$(cat $input)
touch "$output"

for line in $lines
do
	grep -qxF "$line" "$history"
	if [ $? -eq 0 ]; then
		echo -e "$line already processed\n"
	else
		echo -e "processing $line\n"
		python3 test-link-mega.py $line
		exit_status=$?
		if [[ $exit_status -eq 0 ]]; then
			echo -e "OK $line\n"
			echo "$line" >> "$output"
		else
			echo -e "ERROR loading contents $line\n"
		fi
		echo "$line" >> "$history"
	fi
done

if [ -s "$output" ]
then
	cp mega-mail-template.txt mega-mail-temp.txt
	cat "$output" >> mega-mail-temp.txt
	ssmtp abuse@mega.nz < mega-mail-temp.txt
	rm -f mega-mail-temp.txt
	echo -e "MEGA.NZ notice sent\!\n"
fi
rm -f "$output"
exit 0
