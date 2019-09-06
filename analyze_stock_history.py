import pandas as pd, numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('quotes.history.csv', index_col=[0,1])
df['change_20'] = (df.groupby(level=1).diff(-20) / df).close
# df = df.dropna()
# df.groupby(level=1).change_20.median()
# df.groupby(level=1).change_20.std()

df_change_stat = pd.DataFrame()
df_change_stat['p50'] = df.groupby(level=1).change_20.median()
df_change_stat['stdev'] = df.groupby(level=1).change_20.std()
df_change_stat['p50_div_stdev'] = df_change_stat.p50 / df_change_stat.stdev

print(df_change_stat.sort_values(by='p50_div_stdev', ascending=False).head(10))
print(df_change_stat.sort_values(by='p50_div_stdev', ascending=True).head(10))


# df.xs('MCD', level=1, drop_level=False).change_20.hist()
# plt.show()

top_symbols_high = df_change_stat.sort_values(by='p50_div_stdev', ascending=False).head(10).index.values
top_symbols_low = df_change_stat.sort_values(by='p50_div_stdev', ascending=True).head(10).index.values

def plot_symbol(symbol):
    plt.clf()
    df.xs(symbol, level=1, drop_level=False).change_20.hist()
    plt.title('%s 20 tdays change dist' % (symbol))
    plt.xlabel('20 tdays change')
    plt.ylabel('freq')

with open('top_high_symbols.txt', 'w') as outfile:
    for symbol in top_symbols_high:
        plot_symbol(symbol)
        plt.savefig("plots/highs/%s.png" % (symbol))
        outfile.write(symbol + '\n')

with open('top_low_symbols.txt', 'w') as outfile:
    for symbol in top_symbols_low:
        plot_symbol(symbol)
        plt.savefig("plots/lows/%s.png" % (symbol))
        outfile.write(symbol + '\n')
