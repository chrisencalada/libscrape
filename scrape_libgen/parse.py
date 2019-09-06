
import requests
from bs4 import BeautifulSoup
import json

def open_html(path):
    with open(path, 'rb') as f:
        return f.read()
    
    
html = open_html('scraped_object')


#pass request object to beautiful soup and parse html
soup = BeautifulSoup(html.decode("utf-8"),'html.parser')

#selecting the table class in libgen website
############################################################################
#1.parse all books for given search criteria

all_rows = soup.select('.c tr')


data = []

for selection in all_rows:
#select_rows = all_rows[1]
	text = selection.select('td')#('a[href]')
	urls = selection.find_all('a',href=True)
	#iterate over each row that we get from rows variable
	names = []
	
	for row in text:
		if '[1]' in row.text:
			url = urls[2]
			names.append(url['href'])
		else:
			names.append(row.text)
	#[names.append(urls[2]) if '[1]' in row.text  else names.append(row.text) for row in text]
	data.append(names)
	#data.append(links)

dictList = [{k:v for k,v in zip(data[0],n)} for n in data]
dictList = dictList[1:]

for dick in dictList:
	for key,value in dick.items():
		if value == '':
			dick[key] = 'NaN'

#print(len(dictList))
print(dictList)

#def save_html(html, path):
#    with open(path, 'w') as f:
#        json.dump(html, f)

#save_html(dictList,'book_dict')

############################################################################S
#2. display given data in django as a drop down list?


#TO-DO
#1. Mirror support
#2. API research