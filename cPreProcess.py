from cCSVIO import cCSVIO
import pandas as pd

class CPreProcess(cCSVIO):
    PPedCSV = 'PP.csv'
    rawdata = []
    merged = []
    meta = {}
    callength = []
    def __init__(self):
        rawdata = self.readCSV()
        self.rawdata = pd.DataFrame(rawdata[1:], columns=rawdata[0])

    def mergecontent(self):
        self.merged = self.rawdata.content.value_counts().rename_axis('content').reset_index(name='count')

    def callen(self):
        if self.merged.empty:
            self.mergecontent()
        self.callength = self.merged[0].apply(len)
        print(self.callength)
        self.callength = self.merged + self.callength
        print(self.callength)

if __name__ == '__main__':
    test = CPreProcess()
    # print(test.rawdata)
    test.mergecontent()
    merged = test.merged
    print(merged)
    # print(test.rawdata)
    # test.callen()
    # print(test.merged)