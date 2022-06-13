import re
import requests
import json
import sys

def info(id):
	URL="https://api.anonfiles.com/v2/file/{id}/info".format(id=id)
	r = requests.get(url=URL)
	j = json.loads(r.text)
	return j['status']

check = info(sys.argv[1])

if (check == 0):
        check = 1
else:
        check = 0

print(check)

sys.exit(check)

