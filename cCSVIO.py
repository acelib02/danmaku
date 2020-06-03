import csv

class cCSVIO():
    # 基础属性
    CSVfile = 'danmaku.csv'
    Headers = ['videotime','mode','size','color','unixtime','pool','UID','rowID','content']
    # 基础方法

    def writeCSV(self,data):
        with open(self.CSVfile,'w',encoding='utf-8',newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.Headers)
            for each in data:
                f_csv.writerow(each)

    def readCSV(self):
        with open(self.CSVfile,'r',encoding='utf-8') as f:
            f_csv = csv.reader(f)
            data = []
            for row in f_csv:
                data.append(row)
        return data

    def showheaders(self):
        print('CSV Header:\n')
        print(self.Headers)

    def getheaders(self):
        return self.Headers
