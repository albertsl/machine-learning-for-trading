#!/usr/bin/python2

# Stocks market data can be downloaded from Yahoo Finance in CSV format
# http://finance.yahoo.com/quote/HCP/history

import pandas as pd
import functions
import matplotlib.pyplot as plt

def test_run(symbols_list):
    print df1.ix['2016-09-30':'2016-09-01']
    df1 = df1.ix["2014-08-01":"2015-01-29", ["IAG.MC","ELE.MC"]]
    print df1

def test_run2(symbols_list):
    dfadjclose = functions.get_data(symbols_list, '2012-01-22', '2017-01-26')
    functions.plot_adj_close_multiple_normalized(symbols_list, start_date='2013-01-01')

def test_run3(symbols_list):
    print functions.ROI('IAG.MC', 1500, start_date='2013-01-01')
    functions.plot_bollinger_bands(symbols_list[4], wd=20)

def test_run4(symbols_list):
    functions.plot_daily_returns(symbols_list)
    print functions.get_today()

if __name__ == '__main__':
    symbols_list = ['AAPL','IBM','HCP','IAG.MC','ELE.MC']
    test_run4(symbols_list)
