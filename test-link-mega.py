from mega.crypto import base64_to_a32, base64_url_decode, decrypt_attr, decrypt_key
import typing
import boltons.funcutils
import re
import requests
import json
import sys

def get_nodes_in_shared_folder(root_folder: str) -> dict:
	data = [{"a": "f", "c": 1, "ca": 1, "r": 1}]
	response = requests.post("https://g.api.mega.co.nz/cs", params={'id': 0, 'n': root_folder}, data=json.dumps(data))
	list_check = isinstance(response.json(), list)
	print(list_check)
	if(list_check == False):
		print(response.json())
	return int(list_check)

def parse_folder_url(url: str) -> tuple[str, str]:
	"Returns (public_handle, key) if valid. If not returns None."
	REGEXP1 = re.compile(r"mega.[^/]+/folder/([0-z-_]+)#([0-z-_]+)(?:/folder/([0-z-_]+))*")
	REGEXP2 = re.compile(r"mega.[^/]+/#F!([0-z-_]+)[!#]([0-z-_]+)(?:/folder/([0-z-_]+))*")
	m = re.search(REGEXP1, url)
	if not m:
		m = re.search(REGEXP2, url)
	if not m:
		print("Not a valid URL")
		return None
	root_folder = m.group(1)
	key = m.group(2)
	# You may want to use m.group(-1)
	# to get the id of the subfolder
	return (root_folder, key)

    
(root_folder, shared_enc_key) = parse_folder_url(sys.argv[1])
shared_key = base64_to_a32(shared_enc_key)
check = get_nodes_in_shared_folder(root_folder)

if (check == 0):
	check = 1
else:
	check = 0

print(check)

sys.exit(check)
