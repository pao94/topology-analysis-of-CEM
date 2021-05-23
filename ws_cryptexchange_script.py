"""
Created on Fri Dec 28 15:21:35 2018
@author:
Aim of script is to get all relevant crypto exchange platform URL's and 
identify their AS ID.
Export to CSV with the objective to use for network analytics.
"""

from requests import get
from requests import post
from bs4 import BeautifulSoup
import pandas as pd
import time
import socket
import re




def main():
    global df
    
    df = crawl()    
    df['ip'] = df.apply(lambda row: getIP(row),axis=1)
    df.to_csv('./ips.csv',index = False)
    df['asn'] = df.apply(lambda row: getASN(row.ip), axis = 1)
    df.to_csv('./asn.csv',index = False)
    df['asn2'] = df.apply(lambda row: getASN2(row.ip), axis = 1)
    df.to_csv('./asn2.csv',index = False)
    df['crosscheck'] = df.apply(lambda row: crosscheck(row), axis = 1)
    df = df.fillna(0)
    df.asn = df.asn.astype('int64')
    df.to_csv('./crosschecked.csv',index = False)   

def crosscheck(row):
    if row.asn == row.asn2:
        return True
    else:
        return False

def getASN2(targetip):
    url = 'https://traceroute-online.com/ip-asn-lookup/'
    headers = {
    #"Connection": "keep-alive",
    #"Content-Length": 129,
    "Origin": "https://traceroute-online.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #"Accept": "*/*",
    "Referer": "https://traceroute-online.com/ip-asn-lookup/",
    #"Accept-Encoding": "gzip,deflate,sdch",
    #"Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
    #"Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Cookie": "_cfduid=d8e23cac28fd39df56e2ad0cf241a5b211546522071; csrftoken=oLba5l6YRivh0elUFUDAqUXqH4MZyqOy; _ga=GA1.2.1855903888.1546522075; _gid=GA1.2.1412935247.1547319788; _gat=1",
    }
    
    payload = {"csrfmiddlewaretoken":"oLba5l6YRivh0elUFUDAqUXqH4MZyqOy",
    "targetip":targetip}
    r = post(url, data = payload, headers=headers)
    time.sleep(4)
    html = BeautifulSoup(r.content, "html.parser")
    try:
        asn = int(html.find('div', {'class':'box-body'}).text.split(',')[1].replace('"',''))
    except Exception as e:
        print(e)
        asn = None
    return asn

def getASN(row):
    try:
        url = 'https://www.ultratools.com/tools/asnInfoResult?domainName='+row
        resp = getUrl(url)
        time.sleep(4)
        html = BeautifulSoup(resp.content, 'html.parser')
        asn = int(html.find('div', {'class':'tool-results-heading'}).text.replace('AS',''))
        return asn
    except Exception as e:
        
        print(e)
        return None


def getIP(row):
    if row.siteUrl.count('/') >2: 
        try:
            found = re.search('//(.+?)/', row.siteUrl).group(1)
        except AttributeError:
          	found = 'Not Found.' # apply error handling
    else:
        try:
            found = re.findall('//(.*)', row.siteUrl)[0]
        except AttributeError:
            found = 'Not Found.' # apply error handling
    
    try: 
        print(found)
        resp = socket.gethostbyname(found)
    except Exception as e:
        print(e)
        resp = None
    
    if resp is not None:
        return resp

def getUrl(url):
    try:
        print("Perform HTTP GET request on: ", url)
        ans = get(url, stream = True)
        if ans.headers['Content-Type'].lower() is not None and ans.status_code == 200:# and ans.headers['Content-Type'].lower().find('html') > -1:
             return ans
        else:
            print("smth went wrong")
    except Exception as e:
        print(e)


def crawl():
    global dfs
    dfs = []
    for i in range(1,4):
        print(i)
        url = "https://coinmarketcap.com/rankings/exchanges/"+str(i)
        ans = getUrl(url)
        html = inspectFile(ans.content)
        df = getInfo(html)
        dfs.append(df)
        
    dfs = pd.concat(dfs, sort = False)
    dfs.to_csv('./out.csv',index = False)
    return dfs

def inspectFile(content):
    try:
        html = BeautifulSoup(content, 'html.parser')
        table_body = html.find('tbody')
        rows = table_body.find_all('td', {'class':'no-wrap currency-name'})
    except Exception as e:
        print(e)
    return rows

def getInfo(rows):
    
    names = []
    urls = []
    siteUrls = []
    try:
        for i in range(0,len(rows)):
            data = rows[i].text.strip()
            name = data
            names.append(name)
            tmp = rows[i].find('a').get('href')
            url = "https://coinmarketcap.com" + tmp
            urls.append(url)
            time.sleep(4)
            site = getUrl(url)
            insides = site.content
            getHTML = BeautifulSoup(insides, 'html.parser')
            links = getHTML.find('div', {"class":'col-xs-12'})
            
            links = links.find_all('a')
            print(links[0].text)
            siteUrls.append(links[0].text)
            time.sleep(4)
    except Exception as e:
        print(e)
    myData = {"name" : names, "siteUrl" : siteUrls}
    myData = pd.DataFrame.from_dict(myData)
    return myData
        
main()