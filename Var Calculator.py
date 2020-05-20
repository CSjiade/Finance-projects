# Calculating Historical Var at 95% confidence level of a Portfolio

# Calculating Historical Var at 95% confidence level of a Portfolio

import numpy as np
from pandas_datareader import data as wb
from scipy.stats import norm
import matplotlib.pyplot as plt

Stock = ['AWX.SI','E28.SI','558.SI','AJBU.SI','CRPU.SI']
Weights = np.repeat(1/len(Stock),len(Stock))  #equal weight portfolio

Start_cash = 50000

start = "2019-05-20"
end = "2020-05-20"

data = wb.DataReader(Stock, data_source="yahoo", start= start, end=end)['Close']

returns = data.pct_change()

cov_matrix = returns.cov()

mean_ret = returns.mean()

port_mean = mean_ret.dot(Weights)


# portfolio standard deviation
port_std = np.sqrt(Weights.T.dot(cov_matrix).dot(Weights))

mean_investment = (1+port_mean) * Start_cash

std_investment = Start_cash * port_std

conf_level = 0.05  # set at 95% confidence level
var_95 = norm.ppf(conf_level, mean_investment, std_investment)
var = Start_cash - var_95  # Var


Weighted_Daily_returns = returns.dropna()*Weights
Weighted_Daily_total_returns = Weighted_Daily_returns.sum(axis=1)*100

# plotting a histogram showing distribution of historical daily returns
plt.hist(Weighted_Daily_total_returns)
plt.axvline(x=(-var/Start_cash)*100, color="r", linestyle="-",label="Var 95")
plt.legend()
plt.title("Portfolio Daily Returns from " + start + " to " + end)
plt.xlabel("Daily Returns in %")
plt.ylabel("Frequency")

plt.show()

