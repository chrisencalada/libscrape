#scraping infrastructre. Request -> parse -> save?
#store content from request with open() method
# if you open a file, always remember to close it with the close() method

from __future__ import print_function
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import random
from bs4 import BeautifulSoup
from time import sleep
import json
from urllib.request import urlopen
import re

#make function that uses the proxies and user agent spoofing to scrape website

#optimize scraping and prevent blacklisting
#1. rotate through proxies
proxies = {'http': 'socks5h://x1566907:b63SAHfRsG@proxy-nl.privateinternetaccess.com:1080',
           'https': 'socks5h://x1566907:b63SAHfRsG@proxy-nl.privateinternetaccess.com:1080'}



#2. rotate and spoof user agents
user_agent =  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
#3. Use headless browsers???
#4. reduce crawl rate
#5. rotate through different libgen mirrors

#scraping function

url = 'http://gen.lib.rus.ec/search.php?req=murakami&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def&page=1'
#url = 'https://libgen.is/search.php?req=murakami&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def'
#url = 'https://en.wikipedia.org/wiki/Syriana'
#url = 'https://httpbin.org/ip'
s= requests.Session()
retry = Retry(connect = 1)#,backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
s.mount('https://',adapter)
s.mount('http://',adapter)
headers = {'User-Agent':user_agent}
r = s.get(url,headers=headers,proxies=proxies)
soup = BeautifulSoup(r.content,'html.parser')
all_rows = soup.select('.c tr')

link_relay = []
data = []

for selection in all_rows:
#select_rows = all_rows[1]
    text = selection.select('td')#('a[href]')
    urls = selection.find_all('a',href=re.compile('^http://'))
    #iterate over each row that we get from rows variable
    names = []
    
    for row in text:
        if '[1]' in row.text:
            url = urls[0]
            urls_2 = url['href']
            s= requests.Session()
            retry = Retry(connect = 1)#,backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            s.mount('https://',adapter)
            s.mount('http://',adapter)
            headers = {'User-Agent':user_agent}
            response = s.get(urls_2,headers=headers,proxies=proxies)
            soup_2 = BeautifulSoup(response.content,'html.parser')
            urls_3 = soup_2.find('a',href=True)
            attr = urls_2.split('_')[0]
            attr= attr[:-1]
            full_url = attr + urls_3['href']
            names.append(full_url)
            #link_relay.append(url['href'])
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

print(dictList)

#download_links=[]
#print(link_relay)
'''
for n in link_relay:
    s= requests.Session()
    retry = Retry(connect = 1)#,backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('https://',adapter)
    s.mount('http://',adapter)
    headers = {'User-Agent':user_agent}
    response = s.get(n,headers=headers,proxies=proxies)
    soup_2 = BeautifulSoup(response.content,'html.parser')
    urls = soup_2.find('a',href=True)
    download_links.append(urls['href'])


print(download_links)
'''


#def save_html(html, path):
#    with open(path, 'wb') as f:
#        f.write(html)

#save_html(r.content,'scraped_object')