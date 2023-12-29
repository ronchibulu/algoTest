import sys
sys.path.insert(0, "./Fundamental")
import csv
import os
import pandas_datareader as pd
import datetime as dt
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ib_insync import *
import nest_asyncio
from fundamental import fundamental as fd

def hisData():
    curDate = dt.datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)
    startTime = curDate - dt.timedelta(days=365*3)
    endTime = curDate.replace(hour=20, minute=0, second=0, microsecond=0)
    timeArr = getTimePeriods(startTime, endTime, 2)
    tickerInfo, symbolList, symbolStr = fd()
    for ticker in symbolList:
        print(ticker)
        # saveToCSV(timeArr, ticker)
    return timeArr

# Dividing datetime range into equal datetime periods
def getTimePeriods(start, end, frequency, bartime = 5):
    segments = []
    cur = start

    while cur < end:
        next = cur + timedelta(hours=frequency)
        if next > end:
            next = end

        if next.hour > 4 and next.hour <= 20:
            segments.append(next.strftime("%Y%m%d %H:%M:%S US/Eastern"))

        cur = next

    return segments

def saveToCSV(ticker, tickerData):
    filename = f"../DataStorage/{ticker}.csv"
    if(os.path.exists(filename)):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "Ticker", "Open", "High", "Low", "Close", "Volume", "Open Interest"])
    else:
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            for data in tickerData:
                print(data)
                writer.writerow(["Name", "Age", "Gender"])

def getHisData(TimeArr, Ticker):
    nest_asyncio.apply()
    util.startLoop()
    util.logToConsole('DEBUG')

    overall = []

    # init IB connect
    ib = IB()
    for time in TimeArr:
        data = {}
        if not ib.isConnected() or not ib.client.isConnected():
            ib.connect('127.0.0.1', 7497, clientId=0)

        stock = Stock(Ticker, 'SMART', 'USD')
        bars = ib.reqHistoricalData(
            stock, endDateTime='20211201 20:00:00 US/Eastern', durationStr='7200 S',
            barSizeSetting='5 secs', whatToShow='TRADES', useRTH=False)
        
        df = util.df(bars)
        for index, row in df.iterrows():
            data = {}

        ib.disconnect()

    return(overall)