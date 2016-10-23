import datetime
import os.path
import re

import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data


#Loading data functions
def download_data(symbol):
    start = "2010-01-01"
    end = get_today()

    fileName = "data/{}_{}.csv".format(symbol, end)

    if not os.path.isfile(fileName):
        #Delete previous files
        for f in os.listdir("data"):
            if re.search("{}_....-..-...csv".format(symbol), f) and f != fileName:
                os.remove(os.path.join("data", f))
        try:
            df = data.DataReader(symbol, 'yahoo', start, end)
            df.to_csv(fileName)
        except:
            print "Cannot download data from {}".format(symbol)

def load_symbol(symbol):
    download_data(symbol)
    return pd.read_csv("data/{}_{}.csv".format(symbol, get_today()),
                            index_col="Date", parse_dates=True)

def load_symbol_adj_close(symbol):
    download_data(symbol)
    return pd.read_csv("data/{}_{}.csv".format(symbol, get_today()),
                            index_col="Date", usecols=["Date", "Adj Close"],
                            parse_dates=True)

#Calculating things functions
def get_max_close(symbol):
    df = load_symbol(symbol)
    return df['Close'].max()

def get_mean_volume(symbol):
    df = load_symbol(symbol)
    return df['Volume'].mean()

def ROI(symbol, investment, start_date="1900-01-01", end_date="2200-01-01"):
    """Return of investment"""
    df = load_symbol_adj_close(symbol)
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index=dates)
    df1 = df1.join(df, how="inner")

    first_value = df1.ix[-1, "Adj Close"]
    last_value = df1.ix[0, "Adj Close"]

    end_value = (investment/first_value)*last_value
    earnings = end_value-investment
    return (earnings/investment)*100

def get_bollinger_bands(df, wd):
    rm = pd.rolling_mean(df, window=wd)
    rstd = pd.rolling_std(df, window=wd)
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd
    return upper_band, lower_band

def get_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = ((df[1:]/df[:-1].values)-1)*100
    daily_returns.ix[0,:] = 0
    return daily_returns

#Data management
def get_data(symbols_list, start_date="1900-01-01", end_date="2200-01-01"):
    #Let's create an empty DataFrame
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index=dates)

    #join the symbols data
    for symbol in symbols_list:
        dfsymbol = load_symbol_adj_close(symbol)
        dfsymbol= dfsymbol.rename(columns={"Adj Close": symbol})
        df1 = df1.join(dfsymbol, how="inner")

    df2 = df1.ix[::-1]
    return df2

def normalize_data(df):
    return (df/df.ix[0,:]-1)*100

def get_today():
    td = datetime.datetime.today()
    year, month, day = td.year, td.month, td.day
    return "{}-{}-{}".format(year, month, day)

#Plotting functions
def plot_adj_close(symbol, wd=None, start_date="1900-01-01", end_date="2200-01-01"):
    df = get_data([symbol], start_date, end_date)
    df[symbol].plot()

    if wd:
        rm = pd.rolling_mean(df[symbol], window=wd)
        rm.plot()
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.title('Adjusted close of {}'.format(symbol))
    plt.grid(True)
    plt.show()

def plot_adj_close_multiple(symbols_list, start_date="1900-01-01", end_date="2200-01-01"):
    df = get_data(symbols_list, start_date, end_date)
    df.plot()
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.title('Adjusted close')
    plt.grid(True)
    plt.show()

def plot_adj_close_multiple_normalized(symbols_list, start_date="1900-01-01", end_date="2200-01-01"):
    df = get_data(symbols_list, start_date, end_date)
    df = normalize_data(df)
    df.plot()
    plt.xlabel('Day')
    plt.ylabel('%')
    plt.title('Adjusted close')
    plt.grid(True)
    plt.show()

def plot_bollinger_bands(symbol, wd, start_date="1900-01-01", end_date="2200-01-01"):
    #Get data
    df = get_data([symbol], start_date, end_date)
    upper_band, lower_band = get_bollinger_bands(df[symbol],wd)
    rm = pd.rolling_mean(df[symbol], window=wd)

    #Prepare the plot
    df[symbol].plot(label=symbol)
    rm.plot(label="Rolling mean")
    upper_band.plot(label="Upper Bollinger Band")
    lower_band.plot(label="Lower Bollinger Band")
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.title('Adjusted close of {0} + Bollinger Band {1} days'.format(symbol, wd))
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_daily_returns(symbols_list, start_date="1900-01-01", end_date="2200-01-01"):
    #get data
    df = get_data(symbols_list, start_date, end_date)
    dr = get_daily_returns(df)

    #calculate mean and std dev
    mean = dr.mean()
    std = dr.std()

    #plot
    dr.plot()
    plt.xlabel('Day')
    plt.ylabel('% daily return')
    plt.title('Daily returns')
    plt.grid(True)
    plt.legend()
    plt.show()
    for symbol in symbols_list:
        dr[symbol].hist(bins=100, label=symbol)
    plt.legend()
    plt.show()

    return mean, std
