from notifications import *
from dataModels import *
from masterTrends import *

import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import numpy as np
from datetime import datetime

currency = "usd"
days = 30

def priceSummarize(id):
    try:
        # listSymbol = searchTrend(id)
        # for symbol in listSymbol:  
        # updateTime = symbol["updateTime"]   
        symbol = getCoinData(id)               
        id = symbol["id"]
        code = symbol["symbol"]
        name = symbol["name"]
        current_price = symbol["market_data"]["current_price"]["usd"]
        price_change_percentage_1h = symbol["market_data"]["price_change_percentage_1h_in_currency"]["usd"]
        price_change_percentage_24h = symbol["market_data"]["price_change_percentage_24h"]
        price_change_percentage_7d = symbol["market_data"]["price_change_percentage_7d"]
        price_change_percentage_30d = symbol["market_data"]["price_change_percentage_30d"]
        total_volume = symbol["market_data"]["total_volume"]["usd"]
        ath = symbol["market_data"]["ath"]["usd"]
        atl = symbol["market_data"]["atl"]["usd"]    
        ath_date = convertDate(symbol["market_data"]["ath_date"]["usd"])     
        atl_date = convertDate(symbol["market_data"]["atl_date"]["usd"])
        ath_change_percentage = symbol["market_data"]["ath_change_percentage"]["usd"]    
        atl_change_percentage = symbol["market_data"]["atl_change_percentage"]["usd"]        
        updateTime = symbol["last_updated"]
        
        format = f"COIN SUMMARY : {name} | {code.upper()} @ {updateTime} \n"
        format = format + f"price = ${current_price} \n"
        format = format + f"change % 1h = {round(price_change_percentage_1h,2)}% \n"
        format = format + f"change % 24h = {round(price_change_percentage_24h,2)}% \n"
        format = format + f"change % 7d = {round(price_change_percentage_7d,2)}% \n"
        format = format + f"change % 30d = {round(price_change_percentage_30d,2)}% \n"            
        format = format + f"volume = {total_volume} \n"
        format = format + f"ath = ${ath} pada {ath_date}, selisih {round(ath_change_percentage,2)}%  \n"    
        format = format + f"atl = ${atl} pada {atl_date}, selisih {round(atl_change_percentage,2)}%"    
        print(format)
        # telegram_sendMessage(format)
        return format
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def marketSummarize():
    threshold_change_percentage_1h = 3
    threshold_change_percentage_24h = 15
    threshold_change_percentage_7d = 100
    threshold_change_percentage_30d = 300
    threshold_ath_change_percentage = 10
    listSymbol = searchTrend()    
    content = []
    
    for symbol in listSymbol:
        notif = ""
        flnotif = False
        flath = False
        flatl = False
        flPriceChangeUp1h = False
        flPriceChangeUp24h = False
        flPriceChangeUp7d = False
        flPriceChangeUp30d = False
        flPriceChangeDown1h = False
        flPriceChangeDown24h = False
        flPriceChangeDown7d = False
        flPriceChangeDown30d = False

        id = symbol["id"]         
        name = symbol["name"]
        code = symbol["symbol"]
        current_price = symbol["market_data"]["current_price"]["usd"]
        price_change_percentage_1h = symbol["market_data"]["price_change_percentage_1h_in_currency"]["usd"]
        price_change_percentage_24h = symbol["market_data"]["price_change_percentage_24h"]
        price_change_percentage_7d = symbol["market_data"]["price_change_percentage_7d"]
        price_change_percentage_30d = symbol["market_data"]["price_change_percentage_30d"]
        total_volume = symbol["market_data"]["total_volume"]["usd"]
        ath = symbol["market_data"]["ath"]["usd"]
        atl = symbol["market_data"]["atl"]["usd"]
        ath_date = convertDate(symbol["market_data"]["ath_date"]["usd"])     
        atl_date = convertDate(symbol["market_data"]["atl_date"]["usd"])
        ath_change_percentage = symbol["market_data"]["ath_change_percentage"]["usd"]    
        atl_change_percentage = symbol["market_data"]["atl_change_percentage"]["usd"]                
        updateTime = symbol["updateTime"]
        
        if ath_change_percentage >= -threshold_ath_change_percentage :
            flnotif = True
            flath = True
        if atl_change_percentage <= threshold_ath_change_percentage :
            flnotif = True
            flatl = True
        if price_change_percentage_1h > threshold_change_percentage_1h :
            flnotif = True
            flPriceChangeUp1h = True
        if price_change_percentage_1h < -threshold_change_percentage_1h :
            flnotif = True
            flPriceChangeDown1h = True
        if price_change_percentage_24h > threshold_change_percentage_24h :
            flnotif = True
            flPriceChangeUp24h = True
        if price_change_percentage_24h < -threshold_change_percentage_24h :
            flnotif = True
            flPriceChangeDown24h = True
        if price_change_percentage_7d > threshold_change_percentage_7d :
            flnotif = True
            flPriceChangeUp7d = True
        if price_change_percentage_7d < -threshold_change_percentage_7d :
            flnotif = True
            flPriceChangeDown7d = True
        if price_change_percentage_30d > threshold_change_percentage_30d :
            flnotif = True
            flPriceChangeUp30d = True
        if price_change_percentage_30d < -threshold_change_percentage_30d :
            flnotif = True
            flPriceChangeDown30d = True
        
        if flnotif:
            notif = f"- {name} | {code.upper()} | @ {updateTime} "
        if flath:
            notif = notif + f"ATH @ ${ath}, "
        if flatl:
            notif = notif + f"ATL @ ${ath}, "
        if flPriceChangeUp1h:
            notif = notif + f"naik {round(price_change_percentage_1h,2)}% 1jam, "
        if flPriceChangeDown1h:
            notif = notif + f"turun {round(price_change_percentage_1h,2)}% 1jam, "
        if flPriceChangeUp24h:
            notif = notif + f"naik {round(price_change_percentage_24h,2)}% 24jam, "
        if flPriceChangeDown24h:
            notif = notif + f"turun {round(price_change_percentage_24h,2)}% 24jam, "
        if flPriceChangeUp7d and (price_change_percentage_24h != price_change_percentage_7d):
            notif = notif + f"naik {round(price_change_percentage_7d,2)}% 7hari, "
        if flPriceChangeDown7d and (price_change_percentage_24h != price_change_percentage_7d):
            notif = notif + f"turun {round(price_change_percentage_7d,2)}% 7hari, "
        if flPriceChangeUp30d and (price_change_percentage_24h != price_change_percentage_30d):
            notif = notif + f"naik {round(price_change_percentage_30d,2)}% 30hari, "
        if flPriceChangeDown30d and (price_change_percentage_24h != price_change_percentage_30d):
            notif = notif + f"turun {round(price_change_percentage_30d,2)}% 30hari, "
        if flnotif:                    
            content.append(notif)
            
    if content:
        result = "\n".join(content)        
        return result

def getSupportResistanceArray(id):    
    # ticker = yfinance.Ticker(symbol+'-'+currency.upper())
    # data = ticker.info
    # start_time = '2021-05-01'
    # end_time = datetime.now().strftime("%Y-%m-%d")
    # df = ticker.history(interval="1d",start=start_time, end=end_time)

    result = cg.get_coin_ohlc_by_id(id=id,vs_currency=currency,days=days)
    df = pd.DataFrame(result)
    df.columns = ["Date","Open","High","Low","Close"]
    df['Date'] = pd.to_datetime(df['Date'],unit='ms')
    df['Date'] = df['Date'].apply(mpl_dates.date2num)

    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

    def isSupport(df,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support
    def isResistance(df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance
    def isFarFromLevel(l):
        return np.sum([abs(l-x) < s  for x in levels]) == 0

    s =  np.mean(df['High'] - df['Low']) * 2
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
    
def takeClosest(num,listSupports):
    listSupports.sort()
    support = 0
    resistance = listSupports[-1]
    result = []
    for item in listSupports:
        if item <= num:
            support = max(item, support)
        if item > num:
            resistance = min(item, resistance)
    result.append(support)
    if support != resistance and num < resistance:
        result.append(resistance)
    return result    

def coreAnalytic():
    listSymbol = searchSymbols()
    for symbol in listSymbol:        
        symbolType = symbol["symbolType"]  
        symbolID = symbol["symbolID"]      
        tickerID = symbol["tickerID"]        
        if symbolType == "crypto":                        
            try:                                
                updateTime = datetime.today()
                supports = getSupportResistanceArray(tickerID)
                coinData = searchTrend(tickerID)    
                current_price = coinData[0]["market_data"]["current_price"][currency]    
                supres = takeClosest(current_price, supports)                                
                print(f"{symbolID} | {tickerID} | {supports} | {current_price}")
                if supres and len(supports)>1 and len(supres)>1:                                                                 
                    try:
                        support = supres[0]
                        resistance = supres[1]
                        percent2resistance = ((current_price - support) / (resistance - support)) * 100
                        percent2resistance = round(percent2resistance,2)
                    except Exception as e:                        
                        print(f"An Error occured : {e}")
                        percent2resistance = "NA"                                            
                else:
                    support = 0
                    resistance = 0
                    percent2resistance = "NA"

                coin = {}                
                coin.update({"id": tickerID})                
                coin.update({"updateTime": updateTime})
                coin.update({"supports": supports})
                coin.update({"support": support})
                coin.update({"resistance": resistance})
                coin.update({"percent2resistance": percent2resistance})    
                updateTrendSupportResistance(coin)                
            except Exception as e:
                print("An Error occured in coreAnalytic :: ", e)
                return False
    return True    

def main():
    print("coreAnalyzer")
    # print(marketSummarize())
    # priceSummarize("ethereum")
    # supports = getSupportResistanceArray("DOGE")     
    # getSupportResistance("btc")
    # getSupportResistance("ada")
    print(coreAnalytic())


if __name__ == "__main__":    
    main()