from webbot import Browser
from bs4 import BeautifulSoup
import time
import re
import sys
import os
import hashlib
import subprocess


original_stdout = sys.stdout

def saveToFileWithStrip(struct, name):
	with open(name, 'a') as f:
		sys.stdout = f 
		for link in struct:
			print(link.rstrip("\n"))
		sys.stdout = original_stdout

def saveToFile(struct, name):
	with open(name, 'a') as f:
		sys.stdout = f 
		for link in struct:
			print(link)
		sys.stdout = original_stdout

def login(web):
	web.go_to('https://leakedbb.com/member.php?action=login') 
	web.type('-', into='Username', id='username')
	web.type('-', into='Password', id='password')
	web.press(web.Key.ENTER)
	time.sleep(5)

def scrapePage(web, x, url):
	mylist = []
	for i in x:
		url_finished = url + str(i) 
		web.go_to(url_finished)
		content = web.get_page_source()
		soup = BeautifulSoup(content, 'html.parser')
		text = soup.get_text()
		text_urls_mega = re.findall(r'(https?://mega.nz[^\s]+)', text)
		text_urls_anonfiles = re.findall(r'(https?://anonfiles.com[^\s]+)', text)
		text_urls_bayfiles = re.findall(r'(https?://bayfiles.com[^\s]+)', text)
		text_urls_drive = re.findall(r'(https?://drive.google.com[^\s]+)', text)
		samples = soup.find_all("a")
		for link in samples:
			mylist.append(link.get('href'))
		for link in text_urls_mega:
			mylist.append(link)
		for link in text_urls_anonfiles:
			mylist.append(link)
		for link in text_urls_bayfiles:
			mylist.append(link)
		for link in text_urls_drive:
			mylist.append(link)
	return mylist

def readFile(name):
	f = open(name, 'r+')
	lines = [line for line in f.readlines()]
	f.close()
	return lines
	
def scrapeThreads(web, start, end):
	url = "https://leakedbb.com/Forum-Amateur-Nudes?page="
	x = range(start, end, 1)
	mylist = scrapePage(web, x, url)
	
	saveToFile(mylist,'temp.txt')		
			
	lines = readFile('temp.txt')
	filter1 = filter(lambda x: x.startswith("Thread-"), lines)

	saveToFileWithStrip(filter1,'urls.txt')
	
def scrapeLeakLinks(web):
	lines = readFile('urls.txt')
	
	url = "https://leakedbb.com/"
	mylist = scrapePage(web, lines, url)
	
	os.remove("temp.txt")
	saveToFile(mylist, 'temp.txt')
	lines = readFile('temp.txt')
	filter1 = filter(lambda x: x.startswith("https://leakedbb.com/link/"), lines)
	filter2 = filter(lambda x: x.startswith("https://leakedbb.com/onyx/"), lines)
	filter3 = filter(lambda x: x.startswith("https://mega.nz/"), lines)
	filter4 = filter(lambda x: x.startswith("https://anonfiles.com/"), lines)
	filter5 = filter(lambda x: x.startswith("https://bayfiles.com/"), lines)
	filter6 = filter(lambda x: x.startswith("https://drive.google.com/"), lines)
	
	saveToFileWithStrip(filter3, 'mega-temp.txt')
	saveToFileWithStrip(filter4, 'anonfiles-temp.txt')
	saveToFileWithStrip(filter5, 'bayfiles-temp.txt')
	saveToFileWithStrip(filter6, 'drive-temp.txt')

	os.remove("urls.txt")
	saveToFileWithStrip(filter1, 'urls.txt')
	saveToFileWithStrip(filter2, 'urls.txt')

def scrapeCloudLinks(web):
	lines = readFile('urls.txt')

	mylist = scrapePage(web, lines, "")

	os.remove("temp.txt")
	saveToFile(mylist, 'temp.txt')
	lines = readFile('temp.txt')
	filter1 = filter(lambda x: x.startswith("https://mega.nz/"), lines)
	filter2 = filter(lambda x: x.startswith("https://anonfiles.com/"), lines)
	filter3 = filter(lambda x: x.startswith("https://bayfiles.com/"), lines)
	filter4 = filter(lambda x: x.startswith("https://drive.google.com/"), lines)
	
	saveToFileWithStrip(filter1, 'mega-temp.txt')
	saveToFileWithStrip(filter2, 'anonfiles-temp.txt')
	saveToFileWithStrip(filter3, 'bayfiles-temp.txt')
	saveToFileWithStrip(filter4, 'drive-temp.txt')

	os.remove("urls.txt")
	os.remove("temp.txt")

def removeDuplicate(final, temp, completed_lines_hash):
	output_file = open(final, 'a')
	lines = readFile(temp)
	for line in lines:
		hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
		if hashValue not in completed_lines_hash:
			output_file.write(line)
			completed_lines_hash.add(hashValue)
	output_file.close()
	
def removeDuplicates():
	completed_lines_hash = set()
	removeDuplicate('mega-urls.txt', 'mega-temp.txt', completed_lines_hash)
	removeDuplicate('anonfiles-urls.txt', 'anonfiles-temp.txt', completed_lines_hash)
	removeDuplicate('bayfiles-urls.txt', 'bayfiles-temp.txt', completed_lines_hash)
	removeDuplicate('drive-urls.txt', 'drive-temp.txt', completed_lines_hash)
	os.remove("mega-temp.txt")
	os.remove("anonfiles-temp.txt")
	os.remove("bayfiles-temp.txt")
	os.remove("drive-temp.txt")


print("launching browser...\n")
web = Browser()
print("logging in...\n")
login(web)
print(f'scraping threads from page {sys.argv[1]} to page {sys.argv[2]}...\n')
scrapeThreads(web, int(sys.argv[1]), int(sys.argv[2]))
print("scraping leak links from scraped threads...\n")
scrapeLeakLinks(web)
print("scraping cloud links from leak links...\n")
scrapeCloudLinks(web)
print("removing duplicate links...\n")
removeDuplicates()
print("ALL DONE, see mega-urls.txt, anonfiles-urls.txt and bayfiles-urls.txt in current dir!\n")
web.quit()




