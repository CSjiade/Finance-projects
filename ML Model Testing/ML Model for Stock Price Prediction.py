# Experimenting a simple neural network on Stock Prices


# import relevant modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as wb
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import talib


Stock = "MSFT"
Date = '2010-01-01'
end = '2020-05-25'

df = wb.DataReader(Stock, data_source = 'yahoo', start = Date,end=end)
data_source ="/Users/lianjiade/Desktop/Stock_Data/MSFT.csv"
df.to_csv(data_source)
df = pd.read_csv("/Users/lianjiade/Desktop/Stock_Data/MSFT.csv",parse_dates=True,squeeze=True)

data = df[['Close']]


# No.of days forward to predict share price
future = 20


#Creating a future Stock Price Column which will be the model target
data['Future'] = df[['Close']].shift(-future)

# Add RSI14
data['rsi 14'] = talib.RSI(df['Close'],timeperiod=14)


# Splice Data to start from row 14 due to RSI14 as model input
data = data[14:]


X = np.array(data.drop(['Future'],1))[:-future]
y = np.array(data[['Future']].dropna())
x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2)


# Training the model
model = Sequential()
model.add(Dense(1000,activation='relu'))
model.add(Dense(1000,activation='relu'))
model.add(Dense(1))
model.compile(optimizer="adam",loss='mean_squared_error')
history = model.fit(x_train,y_train,epochs=300)

#testing the model MSE on test data
test = model.predict(x_test)
rmse = np.sqrt(np.mean(test-y_test)**2)


# Testing model to predict future share price vs actual data

x_future = data.drop(['Future'],1)[:-future]
x_future = x_future.tail(future)
x_future = np.array(x_future)
predictions = model.predict(x_future)

#graph visualisation
data_1 = data[X.shape[0]:]
data_1['Predict'] = predictions
plt.plot(data['Close'])
plt.plot(data_1[['Close','Predict']])
plt.legend(['Orignal','Actual','Predicted'])
plt.plot(figsize=(30,8))
plt.xlabel('Number Trading Days from Start')
plt.ylabel('Stock Price')
plt.show()
