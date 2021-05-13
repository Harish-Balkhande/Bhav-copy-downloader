from django.shortcuts import render, HttpResponse
from .models import BhavData
import requests, zipfile, io, os, csv
from csv import DictReader
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import json
import datetime
from bs4 import BeautifulSoup

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

def background_task():
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
        # with open("E:/python zip download/Bhav_copy.ZIP","wb") as myfile:
        with open("bhav/downloads/Bhav_copy.ZIP","wb") as myfile:
            for chunk in r.iter_content(chunk_size=128):
                # writing one chunk at a time to pdf file
                if chunk:
                    myfile.write(chunk)
        # Extracting downloaded file
        # with zipfile.ZipFile("E:/python zip download/Bhav_copy.ZIP","r") as zip_ref:
        with zipfile.ZipFile("bhav/downloads/Bhav_copy.ZIP","r") as zip_ref:
            zip_ref.extractall("bhav/downloads")
            archeive = zip_ref.namelist()
            old_name = "bhav/downloads/"+str(archeive[0])
            os.rename(old_name, "bhav/downloads/bhavcopy.csv")
        os.remove("bhav/downloads/Bhav_copy.ZIP")
        

def Save_BhavData(request):
    with open('E:/python zip download/EQ030521.csv', mode='r') as read_obj:
        csv_reader = DictReader(read_obj)
        for row in csv_reader:
            code = row['SC_CODE']
            name = row['SC_NAME']
            open_field = row['OPEN']
            high = row['HIGH']
            low = row['LOW']
            close = row['CLOSE']
            # print(code,name,open_field,high,low,close)
            # radis = {'code':code,'name':name,'open':open,'high':high,'low':low,'close':close}
            # print(radis)
            reg = BhavData(code=code,name=name,open=open_field,high=high,low=low,close=close)
            reg.save()
            cache.clear()            
    return HttpResponse("Data saved Successfully")

def Show_data(request):    
    if 'Data' in cache:
        # get results from cache
        cache_data = cache.get('Data')
        received = json.loads(cache_data)
        # print(received)
        print("Data from cache=======================")
        return render(request, "bhav/showdata.html", {'data':received})    
 
    else:
        DB_data = BhavData.objects.all()       
        results = [cacheData.to_json() for cacheData in DB_data]
        # print(results)
        str_data = json.dumps(results)
        # store data in cache
        cache.set('Data', str_data, timeout=CACHE_TTL)
        print("Data from DB=======================")
        return render(request, "bhav/showdata.html", {'data':results})
        