from webbot import Browser
from bs4 import BeautifulSoup
import time
import re
import sys
import os
import hashlib
import subprocess
import requests
import base64
import json

original_stdout = sys.stdout

def saveToFileWithStrip(struct, name):
	with open(name, 'w') as f:
		sys.stdout = f 
		for link in struct:
			print(link.rstrip("\n"))
		sys.stdout = original_stdout

def loadPage(web):
	web.go_to('https://anonfiles.com/abuse')

def scrapeCaptcha(web):
	content = web.get_page_source()
	soup = BeautifulSoup(content, 'html.parser')
	samples = soup.find_all("img")
	temp = []
	for item in samples:
		temp.append(item['src'])
	filter1 = filter(lambda x: x.startswith("data:image/jpeg;base64"), temp)
	saveToFileWithStrip(filter1, 'captcha-url.txt')

def readFile(name):
	with open(name, 'r') as file:
		data = file.read().rstrip()
	return data
	
def saveCaptcha():
	url = readFile('captcha-url.txt')
	b64_string = url.removeprefix("data:image/jpeg;base64,")
	image_code = base64.b64decode(b64_string.replace("\n",""))
	with open('captcha.jpeg', 'wb') as f:
		f.write(image_code)

def solveCaptcha(f):
	with open(f, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	url = 'https://api.apitruecaptcha.org/one/gettext'
	data = { 'userid':'-', 'apikey':'-',  'data':str(encoded_string)[2:-1]}
	r = requests.post(url = url, json = data)
	j = json.loads(r.text)
	return j['result']

def readLinks(name):
	f = open(name, 'r+')
	lines = [line for line in f.readlines()]
	f.close()
	return lines
	
def fillIn(web, captcha):
	web.click(xpath="//*[@id='abuse-reasons']/option[text()='Pornography']")
	web.type('-', number = 1, classname="form-control")
	web.type('-', number = 2, classname="form-control")
	links = readLinks('anonfiles-urls.txt')
	web.type(links[0].rstrip(), number = 3, classname="form-control")
	header = readFile('anonfiles-notice-templ.txt')
	web.type(header, clear=False, tag="textarea", classname="form-control")
	web.type('\n', clear=False, tag="textarea", classname="form-control")
	for link in links:
		web.type(link, clear=False, tag="textarea", classname="form-control")	
	web.type(captcha, number = 4, classname="form-control")
	web.press(web.Key.ENTER)
	
def checkError(web):
	content = web.get_page_source()
	soup = BeautifulSoup(content, 'html.parser')
	fail = soup.find("strong", string="Report submission failed.")
	if fail:
		return True
	return False

		
print("launching browser...\n")
web = Browser()
check = True
while check != False:
	print("loading website...\n")
	loadPage(web)
	print("scraping captcha urls...\n")
	scrapeCaptcha(web)
	print("saving captcha...\n")
	saveCaptcha()
	print("solving captcha...")
	captcha = solveCaptcha('captcha.jpeg')
	print(captcha)
	print("filling out the form...\n")
	fillIn(web, captcha)	
	check = checkError(web)
	if check:
		print("ERROR occured, trying again...\n")

time.sleep(4)
print("ALL DONE, notice sent!\n")
web.quit()



