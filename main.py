import pandas as pd
import functions

def test_run():
    # df = pd.read_csv("data/AAPL.csv")
    # print df.head()
    # print df[10:21]
    for symbol in ['AAPL','IBM']:
        print 'Mean volume ', symbol, functions.get_max_close(symbol)

if __name__ == '__main__':
    test_run()
