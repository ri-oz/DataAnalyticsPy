

# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re


# %%

def getUrlList(url, prefix='https://www.ss.com', postfix='sell/', tag='a', class_='a_category'):
    req = requests.get(url)
    if req.status_code != 200:
        print(f'Unexpected status code {req.status_code}. Stopping parse')
        return [] #return early and often principle
    soup = BeautifulSoup(req.text, 'lxml') # could skip soup variable as well but keeping for readability
    return [ prefix + el['href'] + postfix for el in soup.find_all(tag, class_) ]
    # What else could we pass as argument? How could our return fail?
    

def processRow(row, baseurl='https://www.ss.com'):
    ritems = []
    tds = row.find_all('td')
    ritems.append(baseurl + tds[1].a['href'])
    ritems.append(tds[2].text.strip().replace('\r','').replace('\n', ''))
    for td in tds[3:-1]:
        ritems.append(td.text)
    ritems.append(int(tds[-1].text.split()[0].replace(',','')))
    ritems.append(tds[-1].text.split()[1])
    return ritems

def processRows(rows):
    rowlist=[]
    for row in rows:
        rowlist.append(processRow(row))
    return rowlist


def getRows(url):
    req = requests.get(url)
    rows = []
    if req.status_code != 200:
        print("Bad Request"+req.status_code)
        return
    soup = BeautifulSoup(req.text, 'lxml')
    print("Processing: "+ str(soup.title))
    # this will be specific to ss.lv and ss.com
    alltrs = soup.find_all('tr')
    for el in alltrs:
        if 'id' in el.attrs and 'tr_' in el.attrs['id']:
            rows.append(el)
    rows = rows[:-1] # we do not need the last one nor do we need to store
    return rows


def processPage(url):
    rows = getRows(url)
    mylist = processRows(rows)
    return mylist # could return processRows(rows)


def processPages(urls):
    results = []
    for url in urls:
        print("Processing: "+url)
        results += processPage(url)
        time.sleep(0.1)
    return results


# %%

url = "https://www.ss.lv/lv/real-estate/plots-and-lands/"


# %%

mylist = processPages(getUrlList(url))
len(mylist)


# %%


dfmylist = pd.DataFrame(mylist)

adw_list = dfmylist[0].tolist()
# %%
