import cdanmaku
from bs4 import BeautifulSoup as BS
from datetime import datetime,timedelta


class cdanmakuHistory(cdanmaku.cdanmaku):
    PostDate=''
    oneday = timedelta(days=1)
    maxday = 365
    def __init__(self):
        self.showheaders()
        self.Today = datetime.today().date()

    def getPostDate(self):
        if not self.htmldata:
            self.download_page()
        bs = BS(test.htmldata, 'html.parser')
        data = bs.find_all('div', class_='video-data')[0]
        PostDate = data.find_all('span')[1].text.split()[0]
        self.PostDate = datetime.strptime(PostDate, '%Y-%m-%d').date()

    def fufillDate(self):
        self.date = []
        day = self.Today
        if not self.PostDate:
            self.getPostDate()
        while day >= self.PostDate:
            self.date.append(str(day))
            day = day - self.oneday

    def getHistorydanmaku(self):
        HistoryDM=[]
        daycounter = 0
        if not self.date:
            self.fufillDate()
        for day in self.date:
            if daycounter >= self.maxday:
                break
            else:
                print(day)
                content = self.getDailydanmaku(day)
                data = self.formatdanmaku(content)
                HistoryDM = HistoryDM + data
                daycounter += 1
        return HistoryDM

    def mainProcess(self, bv):
        self.setBV(bv)
        self.analasis()
        DMdata = self.getHistorydanmaku()
        self.writeCSV(DMdata)
        print('over')

    def setMaxday(self, maxday):
        self.maxday = maxday


if __name__ == '__main__':
    test = cdanmakuHistory()
    # test.setMaxday(15)
    test.mainProcess('BV15K411W7HN')
