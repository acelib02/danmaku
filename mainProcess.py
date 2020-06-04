import cdanmaku

if __name__ == '__main__':
    Dammaku = cdanmaku.cDammaku()
    Dammaku.setBV("BV1jC4y147rv")
    Dammaku.download_page()
    Dammaku.analasis()
    for eachday in Dammaku.date:
        content = Dammaku.getDailyDammaku(eachday)
        DMdata = Dammaku.formatDammaku(content)
        Dammaku.writeCSV(DMdata)
    print('over')