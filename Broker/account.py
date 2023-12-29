from ib_insync import *
import nest_asyncio

def account():
    nest_asyncio.apply()
    util.startLoop()
    util.logToConsole('DEBUG')

    # init IB connect
    ib = IB()
    if not ib.isConnected() or not ib.client.isConnected():
        ib.connect('127.0.0.1', 7497, clientId=0)

    account_values = ib.accountValues()
    bp = next((v.value for v in account_values if v.tag == 'BuyingPower'), None)

    stock = Stock('TVTX', 'SMART', 'USD')
    bars = ib.reqHistoricalData(
        stock, endDateTime='20211201 20:00:00 US/Eastern', durationStr='7200 S',
        barSizeSetting='5 secs', whatToShow='TRADES', useRTH=False)
    
    # ReportsFinSummary for total revenue, dividends & eps
    # fundamentals = ib.reqFundamentalData(stock, 'ReportsFinStatements')
    
    df = util.df(bars)
    # shortFloats = []
    # for bar in bars:
    #     shortFloat = bar.shortableShares / bar.floatShares
    #     shortFloats.append(shortFloat)

    ib.disconnect()

    return(account_values, bp, ib, df)