# including libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yfin
import datetime as dt

#Getting Data Frame
plt.style.use('fivethirtyeight')
yfin.pdr_override()
start=dt.datetime(2006,1,1)
end=dt.datetime(2012,1,1)
df = pdr.get_data_yahoo('IBM', start, end)

#Visualize the data

plt.figure(figsize=(12.5, 4.5))
plt.plot(df['Adj Close'], label ='IBM')
plt.title('WMT Adj. Close (2006 - 2011)')
plt.xlabel('Jan. 01, 2006 - Dec. 30, 2011')
plt.ylabel('Adj. Close ($)')

#Create the simple moving average with a 30 day window

SMA30 = pd.DataFrame()
SMA30['Adj Close'] = df['Adj Close'].rolling(window=30).mean()

# Create a simple moving average for 120 days

SMA120 = pd.DataFrame()
SMA120['Adj Close'] = df['Adj Close'].rolling(window=120).mean()
#Visualize the data

plt.figure(figsize=(12.5, 4.5))
plt.plot(df['Adj Close'], label ='WMT')
plt.plot(SMA30['Adj Close'], label ='SMA 30')
plt.plot(SMA120['Adj Close'], label ='SMA 120')
plt.title('IBM Adj. Close (2006 - 2011)')
plt.xlabel('Jan. 01, 2006 - Dec. 30, 2011')
plt.ylabel('Adj. Close ($)')
plt.legend(loc='lower right')
plt.show()

#Create a new data frame to store all the data

data=pd.DataFrame()
data['AAPL'] = df['Adj Close']
data['SMA30']= SMA30['Adj Close']
data['SMA120']= SMA120['Adj Close']


# Create a function to signal when to buy and sell

def buy_sell(data):
  netGain=0
  signalBuy = []
  signalSell = []
  stock = False  #initially nothing to sell
  for index in range(len(data)):

    if data['SMA30'][index] > data['SMA120'][index]:
      if stock is False:
        signalBuy.append(data['AAPL'][index])
        signalSell.append(np.nan)
        netGain-=data['AAPL'][index]
        stock=True
      else:
        signalBuy.append(np.nan)
        signalSell.append(np.nan)
    elif data['SMA30'][index] < data['SMA120'][index]:
      if stock:
        signalBuy.append(np.nan)
        signalSell.append(data['AAPL'][index])
        stock=False
        netGain+=data['AAPL'][index]
      else:
        signalBuy.append(np.nan)
        signalSell.append(np.nan)
    else:
      signalBuy.append(np.nan)
      signalSell.append(np.nan)
  if stock:
    netGain+=data['AAPL'][-1]
  return signalBuy, signalSell, netGain

#adding the buy call and sell call to the data

data['Buy_Signal_Price'], data['Sell_Signal_Price'], netGain = buy_sell(data)

# Testing out the stratergy

plt.figure(figsize=(12.5, 4.5))
plt.plot(df['Adj Close'], label ='AAPL', alpha = 0.25)
plt.plot(SMA30['Adj Close'], label ='SMA 30', alpha = 0.25)
plt.plot(SMA120['Adj Close'], label ='SMA 120', alpha = 0.25)
plt.scatter(data.index, data['Buy_Signal_Price'], label ='Buy', marker ='^', color ='green')
plt.scatter(data.index, data['Sell_Signal_Price'], label ='Sell', marker ='v', color ='red')
plt.title('Apple Adj. Close (Buy and Sell)')
plt.xlabel('Jan. 01, 2006 - Dec. 30, 2011')
plt.ylabel('Adj. Close ($)')
plt.legend(loc='lower right')
plt.show()