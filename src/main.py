#!/usr/bin/python2

# Stocks market data can be downloaded from Yahoo Finance in CSV format
# http://finance.yahoo.com/quote/HCP/history

import pandas as pd
import functions
import matplotlib.pyplot as plt

def test_run():
    # df = pd.read_csv("data/AAPL.csv")
    # print df.head()
    # print df[10:21]
    for symbol in ['AAPL','IBM','HCP','IAG.MC','ELE.MC']:
        #print 'Mean volume ', symbol, functions.get_max_close(symbol)
        df = pd.read_csv("data/{}.csv".format(symbol))
        #print df['Adj Close']
        df['Adj Close'].plot()

        #Create the plot
        plt.xlabel('Day number')
        plt.ylabel('Price')
        plt.title('Adjusted close of {}'.format(symbol))
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    test_run()
