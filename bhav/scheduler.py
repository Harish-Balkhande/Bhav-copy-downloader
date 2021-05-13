# import requests, zipfile, io, os, csv
# from bs4 import BeautifulSoup

# def background_task():
#  # Web scrapping to get link
#     url = 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'
#     r = requests.get(url, stream = True,headers={'User-Agent': 'Chrome/90.0.4430.93'},allow_redirects=True)
#     html_content = r.content
#     soup = BeautifulSoup(html_content, 'html.parser')
#     anchor = soup.find('a', id="ContentPlaceHolder1_btnhylZip")
#     link = anchor.get('href')
#     # Downloading file
#     r = requests.get(link, stream = True,headers={'User-Agent': 'Chrome/90.0.4430.93'},allow_redirects=True)
#     print(r.status_code)
#     # Save the equity file
#     if r.status_code == 200:        
#         with open("bhav/downloads/Bhav_copy.ZIP","wb") as myfile:
#             for chunk in r.iter_content(chunk_size=128):
#                 # writing one chunk at a time to pdf file
#                 if chunk:
#                     myfile.write(chunk)
        
#         with zipfile.ZipFile("bhav/downloads/Bhav_copy.ZIP","r") as zip_ref:
#             zip_ref.extractall("bhav/downloads")
#             archeive = zip_ref.namelist()
#             old_name = "bhav/downloads/"+str(archeive[0])
#             os.rename(old_name, "bhav/downloads/bhavcopy.csv")
#         os.remove("bhav/downloads/Bhav_copy.ZIP")

# background_task()