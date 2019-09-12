import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from time import sleep
import json
from urllib.request import urlopen
import re
from multiprocessing import Pool
from multiprocessing import cpu_count
import logging
import time



logger = logging.getLogger(__name__)


def request_multithread(booklist):
    sessions = requests.Session()
    proxies = {'http': 'socks5h://x1566907:b63SAHfRsG@proxy-nl.privateinternetaccess.com:1080',
    'https': 'socks5h://x1566907:b63SAHfRsG@proxy-nl.privateinternetaccess.com:1080'}
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    headers = {'User-Agent':user_agent}
    response = sessions.get(booklist['Mirrors'], proxies=proxies,headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,features='html5lib')
        pathname = soup.find('a',href=True)
        if pathname:
            sld = booklist['Mirrors'].split('_')[0]
            sld = sld[:-1]
            booklist['Mirrors'] = sld + pathname['href']
    else:
        #change to get second mirror?
        booklist['Mirrors'] = response.status_code

    return booklist

def request_w_proxies(url,s,payload):
        proxies = {'http': 'socks5h://x1566907:b63SAHfRsG@proxy-nl.privateinternetaccess.com:1080',
                   'https': 'socks5h://x1566907:b63SAHfRsG@proxy-nl.privateinternetaccess.com:1080'}

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        s= s
        #retry = Retry(connect = 4)#,backoff_factor=0.5)
        #adapter = HTTPAdapter(max_retries=retry)
        #s.mount('https://',adapter)
        #s.mount('http://',adapter)
        headers = {'User-Agent':user_agent}
        r = s.get(url,headers=headers,proxies=proxies,params=payload)
        r.encoding = 'utf-8'


        return r

def scrape(input_author):
    #open requests session outside of the loop to keep-alive for all page requests
    s = requests.Session()
    book_list = []
    for page in range(1,10,1):
        logger.debug('page' + str(page))
        url = 'http://gen.lib.rus.ec/search.php?'
        payload = {"req":input_author,"page":page,"res":100,"phrase":1}
        
        start = time.time()
        r = request_w_proxies(url,s,payload)
        end = time.time()
        logger.error('requesting' +' '+ str(end-start))
        
        soup = BeautifulSoup(r.text,features='html5lib')
        if len(soup.select('.c')) < 1:
            return book_list
        else:
            table = soup.select('.c')[0]
            rows = table.findAll('tr')
        if len(rows) == 1:
            return book_list
        all_rows = soup.select('.c tr')

        start = time.time()
        for row in all_rows:
            text = row.select('td')
            urls = row.find_all('a',href=re.compile('^http://'))
            #iterate over each row that we get from rows variable
            cell_value = []
            
            for value in text:
                if '[1]' in value.text:
                    #first mirror url (need to scrape all mirrors and then check to see which works?)
                    url = urls[0]
                    urls_2 = url['href']

                    cell_value.append(urls_2)
                else:
                    cell_value.append(value.text)
            
            book_list.append(cell_value)
        end = time.time()
        logger.debug('sub-requests' +' '+ str(end-start))

    return book_list

def make_dict_get_urls(input_author):
    data = scrape(input_author)
    start = time.time()
    dictList = [{k:v for k,v in zip(data[0],n)} for n in data]
    dictList[:] = [d for d in  dictList if d.get('Mirrors') != 'Mirrors']
    #using multiprocessing to request the complete list of mirrors to get the actual download urls
    pool = Pool(cpu_count()*2)
    dictList = pool.map(request_multithread,dictList)
    #replace any blank records with NA
    for book in dictList:
        for key,value in book.items():
            if value == '':
                book[key] = 'NA'
    end = time.time()
    logger.debug('dict' +' '+ str(end-start))
    
    return dictList
