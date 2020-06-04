import requests
from lxml import etree
import re
from datetime import datetime
import cCSVIO


class cdanmaku(cCSVIO.cCSVIO):
    # 弹幕爬取功能
    BaseURL = "https://www.bilibili.com/video/"
    BV = 'BV1jC4y147rv'
    cidAPI = "https://www.bilibili.com/widget/getPageList?"
    danmakuAPI = "https://api.bilibili.com/x/v2/dm/history?type=1&oid="
    aid = ''
    cid = ''
    cookies = {'Cookie':'l=v; _uuid=161EFE2D-9E65-07CC-48AB-B05C22DBD14605163infoc; '
                      'buvid3=F344B872-1819-42F6-BF91-78D7585D12E6155825infoc; '
                      'sid=k22lp5mw; DedeUserID=148778; '
                      'DedeUserID__ckMd5=9a668543a86a159d; '
                      'SESSDATA=d43071b3%2C1605362566%2C672d8*51; '
                      'bili_jct=de4c0f7c0f711fbb455df4c640e036a0; '
                      'PVID=1'}
    Today = ''
    date = []
    htmldata = ''

    def __init__(self):
        self.showheaders()
        self.Today = datetime.today().date()
        self.date = [self.Today]

    def setBV(self, bv):
        if not bv:
            self.BV = "BV1jC4y147rv"
        else:
            self.BV = bv
        self.showBV()

    def showBV(self):
        print('BV: '+self.BV)

    def download_page(self):
        url = self.BaseURL + self.BV
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        self.htmldata = requests.get(url, headers=headers).text

    def analasis(self):
        if not self.htmldata:
            self.download_page()
        self.aid = re.findall(r'aid=\d*', self.htmldata)[0]
        cjson = requests.get(self.cidAPI + self.aid).json()
        self.cid = cjson[0]['cid']

    def getDailydanmaku(self, date):
        djson = requests.get(self.danmakuAPI+str(self.cid)+'&date='+str(date), cookies=self.cookies).content
        content = etree.HTML(djson)
        return content

    def formatdanmaku(self, content):
        data = []
        for each in content.xpath('//d'):
            a = each.xpath('@p')[0].split(',')
            b = str(each.xpath('text()')[0])
            b.encode('utf-8')
            a.append(b)
            a[0] = float(a[0])
            a[1:5] = [int(a) for a in a[1:5]]
            data.append(a)
        return data

    def mainProcess(self, bv):
        self.setBV(bv)
        self.download_page()
        self.analasis()
        content = self.getDailydanmaku(self.Today)
        DMdata = self.formatdanmaku(content)
        self.writeCSV(DMdata)
        print('over')

if __name__ == '__main__':
    danmaku = cdanmaku()
    danmaku.mainProcess('BV17Z4y1p7o3')
