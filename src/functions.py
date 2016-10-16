import matplotlib.pyplot as plt
import pandas as pd

#Loading data functions
def load_symbol(symbol):
    return pd.read_csv("data/{}.csv".format(symbol), index_col="Date",
    parse_dates=True)

def load_symbol_adj_close(symbol):
    return pd.read_csv("data/{}.csv".format(symbol), index_col="Date",
    usecols=["Date", "Adj Close"], parse_dates=True)

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

#Data management
def join_multiple_adj_close(symbols_list, start_date="1900-01-01", end_date="2200-01-01"):
    #Let's create an empty DataFrame
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index=dates)

    #join the symbols data
    for symbol in symbols_list:
        dfsymbol = load_symbol_adj_close(symbol)
        dfsymbol= dfsymbol.rename(columns={"Adj Close": symbol})
        df1 = df1.join(dfsymbol, how="inner")

    return df1

def normalize_data(df):
    return (df/df.ix[-1,:]-1)*100

#Plotting functions
def plot_adj_close(symbol):
    df = load_symbol_adj_close(symbol)
    df['Adj Close'].plot()
    plt.xlabel('Day number')
    plt.ylabel('Price')
    plt.title('Adjusted close of {}'.format(symbol))
    plt.grid(True)
    plt.show()

def plot_adj_close_multiple(symbols_list, start_date="1900-01-01", end_date="2200-01-01"):
    df = join_multiple_adj_close(symbols_list, start_date, end_date)
    df.plot()
    plt.xlabel('Day number')
    plt.ylabel('Price')
    plt.title('Adjusted close')
    plt.grid(True)
    plt.show()

def plot_adj_close_multiple_normalized(symbols_list, start_date="1900-01-01", end_date="2200-01-01"):
    df = join_multiple_adj_close(symbols_list, start_date, end_date)
    df = normalize_data(df)
    df.plot()
    plt.xlabel('Day number')
    plt.ylabel('%')
    plt.title('Adjusted close')
    plt.grid(True)
    plt.show()
