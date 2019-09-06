from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect
from django.utils import timezone
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import random
from bs4 import BeautifulSoup
from time import sleep
import json
from urllib.request import urlopen
import re
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from .models import Books
import logging
import time
from multiprocessing import Pool
from multiprocessing import cpu_count
from django.db.models import Count

#cleanup
#1. clean-up variable names
#2.move functions to a function file

#core
#1. if more than 10 pages of results our if statement doesn't work anymore
#1. check why sometimes you get nonetype failures
#NoneType' object is not subscriptable
#1. clean up the author names so that same name does not show as distinct
#3. mass download link? 
#4. add a function to expire stale data
#5. set up a data pipeline to download weekly data dumps from libgen and load them into database
#6. host this online??
#7. fix mirror site logic (download all 5 mirrors? then loop through them until you find one that doesnt 503?) 

logger = logging.getLogger(__name__)

def request_multithread(dictList):
    sessions = requests.Session()
    response = sessions.get(dictList['Mirrors'])
    if response.status_code == 200:
        soup_2 = BeautifulSoup(response.text,'html.parser')
        urls_3 = soup_2.find('a',href=True)
        if urls_3 is None:
            pass
        else:
            attr = dictList['Mirrors'].split('_')[0]
            attr = attr[:-1]
            dictList['Mirrors'] = attr + urls_3['href']
    else:
        dictList['Mirrors'] = response.status_code

    return dictList


def request_with_proxies(url,s,payload):
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

def scrape_1(input_author):
    #open requests session outside of the loop to keep-alive for all page requests
    s = requests.Session()
    all_data = []
    for page in range(1,10,1):
        logger.error('page' + str(page))
        url = 'http://gen.lib.rus.ec/search.php?'
        payload = {"req":input_author,"page":page,"res":100,"phrase":1}
        
        start = time.time()
        r = request_with_proxies(url,s,payload)
        end = time.time()
        logger.error('requesting' +' '+ str(end-start))
        
        soup = BeautifulSoup(r.text,features='html5lib')
        table = soup.select('.c')[0]
        rows = table.findAll('tr')
        if len(rows) == 1:
            return all_data
        all_rows = soup.select('.c tr')

        start = time.time()
        for selection in all_rows:
            text = selection.select('td')
            urls = selection.find_all('a',href=re.compile('^http://'))
            #iterate over each row that we get from rows variable
            names = []
            
            for row in text:
                if '[1]' in row.text:
                    url = urls[0]
                    urls_2 = url['href']

                    names.append(urls_2)
                else:
                    names.append(row.text)
            
            all_data.append(names)
        end = time.time()
        logger.error('sub-requests' +' '+ str(end-start))

    return all_data

def makes_list_d(input_author):
    sessions = requests.Session()
    data = scrape_1(input_author)
    start = time.time()
    dictList = [{k:v for k,v in zip(data[0],n)} for n in data]
    dictList[:] = [d for d in  dictList if d.get('Mirrors') != 'Mirrors']

    
    pool = Pool(cpu_count()*2)
    dictList = pool.map(request_multithread,dictList)
    
    for dick in dictList:
        for key,value in dick.items():
            if value == '':
                dick[key] = 'NA'
    end = time.time()
    logger.error('dict' +' '+ str(end-start))
    
    return dictList

class AuthorForm(forms.Form):
    A_Name = forms.CharField(label='Author Name',max_length=100)

#@csrf_exempt
def Author(request):
    submitted = False
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            # add book name search functionality
            cd = form['A_Name'].value()
            start = time.time()
            check = makes_list_d(cd)
            end = time.time()
            logger.error('total'+' ' +str(end-start))
            hold = check

            #2.
            for x in hold:
                p = Books(
                ID=x['ID'],
                Author=x['Author(s)'],
                Title=x['Title'],
                Publisher=x['Publisher'],
                Year_published=x['Year'],
                num_Pages=x['Pages'],
                Language=x['Language'],
                Size=x['Size'],
                Extension=x['Extension'],
                Mirrors=x['Mirrors'],
                Edit=x['Edit'],
                created_at =timezone.now()
                )
                p.save()
            #3. return only a distinct list of authors whose name matches entered name
            
            #assert False
            return render(request,'downloads/index.html',{'name':Books.objects.values('Author').filter(Author__contains=cd).distinct().annotate(Title_count=Count('Title'))})
    else:
        form = AuthorForm()
        if 'submitted' in request.GET:
            submitted = True

    #send it to appropriate views file that will use form data
    return render(request,'downloads/landing.html',{'form': form, 'submitted':submitted})


