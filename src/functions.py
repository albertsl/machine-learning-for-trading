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

# Not working yet
# def ROE(symbol, start_date, end_date, investment):
#     df = load_symbol_adj_close(symbol)
#     dates = pd.date_range(start_date, end_date)
#     df1 = pd.DataFrame(index=dates)
#     df1 = df1.join(df, how="inner")
#     print df1
#     print df1.first("1D")
#     print df1.last("1D")

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

#Plotting functions
def plot_adj_close(symbol):
    df = load_symbol_adj_close(symbol)
    df['Adj Close'].plot()
    plt.xlabel('Day number')
    plt.ylabel('Price')
    plt.title('Adjusted close of {}'.format(symbol))
    plt.grid(True)
    plt.show()

def plot_adj_close_multiple(symbols_list):
    df = join_multiple_adj_close(symbols_list)
    df.plot()
    plt.xlabel('Day number')
    plt.ylabel('Price')
    plt.title('Adjusted close')
    plt.grid(True)
    plt.show()
