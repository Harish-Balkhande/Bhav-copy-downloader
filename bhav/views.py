from django.shortcuts import render, HttpResponse
from .models import BhavData
import requests, zipfile, io, os, csv
from csv import DictReader

# file_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ030521_CSV.ZIP"
# r = requests.get(file_url, stream = True,headers={'User-Agent': 'Chrome/90.0.4430.93'})
# print(r.status_code)
# # Save the equity file
# if r.status_code == 200:
#     with open("E:/python zip download/EQ030521_CSV.ZIP","wb") as myfile:
#         for chunk in r.iter_content(chunk_size=128):
#             # writing one chunk at a time to pdf file
#             if chunk:
#                 myfile.write(chunk)
#     # Extracting downloaded file            
#     with zipfile.ZipFile("E:/python zip download/EQ030521_CSV.ZIP","r") as zip_ref:
#         zip_ref.extractall("E:/python zip download")
#     os.remove("E:/python zip download/EQ030521_CSV.ZIP")

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
            print(code,name,open_field,high,low,close)
            # radis = {'code':code,'name':name,'open':open,'high':high,'low':low,'close':close}
            # print(radis)
            reg = BhavData(code=code,name=name,open=open_field,high=high,low=low,close=close)
            reg.save()
            # contex = {'code':code,'name':name,'open':open_field,'high':high,'low':low,'close':close}
    return HttpResponse("Data saved Successfully")

def Show_data(request):
    current_data = BhavData.objects.all()
    return render(request, "bhav/showdata.html", {'data':current_data})
    
