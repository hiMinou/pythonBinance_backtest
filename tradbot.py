#definition de var, imports de librairies et de data
from typing import Final
import pandas as pd
from binance.client import Client 
import ta

klinesT = Client().get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "01 January 2017")
df = pd.DataFrame(klinesT, columns= ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'Ignore' ])


#clean data set

del df['Ignore']
del df['close_time']
del df['quote_av']
del df['tb_base_av']
del df['tb_quote_av']
del df['trades']
del df['volume']

df['close'] = pd.to_numeric(df['close'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['open'] = pd.to_numeric(df['open'])

#convertir le timestamp et indexage
df = df.set_index(df['timestamp'])
df.index = pd.to_datetime(df.index, unit="ms")
del df['timestamp']

#definition des indicateurs
df['SMA200'] = ta.trend.sma_indicator(df['close'], 200)
df['SMA600'] = ta.trend.sma_indicator(df['close'], 600)

#traiter notre backtest
usdt = 1000
btc = 0
lastIndex = df.first_valid_index()

for index, row in df.iterrows():
    if df['SMA200'][lastIndex] > df['SMA600'][lastIndex] and usdt > 10:
        btc = usdt / df['close'][index]
        btc = btc - 0.007 * btc
        usdt = 0
        print("Achat BTC à ", df['close'][index], "$ le ", index)
    if df['SMA200'][lastIndex] < df['SMA600'][lastIndex] and btc > 0.0001:
        usdt = btc * df['close'][index]
        usdt = usdt - 0.007 * usdt
        btc = 0
        print("Vente BTC à", df['close'][index], "$ le ", index)
    lastIndex = index


#afficher nos résultats
finalResultat = usdt + btc * df['close'].iloc[-1]
print("usdt: ", usdt, "btc",btc)
print("Gain final: ", finalResultat," USDT")