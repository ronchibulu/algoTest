import csv
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

def testing():
    ticker = "AAPL"

    news = yf.Ticker(ticker).news

    url = "https://docs.ansible.com/ansible/latest/os_guide/windows_setup.html#winrm-setup"

    # Fetch the webpage content
    page = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the article content
    article = soup.find(id="setting-up-a-windows-host")

    sector_tickers = ['XLF', 'XLK', 'XLI', 'XLV', 'XLY', 'XLE']

    sector_data = {}
    for ticker in sector_tickers:
        sector_data[ticker] = yf.download(ticker, start='2022-01-01', end='2022-05-01', interval="1d")

    rolling_window = 10
    for ticker, data in sector_data.items():
        data['rolling'] = data['Close'].rolling(window=rolling_window).mean()

    fig, axs = plt.subplots(len(sector_tickers), 1, figsize=(8, 4 * len(sector_tickers)), sharex=True)
    for i, ticker in enumerate(sector_tickers):
        axs[i].plot(sector_data[ticker].index, sector_data[ticker]['Close'])
        axs[i].plot(sector_data[ticker].index, sector_data[ticker]['rolling'])
        axs[i].set_title(ticker)
    plt.show()

    # resistance = ta.pivotpoints.PivotPoints(stock_data["High"], stock_data["Low"], stock_data["Close"]).resistance.iloc[-1]
    # support = ta.pivotpoints.PivotPoints(stock_data["High"], stock_data["Low"], stock_data["Close"]).support.iloc[-1]

    # # Extract the article title and content
    # title = article.find("h1").get_text()
    # content = "\n".join([p.get_text() for p in article.find_all("p")])

    # # Print the title and content
    # print(content)

    return 