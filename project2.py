import pandas as pd
from project1 import *



# part 1

filepath = '/Users/wangyz/PycharmProjects/pythonProject/691.csv'
def get_log_return(df):
    log_returns = pd.Series(np.log((df['close'] - df['open'])/df['open'] + 1),name='log returns')
    return pd.concat([df,log_returns], axis=1)




# 1
def clean_up(trade_type):
    a = preparation(filepath)
    a = a[~a['Sale Condition'].str.contains(trade_type, na=False)]

    to_drop = []
    for time in a['Time']:
        if time > pd.Timestamp('1900-01-01 16:00:00', freq='T'):
            to_drop.append(time)
    a = a.drop(to_drop)
    return a

# 2

h1=get_log_return(minute('1min'))
h2=get_log_return(minute('1min'))

to_drop = []
for time in h1.index:

    if time > pd.Timestamp('1900-01-01 16:00:00', freq='T'):
        to_drop.append(time)
h1 = h1.drop(to_drop)
h2=h2.drop(to_drop)


def dbStructure(h1,h2,option):
    vxCalendar = h1.index
    if option=='log returns':
        mnLogReturns = np.vstack((np.array(h1['log returns']), np.array(h2['log returns'])))
        dbLogReturns = [vxCalendar,['1min','1min'],mnLogReturns.transpose()]

        return dbLogReturns
    if option=='Trade Volume':
        mnTradeVolume = np.vstack((np.array(h1['Trade Volume']), np.array(h2['Trade Volume'])))
        dbTradeVolume = [vxCalendar,['1min','1min'],mnTradeVolume.transpose()]

        return dbTradeVolume
    if option=='Trade Price':
        mnTradePrice = np.vstack((np.array(h1['close']), np.array(h2['close'])))
        dbTradePrice = [vxCalendar,['1min','1min'],mnTradePrice.transpose()]

        return dbTradePrice

# 3

