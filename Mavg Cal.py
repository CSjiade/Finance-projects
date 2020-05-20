// Simple Moving Average Calculator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as wb

Stock = 'AWX.SI'
Date = '2019-08-1'

Stock_Data = wb.DataReader(Stock, data_source = 'yahoo', start = Date)
Price_Close = Stock_Data['Close']
Close_avg_25 = Price_Close.rolling(window = 25).mean()
Close_avg_50= Price_Close.rolling(window = 50).mean()

plt.figure(figsize=(10, 5))
plt.plot(Close_avg_25)
plt.plot(Price_Close)
plt.plot(Close_avg_50)
plt.legend([Stock + ' Close_avg_25', Stock + ' Price_Close', Stock + ' Close_avg_50']);


plt.show()
