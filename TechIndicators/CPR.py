import backtrader as bt
from ib_insync import *

def CPR(ticker, ib: IB):
    contract = Stock(ticker, 'SMART', 'USD')
    pricebars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )
    # P = high + low + close / 3
    # R1 = (P * 2) - low
    # R2 = P + (High - Low)
    # S1 = (P * 2) - High
    # S2 = P - (High - Low)

    # return(R1, R2, P, S1, S2)

    return(pricebars)

def ABC(ib: IB):
    tickers = ["TSLA", "AAPL"]
    contracts= []
    for ticker in tickers:
        contract = Stock(ticker, 'SMART', 'USD')
        ib.qualifyContracts(contract)
        contracts.append(contract)
    bars = ib.tickers(*contracts)
    # ib.reqRealTimeBars
    return(bars)