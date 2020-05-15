## A simple moving average backtest strategy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as wb





Stock = 'AWX.SI'
Date = '2019-01-01'
df = wb.DataReader(Stock, data_source = 'yahoo', start = Date)
data_source =r'Desktop:\datafile\AWX.SI.csv'
df.to_csv(data_source)
dff = pd.read_csv(r'Desktop:\datafile\AWX.SI.csv')



class Strategy:

    def __init__(self):

        self.long_run =long_run
        self.short_run = short_run
        self.cond = dff.index > self.long_run
        self.trade_price = dff['Open']
        self.close= dff['Adj Close']

    def smav(self):
        self.smav =np.where(Strategy().cond,Strategy().close.rolling(window = Strategy().short_run).mean(),0)
        return self.smav

    def lmav(self):
        self.lmav =np.where(Strategy().cond,Strategy().close.rolling(window = Strategy().long_run).mean(),0)
        return self.lmav


    def trend_day(self):
        self.trend_day = np.where(Strategy().smav()>Strategy().lmav(),1,
                                  np.where(Strategy().smav()<Strategy().lmav(),-1,0))

        return self.trend_day

    def prev_trend_day(self):
        self.prev_trend_day =np.where(Strategy().cond,np.roll(Strategy().trend_day(),1),0)
        return self.prev_trend_day

    def diff_trend_day(self):
        self.diff_trend_day = Strategy().trend_day() + Strategy().prev_trend_day()
        return self.diff_trend_day

t_name = 'mav'
long_run = 25
short_run = 1

s = Strategy()
dff['smav']= s.smav()
dff['lmav'] = s.lmav()
dff['trend_day']=s.trend_day()
dff['prev_trend_day']=s.prev_trend_day()
dff['diff_trend_day'] = s.diff_trend_day()





class Signal:
    def __init_(self):
        pass
    def trade_signal(self):
        self.trade_signal = np.where(Strategy().diff_trend_day()==0,Strategy().trend_day(),0)
        return self.trade_signal

    def order(self):
        self.order = np.where(Strategy().cond,np.roll(Signal().trade_signal(),1),0)
        return self.order

ts = Signal()
dff['trade_signal'] = ts.trade_signal()
dff['order'] = ts.order()





class Portfolio:
    def __init__(self):
        self.lot_size_long =1
        self.lot_size_short = 1
        self.contract_size =2000
        self.initial_cash = 10000
        self.long_amt = (-1)*np.where(Signal().order()==1,self.lot_size_long*self.contract_size*Strategy().trade_price,0)
        self.short_amt = (1)*np.where(Signal().order()==-1,self.lot_size_short*self.contract_size*Strategy().trade_price,0)

    def cash_delta(self):
        self.cash_delta = Portfolio().long_amt + Portfolio().short_amt
        return self.cash_delta

    def end_bal(self):
        self.end_bal = Portfolio().initial_cash + Portfolio().cash_delta().cumsum()
        return self.end_bal

    def end_pos(self):
        self.end_pos = Signal().order().cumsum()
        return self.end_pos

p = Portfolio()
dff['long_amt'] = p.long_amt
dff['short_amt'] = p.short_amt
dff['cash_delta'] = p.cash_delta()
dff['end_bal'] = p.end_bal()
dff['end_pos']= p.end_pos()
dff['pnl'] = dff['end_bal'] + (Portfolio().end_pos()*Strategy().trade_price*Portfolio().contract_size)


dff1=dff.set_index('Date')
plt.plot(dff1['pnl'])


plt.show()
