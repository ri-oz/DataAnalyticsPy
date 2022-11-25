

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


url = "https://www.ss.lv/lv/real-estate/plots-and-lands/"


# %%

mylist = processPages(getUrlList(url))

dfmylist = pd.DataFrame(mylist)

adw_list = dfmylist[0].tolist()


def get_ZemePrice(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    price_detail_soup = soup_adv_text_html.find(id="tdo_8")
    
    if price_detail_soup == None:
         adv_price = "NA"
    else:
        adv_price = price_detail_soup.get_text()
        
    return adv_price




def get_ZemePielietojums(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    pielietojums_detail_soup = soup_adv_text_html.find(id="tdo_228")
    
    if pielietojums_detail_soup == None:
         adv_pielietojums = "NA"
    else:
        adv_pielietojums = pielietojums_detail_soup.get_text()
        
    return adv_pielietojums



def get_Zemeplatiba(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    platiba_detail_soup = soup_adv_text_html.find(id="tdo_3")
    
    if platiba_detail_soup == None:
         adv_platiba = "NA"
    else:
        adv_platiba = platiba_detail_soup.get_text()
        
    return adv_platiba



def get_ZemeKnumurs(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    Knumurs_detail_soup = soup_adv_text_html.find(id="tdo_1631")
    
    if Knumurs_detail_soup == None:
         adv_Knumurs = "NA"
    else:
        adv_Knumurs = Knumurs_detail_soup.get_text()
        
    return adv_Knumurs



def get_ZemePilseta(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    Pilseta_detail_soup = soup_adv_text_html.find(id="tdo_20")
    
    if Pilseta_detail_soup == None:
         adv_Pilseta = "NA"
    else:
        adv_Pilseta = Pilseta_detail_soup.get_text()
        
    return adv_Pilseta



def get_ZemeIela_nosaukums(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    Iela_nosaukums_detail_soup = soup_adv_text_html.find(id="tdo_11")
    
    if Iela_nosaukums_detail_soup == None:
         adv_Iela_nosaukums = "NA"
    else:
        adv_Iela_nosaukums = Iela_nosaukums_detail_soup.get_text()
        
    return adv_Iela_nosaukums



def get_datums(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    datums_detail_soup = soup_adv_text_html.findAll(text=re.compile('Datums:'))
        
    return datums_detail_soup



# %%

get_datums("https://www.ss.lv/msg/lv/real-estate/plots-and-lands/dobele-and-reg/dobele/bbohx.html")


# %%



odel_list = []
year_list = []
transm_list = []
btyp_list = []
color_list = []
price_list = []
motor_list = []
milige_list = []
link_list = addlist_new
apriko_list = []
seats_list = []
dates_list = []


for items in addlist_new:
    
    response = requests.get('https://www.ss.com/msg/lv/transport/cars/dacia/'+str(items))
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    model_detail_soup = soup_adv_text_html.find(id="tdo_31")
    
    if model_detail_soup == None:
         adv_model = "NA"
    else:
        adv_model = model_detail_soup.get_text()
    
    model_list.append(adv_model)