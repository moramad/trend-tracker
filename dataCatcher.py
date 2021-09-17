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
currency = "usd"

def getCoinData(id):
    try:
        result = cg.get_coin_by_id(id)
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def getCoinPrice(id):
    try:
        coin = cg.get_coin_by_id(id, tickers=False, community_data=False, developer_data=False, sparkline=False)        
    except:        
        result = False
    return coin

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

# update to trend table
def trendUpdater():    
    listSymbol = searchSymbols()
    for symbol in listSymbol:        
        symbolID = symbol["symbolID"]
        symbolType = symbol["symbolType"]
        tickerID = symbol["tickerID"]        
        if symbolType == "crypto":                        
            try:                
                print(f"{symbolID} | {tickerID}")
                coin = getCoinData(tickerID)                                   
                updateTime = datetime.today()
                coin.update({"updateTime": updateTime})
                result = updateTrend(coin)         

                updateTime = datetime.today().replace(minute=0,second=0,microsecond=0)
                current_price = coin["market_data"]["current_price"][currency]
                high = coin["market_data"]["high_24h"][currency]
                low = coin["market_data"]["low_24h"][currency]
                market_cap = coin["market_data"]["market_cap"][currency]
                coin = {}
                coin.update({"id": tickerID})
                coin.update({"symbolID": symbolID})                
                coin.update({"current_price": current_price})
                coin.update({"high": high})
                coin.update({"low": low})
                coin.update({"market_cap": market_cap})
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
    print(trendUpdater())
    # print(getCoinPrice("ethereum"))
    # print(getCoinData("binancecoin"))

if __name__ == "__main__":    
    main()
