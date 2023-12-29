import backtrader as bt
import datetime as dt
import backtrader_ib_insync as ibnew

class StockStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print(f'{dt}, {txt}')

    def __init__(self):
        self.open = self.datas[0].open
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.close = self.datas[0].close
        self.volume = self.datas[0].volume
        self.openinterest = self.datas[0].openinterest

    def next(self):
        self.log(f'Open:{self.open[0]:.2f}, \
                   High:{self.high[0]:.2f}, \
                   Low:{self.low[0]:.2f}, \
                   Close:{self.close[0]:.2f}, \
                   Volume:{self.volume[0]:.2f}, \
                   OpenInterest:{self.volume[0]:.2f}' )

def start():
    cerebro = bt.Cerebro()
    store = ibnew.IBStore(host='127.0.0.1', port=7497)
    broker = store.getbroker()
    cerebro.setbroker(broker)
    ibdata = store.getdata
    start = dt.datetime(2020, 5, 1, 4, 0, 0)
    end = dt.datetime(2020, 5, 1, 11, 59, 30)

    data = ibdata(dataname='AAPL', # Symbol name
                secType='STK',   # SecurityType is STOCK 
                exchange='SMART',# Trading exchange IB's SMART exchange 
                currency='USD',  # Currency of SecurityType
                historical=True,
                fromdate=start,
                todate=end,  
                what='TRADES',  # Update this parameter to select data type
                timeframe= bt.TimeFrame.Seconds, compression=30,
                # qcheck=0.5,
                # backfill_start=True, backfill=True,
                # latethrough=True,
                # tz=None,
                useRTH = False,
                # hist_tzo = None,
                )

    cerebro.adddata(data)

    # Add the printer as a strategy
    cerebro.addstrategy(StockStrategy)

    cerebro.run()

    # cerebro.plot()

start()