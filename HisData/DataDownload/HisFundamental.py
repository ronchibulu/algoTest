import csv
import pandas_datareader as pd
import requests
import yfinance as yf
import datetime as dt
from bs4 import BeautifulSoup
import re
import time

def hisFundamental(stockList):
    # Defining csv data
    filename = '../DataStorage/FundamentalData.csv'
    dtn = dt.datetime.now().strftime("%Y-%m-%d")
    header = [
        'Ticker',
        'Date',
        "mktWatch-marketCap",
        "mktWatch-float",
        "mktWatch-Beta",
        "mktWatch-P/Eratio",
        "mktWatch-EPS",
        "mktWatch-yield",
        "mktWatch-dividend",
        "mktWatch-short%"
    ]

    # open the CSV file using a context manager
    with open(filename, mode='w', newline='') as csv_file:
        # create a writer object using the csv module
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)

    data = []

    for symbol in stockList:
        data = data + [symbol, dtn]

        # Market Watch Data
        url = f"https://www.marketwatch.com/investing/stock/{symbol}"
        # Fetch the webpage content
        page = requests.get(url)

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(page.content, "html.parser")

        # Retrieve Data
        mktWatchdata = soup.body.find_all("small", {"class": "label"}, string=["Market Cap", "Public Float", "Beta", "P/E Ratio", "EPS", "Yield", "Dividend", "% of Float Shorted"])
        
        for item in mktWatchdata:
            val = item.find_next_siblings("span", {"class": "primary"})[0].text
            match = re.search(r"([0-9\.]+)\s?(M|B)", val)
            if match is not None:
                quantity = match.group(1)
                magnitude = match.group(2)
                data.append(float(quantity) * (10 ** 9 if magnitude == "B" else 10 ** 6))
            else:
                val = re.sub(r'($|%)', ' ', val)
                data.append(val.replace("$", ""))

        # open the CSV file using a context manager
        with open(filename, mode='a', newline='') as csv_file:
            # create a writer object using the csv module
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data)
        data = []

        time.sleep(2)

    return