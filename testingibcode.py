# retrieving ib historical data, after connected to IB
def hisData():
    # contract = Forex('EURUSD')
    stock = Stock('AMTD', 'SMART', 'USD')
    bars = ib.reqHistoricalData(
        stock, endDateTime='20230303 15:59:00 US/Eastern', durationStr='30 D',
        barSizeSetting='1 hour', whatToShow='TRADES', useRTH=False)
    
    ticks = ib.reqHistoricalTicks(
        stock, startDateTime='20230303 08:00:00 US/Eastern', 
        endDateTime='20230303 15:59:00 US/Eastern', numberOfTicks=500, 
        whatToShow='TRADES', useRth=False)

    # convert to pandas dataframe:
    df = util.df(bars)
    ds = util.df(ticks)

# use IB TWS scanner for scanning stocks (currently using financialmodelingprep)
# reason for using financialmodelingprep: IB scanner requires scancode which I dont want
def IBScanner():
    sub = ScannerSubscription(
        instrument='STK',
        scanCode='TOP_PERC_GAIN',
    )

    tagValues = [
        TagValue('usdPriceAbove', 1),
        TagValue('usdPriceBelow', 10),
        TagValue('volumeAbove', 100000),
        TagValue('marketCapAbove1e6', 50),
        TagValue('marketCapBelow1e6', 500),
    ]

    scanResults = ib.reqScannerData(sub)

    for stock in scanResults:
        print(stock.contractDetails.contract.symbol)

    filtered_stocks = [stock.contractDetails.contract.symbol for stock in scanResults]

    ds = util.df(filtered_stocks)

    return(len(filtered_stocks))