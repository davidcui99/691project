import scipy.stats as stats
import pylab
import numpy as np
import pandas as pd
import statsmodels.api as sm
import math
from matplotlib import pyplot as plt
import scipy

filepath = '/Users/wangyz/PycharmProjects/pythonProject/691.csv'


def preparation(filepath):
    trade_data = pd.read_excel(filepath)
    trade_data["Time"] = pd.to_datetime(trade_data["Time"], format='%H%M%S%f')
    # trade_data = trade_data.set_index("Time")

    return trade_data


def extract_ticks(symbol):
    a = preparation(filepath)
    b = a[a['Symbol'] == symbol]
    c = b['Trade Price']
    return c


def del_trade_type(trade_type):
    a = preparation(filepath)
    a = a[~a['Sale Condition'].str.contains(trade_type, na=False)]
    return a


def reindex():
    a = preparation(filepath)
    a = a.set_index('Time')
    return a


def minute(size):
    a = preparation(filepath)
    a_timeindex = a.set_index("Time")
    a_MinBars = a_timeindex['Trade Price'].resample(size).ohlc()
    a_vol=a_timeindex['Trade Volume'].resample(size).ohlc()
    a_vol=pd.Series(a_vol['close'],name='Trade Volume')
    return pd.concat([a_MinBars, a_vol], axis=1)





def tick(size):
    a = preparation(filepath)
    b=len(a)
    cc=[]
    open=[]
    high=[]
    low=[]
    close=[]
    vol=[]
    time=[]
    for i in range((b//size)+1):
        start=size*i
        end=size*(i+1)-1
        if end<b:
            d = a[start:end]
            h=d['Trade Price'].tolist()
            time.append(str(d['Time'][start]))
            vol.append(sum(d['Trade Volume']))
            open.append(h[0])
            close.append(h[len(h)-1])
            high.append(max(h))
            low.append(min(h))
        else:
            dd = a[start:b-1]
            h = dd['Trade Price'].tolist()
            time.append(str(dd['Time'][start]))
            vol.append(sum(dd['Trade Volume']))
            open.append(h[0])
            close.append(h[len(h) - 1])
            high.append(max(h))
            low.append(min(h))

    c = {'Time':time,"open": open, "high": high, 'low':low,'close':close,'volume':vol}
    a_TickBars = pd.DataFrame(c, columns=['Time','open','high','low','close','volume'])
    return a_TickBars


def volume(size):
    a = preparation(filepath)
    b=len(a)
    start=0
    open=[]
    high=[]
    low=[]
    close=[]
    vol=[]
    time=[]

    for i in range(b):
        hhh=sum(a['Trade Volume'][start:i].tolist())
        if hhh>size:

            d = a[start:i]
            h = d['Trade Price'].tolist()
            time.append(str(d['Time'][start]))
            vol.append(sum(d['Trade Volume']))
            open.append(h[0])
            close.append(h[len(h) - 1])
            high.append(max(h))
            low.append(min(h))
            start=i
    c = {'Time':time,"open": open, "high": high, 'low':low,'close':close,'volume':vol}
    a_VolBars = pd.DataFrame(c, columns=['Time','open','high','low','close','volume'])
    return a_VolBars


def dollar(size):
    a = preparation(filepath)
    b=len(a)
    dol=[]
    start=0
    open=[]
    high=[]
    low=[]
    close=[]
    time=[]
    Dollar=a['Trade Volume']*a['Trade Price']
    for i in range(b):
        hhh=sum(Dollar[start:i].tolist())
        if hhh>size:
            d = a[start:i]
            h = d['Trade Price'].tolist()
            time.append(str(d['Time'][start]))
            dol.append(sum(Dollar[start:i]))
            open.append(h[0])
            close.append(h[len(h) - 1])
            high.append(max(h))
            low.append(min(h))
            start=i
    c = {'Time':time,"open": open, "high": high, 'low':low,'close':close,'Dollar':dol}
    a_DolBars = pd.DataFrame(c, columns=['Time','open','high','low','close','Dollar'])
    return a_DolBars
