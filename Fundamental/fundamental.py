from ib_insync import *
from urllib.request import urlopen
import certifi
import json
import datetime as dt
import pandas_datareader.data as pdr
import yfinance as yf

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def fundamental():
    # --- stocksera
    # client = stocksera.Client(api_key="qkHuJAma.jPwMPmtqbxMwaRqIlG8cKYCEvxxjg59v")
    # sv = client.short_volume(ticker="BBBY", date_from="2023-03-09", date_to="2023-03-09")

    # date time now
    dtn = dt.datetime.now().strftime("%Y%m%d")

    mktCapMore = 50000000
    mktCapLower = 500000000
    priceMore = 1
    priceLower = 15
    vMore = 100000
    exchange = "NYSE,NASDAQ,AMEX"

    url = (f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={mktCapMore}&isEtf=false&isActivelyTrading=true&exchange={exchange}&marketCapLowerThan={mktCapLower}&priceMoreThan={priceMore}&priceLowerThan={priceLower}&volumeMoreThan={vMore}&apikey=27e4f236d5ec6459bea15469ac9d5d36")
    data = get_jsonparsed_data(url)
    # available fields = symbol, companyName, marketCap, sector, industry, beta, price, lastAnnualDividend, volume, exchange, exchangeShortName, country, isEtf, isActivelyTrading
    tickerInfo = [{"symbol": d['symbol'], "marketCap": d['marketCap'], "sector": d['sector'], "industry": d['industry'], "price": d['price'], "volume": d['volume']} for d in data]
    # getting tickers as string
    symbolList = [d["symbol"] for d in tickerInfo]
    symbolStr = ",".join(symbolList)

    # --- using alphavantage to retrieve news sentiment
    # alpha vantage api key
    # JYIMQKXF9AXIO053
    # aurl = (f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&limit=1&sort=RELEVANCE&apikey=JYIMQKXF9AXIO053')
    # r = requests.get(aurl)
    # adata = r.json()
    
    # --- using sec-api.io to retrieve stock float
    # api_key = '33a3936ae84c411d4bdceca0b952277f139763be335274e970463974ef5bcedc'
    # ticker = 'INAB'
    # url = f'https://api.sec-api.io/float?ticker={ticker}&token={api_key}'
    # response = requests.get(url)
    # data = json.loads(response.text)

    # return(adata.get("feed")[0].get("title"))
    return(tickerInfo, symbolList, symbolStr)