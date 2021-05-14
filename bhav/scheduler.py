from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

from django.conf import settings
import requests, zipfile, io, os, csv
from csv import DictReader
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
import json
from bs4 import BeautifulSoup

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

# --------This function downloads bhav copy and store it into the redis -----------
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
    if r.status_code == 200:        
        with open("bhav/downloads/Bhav_copy.ZIP","wb") as myfile:
            for chunk in r.iter_content(chunk_size=128):                
                if chunk:
                    myfile.write(chunk)
        # Extracting zip file & rename the archeived file
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
        cache.set('Data', cache_str, timeout=CACHE_TTL)
    os.remove("bhav/downloads/bhavcopy.csv")


def start():
    jobstores = {
        # 'mongo': {'type': 'mongodb'},
        'default': SQLAlchemyJobStore(url='sqlite:///db.sqlite3')  
        
    }
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='Asia/kolkata')
    scheduler.add_job(
            background_task, 'cron', day_of_week='*', hour=18, minute=00,
            id="scheduler_id",
            max_instances=1,
            replace_existing=True,
        ) 
    
    scheduler.start()