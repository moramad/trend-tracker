from datetime import datetime
from pycoingecko import CoinGeckoAPI
import yfinance as yf
from masterSymbols import *
from masterTrends import *
import yfinance
import pandas as pd
import numpy as np
import json

cg = CoinGeckoAPI()

def getCoinData(id):
    try:
        result = cg.get_coin_by_id(id)
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def getCoinPrice(coin, currencies="usd"):
    try:
        price = cg.get_price(ids=coin, vs_currencies= currencies)
        result = price[coin][currencies]
    except:        
        result = False
    return result

def getStockPrice(emitten):
    try:
        ticker = yf.Ticker(emitten)    
        data = ticker.info    
        data = data["currentPrice"]
        # data = data.get("currentPrice")
    except Exception as e:
        print("An Error occured :: ", e)
        return False
    return data

def getSupportResistance(symbol):    
    ticker = yfinance.Ticker(symbol+'-USD')
    data = ticker.info
    start_time = '2021-05-01'
    end_time = datetime.now().strftime("%Y-%m-%d")
    df = ticker.history(interval="1d",start=start_time, end=end_time)
    df['Date'] = pd.to_datetime(df.index)    
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

    def isSupport(df,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support
    def isResistance(df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance
    def isFarFromLevel(l):
        return np.sum([abs(l-x) < s  for x in levels]) == 0

    s =  np.mean(df['High'] - df['Low'])/2 
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]            
            if isFarFromLevel(l):
                levels.append((i,l))
        elif isResistance(df,i):
            l = df['High'][i]            
            if isFarFromLevel(l):
                levels.append((i,l))    

    supports = []
    for level in levels :
        support = rounding(level[1])
        supports.append(support)
    return supports


# update to trend table
def trendUpdater1():    
    listSymbol = searchSymbols()
    for symbol in listSymbol:        
        symbolID = symbol["symbolID"]
        symbolType = symbol["symbolType"]
        tickerID = symbol["tickerID"]        
        if symbolType == "crypto":                        
            try:
                updateTime = datetime.today()
                print(f"{symbolID} | {tickerID}")
                coin = getCoinData(tickerID)                                   
                coin.update({"updateTime": updateTime})
                result = updateTrend(coin)         
                supports = getSupportResistance(symbolID)                                       
                updateTrendSupport(coin,supports)
            except:                              
                return False
    return True

# update to history table
def trendUpdater2():        
    listSymbol = searchSymbols()
    for symbol in listSymbol:        
        # symbolID = symbol["symbolID"]
        symbolType = symbol["symbolType"]
        tickerID = symbol["tickerID"]        
        if symbolType == "crypto":                        
            try:
                price = getCoinPrice(tickerID)   
                updateTime = datetime.today().replace(minute=0,second=0,microsecond=0)

                coin = {}
                coin.update({"id": tickerID})
                coin.update({"price": price})
                coin.update({"updateTime": updateTime})               
                result = updateHistory(coin)                
            except:
                return False
    return True


def main():
    print("dataCatcher")
    # print(getCoinPrice('polygon'))
    # print(getStockPrice('ASII.JK'))    
    # print("dataCatcher.py")
    # print(getCoinData("ethereum"))
    print(trendUpdater1())
    # print(getCoinData("binancecoin"))

if __name__ == "__main__":    
    main()
