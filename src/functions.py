import pandas as pd

def get_max_close(symbol):
    df = pd.read_csv("data/{}.csv".format(symbol))
    return df['Close'].max()

def get_mean_volume(symbol):
    df = pd.read_csv("data/{}.csv".format(symbol))
    return df['Volume'].mean()
