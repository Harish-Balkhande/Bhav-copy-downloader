from django.shortcuts import render, HttpResponse
# from .models import BhavData
import requests, zipfile, io, os, csv
from csv import DictReader
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
from django.core.cache import cache
import json
# import datetime
from bs4 import BeautifulSoup
from .forms import search_form
# RegEx
import re

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

def background_task(request):
    # Web scrapping to get link
    url = 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'
    r = requests.get(url, stream = True,headers={'User-Agent': 'Chrome/90.0.4430.93'},allow_redirects=True)
    html_content = r.content
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor = soup.find('a', id="ContentPlaceHolder1_btnhylZip")
    link = anchor.get('href')
    # Downloading file
    r = requests.get(link, stream = True,headers={'User-Agent': 'Chrome/90.0.4430.93'},allow_redirects=True)
    print(r.status_code)
    # Save the equity file
    if r.status_code == 200:        
        with open("bhav/downloads/Bhav_copy.ZIP","wb") as myfile:
            for chunk in r.iter_content(chunk_size=128):
                # writing one chunk at a time to pdf file
                if chunk:
                    myfile.write(chunk)
        
        with zipfile.ZipFile("bhav/downloads/Bhav_copy.ZIP","r") as zip_ref:
            zip_ref.extractall("bhav/downloads")
            archeive = zip_ref.namelist()
            old_name = "bhav/downloads/"+str(archeive[0])
            os.rename(old_name, "bhav/downloads/bhavcopy.csv")
        os.remove("bhav/downloads/Bhav_copy.ZIP")


    # Cashe data into redis from downloaded bhav copy
    with open('bhav/downloads/bhavcopy.csv', mode='r') as read_obj:
        csv_reader = DictReader(read_obj)
        data = []
        for row in csv_reader:
            code = row['SC_CODE']
            name = row['SC_NAME']
            open_field = row['OPEN']
            high = row['HIGH']
            low = row['LOW']
            close = row['CLOSE']            
            redis = {'code':code,'name':name,'open':open_field,'high':high,'low':low,'close':close}            
            cache.clear()            
            data.append(redis)
        
        cache_str = json.dumps(data)
        # print(cache_str)
        cache.set('Data', cache_str, timeout=CACHE_TTL)
    os.remove("bhav/downloads/bhavcopy.csv")
    # return HttpResponse(cache_str)
    

def Show_data(request):    
    if 'Data' in cache:
        # get results from cache
        cache_data = cache.get('Data')
        received = json.loads(cache_data)
        # print(received)
        print("Data from cache=======================")
        
    else:
        background_task(request)
        cache_data = cache.get('Data')
        received = json.loads(cache_data)
    fm = search_form()
    return render(request, "bhav/showdata.html", {'data':received, 'form':fm})

 
def search_data(request):
    if request.method == "GET":        
        fm = search_form(request.GET)
        print("request received")
        if fm.is_valid():
            sch = fm.cleaned_data.get('search_key')
            cache_data = cache.get('Data')
            received = json.loads(cache_data)
            # RegEx for search
            lst = []
            for dic in received: 
                if sch.isnumeric():   
                    num = dic['code'].strip().lower()
                    x = re.findall("^"+sch, num)
                    if x:
                        lst.append(dic)
                        print("num : ",lst)
                        
                else:
                    st = dic['name'].strip().lower()        
                    x = re.findall("^"+sch, st)        
                    if x:
                        lst.append(dic)
                        print("str : ",lst)
            # return HttpResponse(lst)
            fm = search_form()      
            return render(request, "bhav/showdata.html", {'data':lst, 'form':fm})