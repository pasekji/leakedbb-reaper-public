#!/bin/bash

echo "Testing bayfiles.com links...\n"
links='bayfiles-urls.txt'
input='bf-temp.txt'
output='bayfiles-not-processed.txt'
history='bayfiles-processed.txt'
awk -F '/' '{ print $4 }' "$links" > "$input"
lines=$(cat $input)
touch "$output"

for line in $lines
do
	grep "$line" "$history"
	if [ $? -eq 0 ]; then
		echo -e "$line already processed\n"
	else
		echo -e "processing $line\n"
		python3 test-link-bayfiles.py $line
		exit_status=$?
		if [[ $exit_status -eq 0 ]]; then
			echo -e "OK $line\n"
			grep "$line" "$links" >> "$output"
		else
			echo -e "ERROR loading contents $line\n"
		fi
		grep "$line" "$links" >> "$history"
	fi
done

cat "$output" > "$links"
rm -f "$output"
rm -f "$input"
echo -e "bayfiles.com links sorted\!\n"
exit 0
