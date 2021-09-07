from datetime import datetime
from pycoingecko import CoinGeckoAPI
import yfinance as yf
from masterSymbols import *
from masterTrends import *

cg = CoinGeckoAPI()

def getCoinData(id):
    try:
        result = cg.get_coin_by_id(id)
        return result
    except:
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

def trendUpdater():    
    listSymbol = searchSymbols()
    for symbol in listSymbol:        
        # symbolID = symbol["symbolID"]
        symbolType = symbol["symbolType"]
        tickerID = symbol["tickerID"]        
        if symbolType == "crypto":                        
            try:
                coin = getCoinData(tickerID)                  
                result = updateTrend(coin)
                print(result)
            except:
                return False
    return True

def main():
    # print("dataCatcher")
    # print(getCoinPrice('polygon'))
    # print(getStockPrice('ASII.JK'))    
    # print("dataCatcher.py")
    # print(getCoinData("ethereum"))
    print(trendUpdater())

if __name__ == "__main__":    
    main()