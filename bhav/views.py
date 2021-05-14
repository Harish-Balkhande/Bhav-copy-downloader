from django.shortcuts import render, HttpResponse
from django.core.cache import cache
import json
from .forms import search_form
import re #RegEx
from .scheduler import background_task

# Render data to table
def Show_data(request):    
    if 'Data' in cache:        
        cache_data = cache.get('Data')
        received = json.loads(cache_data)        
        
    else:
        background_task()
        cache_data = cache.get('Data')
        received = json.loads(cache_data)
    fm = search_form()
    return render(request, "bhav/showdata.html", {'data':received, 'form':fm})

# search the records on the basis of code or Name of the table column
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
            fm = search_form()      
            return render(request, "bhav/showdata.html", {'data':lst, 'form':fm})