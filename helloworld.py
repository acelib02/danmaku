import requests
from bs4 import BeautifulSoup as BS
from lxml import etree
from requests import exceptions
import re
import csv
from datetime import datetime,timedelta

def download_page(url):
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    data = requests.get(url, headers=headers)
    return data

if __name__ == "__main__":
    BV = "BV1jC4y147rv"
    BaseUrl = "https://www.bilibili.com/video/"
    url = BaseUrl + BV
    data = download_page(url).text
    #print(data)
    res = re.findall('aid=\d*',data)
    print(res)

    cidAPI = requests.get('https://www.bilibili.com/widget/getPageList?aid=795002713')
    cjson = cidAPI.json()
    print(cjson)
    print(cjson[0]['cid'])

    dammaku = "https://api.bilibili.com/x/v2/dm/history?type=1&oid=173527223&date=2020-05-18"
    cookies={'Cookie':'l=v; _uuid=161EFE2D-9E65-07CC-48AB-B05C22DBD14605163infoc; '
                      'buvid3=F344B872-1819-42F6-BF91-78D7585D12E6155825infoc; '
                      'sid=k22lp5mw; DedeUserID=148778; '
                      'DedeUserID__ckMd5=9a668543a86a159d; '
                      'SESSDATA=d43071b3%2C1605362566%2C672d8*51; '
                      'bili_jct=de4c0f7c0f711fbb455df4c640e036a0; '
                      'PVID=1'}

    djson = requests.get(dammaku,cookies=cookies).content
    content = etree.HTML(djson)

    headers = ['videotime','mode','size','color','unixtime','pool','UID','rowID','content']
    f = open('dammaku.csv','w',encoding='utf-8')
    f_csv = csv.writer(f)
    f_csv.writerow(headers)

    for each in content.xpath('//d'):
        a = str(each.xpath('@p')[0]).split(',')
        b=str((each.xpath('text()')[0]))
        b.encode('utf-8')
        a.append(b)
        a[0] = float(a[0])
        a[1:6] = [int(a) for a in a[1:6]]

        print(a)
        f_csv.writerow(a)

    f.close()

    print(datetime.today().date())