#!/bin/bash

touch processed.txt
cat mega-processed.txt >> processed.txt
cat anonfiles-processed.txt >> processed.txt
cat bayfiles-processed.txt >> processed.txt
echo -e "backing up processed links...\n"
echo -e "to: -\nsubject: leakedbb-reaper processed backup\n"| (cat - && uuencode processed.txt processed.txt) | ssmtp -
rm -f processed.txt
