#!/bin/bash

python3 scraper.py $1 $2

if [ -s mega-urls.txt ]
then
	./mega-sorter-and-mail.sh
fi

if [ -s anonfiles-urls.txt ]
then
	./anonfiles-sorter.sh
	if [ -s anonfiles-urls.txt ]
	then
		python3 anonfiles-notice.py
	fi
fi

if [ -s bayfiles-urls.txt ]
then
	./bayfiles-sorter.sh
	if [ -s bayfiles-urls.txt ]
	then
		python3 bayfiles-notice.py
	fi
fi

rm mega-urls.txt anonfiles-urls.txt bayfiles-urls.txt
./processed-backup.sh

exit 0
