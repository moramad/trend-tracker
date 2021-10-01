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
        symbol = searchTrend(id)[0]        
        # symbol = getCoinData(id)               
        id = symbol["id"]
        code = symbol["symbol"]
        name = symbol["name"]
        current_price = symbol["market_data"]["current_price"][currency]
        price_change_percentage_1h = symbol["market_data"]["price_change_percentage_1h_in_currency"][currency]
        price_change_percentage_24h = symbol["market_data"]["price_change_percentage_24h"]
        price_change_percentage_7d = symbol["market_data"]["price_change_percentage_7d"]
        price_change_percentage_30d = symbol["market_data"]["price_change_percentage_30d"]
        total_volume = symbol["market_data"]["total_volume"][currency]
        ath = symbol["market_data"]["ath"][currency]
        atl = symbol["market_data"]["atl"][currency]    
        ath_date = convertDate(symbol["market_data"]["ath_date"][currency])     
        atl_date = convertDate(symbol["market_data"]["atl_date"][currency])
        ath_change_percentage = symbol["market_data"]["ath_change_percentage"][currency]    
        atl_change_percentage = symbol["market_data"]["atl_change_percentage"][currency]        
        updateTime = symbol["updateTime"]
        percent2resistance = symbol["percent2resistance"]
        
        format = f"<b>COIN SUMMARY</b> : {name} | {code.upper()} @ {updateTime} \n"
        format = format + f"price = ${current_price:,} \n"
        format = format + f"% 1h = {round(price_change_percentage_1h,2)}% \n"
        format = format + f"% 24h = {round(price_change_percentage_24h,2)}% \n"
        format = format + f" % 7d = {round(price_change_percentage_7d,2)}% \n"
        format = format + f" % 30d = {round(price_change_percentage_30d,2)}% \n"            
        format = format + f"volume = {total_volume:,} \n"
        format = format + f"% ath = ${ath} @ {ath_date}, {round(ath_change_percentage,2)}% \n"    
        format = format + f"% atl = ${atl} @ {atl_date}, {round(atl_change_percentage,2)}% \n"
        format = format + f"% 2Res = ${percent2resistance}%"
        print(format)
        # telegram_sendMessage(format)
        return format
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def topcapSummarize():
    topcap = searchTopCap()
    
    format = f"<b>TOPCAP SUMMARY</b> : \n"
    for symbol in topcap:
        id = symbol["id"]
        code = symbol["symbol"]
        name = symbol["name"]
        current_price = symbol["market_data"]["current_price"][currency]
        price_change_percentage_24h = round(symbol["market_data"]["price_change_percentage_24h"],2)
        updateTime = symbol["updateTime"]
        percent2resistance = symbol["percent2resistance"]
        market_cap_rank = symbol["market_cap_rank"]      
        market_cap = symbol["market_data"]["market_cap"][currency]
        
        format = format + f"{market_cap_rank}. {id.upper()} ({code}) 💎MC: ${market_cap:,} 💰USD: ${current_price:,} {price_change_percentage_24h}% 📈{percent2resistance}% 2Res  \n"                
    format = format + f"Update @ {updateTime}"
    return format

def marketSummarize():
    threshold_change_percentage_1h = 3
    threshold_change_percentage_24h = 15
    threshold_change_percentage_7d = 150
    threshold_change_percentage_30d = 300
    threshold_ath_change_percentage = 5
    threshold_percent2resistance = 5
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
        fl2Resistance = False

        id = symbol["id"]         
        name = symbol["name"]
        code = symbol["symbol"]
        current_price = symbol["market_data"]["current_price"][currency]
        price_change_percentage_1h = symbol["market_data"]["price_change_percentage_1h_in_currency"][currency]
        price_change_percentage_24h = symbol["market_data"]["price_change_percentage_24h"]
        price_change_percentage_7d = symbol["market_data"]["price_change_percentage_7d"]
        price_change_percentage_30d = symbol["market_data"]["price_change_percentage_30d"]
        total_volume = symbol["market_data"]["total_volume"][currency]
        ath = symbol["market_data"]["ath"][currency]
        atl = symbol["market_data"]["atl"][currency]
        ath_date = convertDate(symbol["market_data"]["ath_date"][currency])     
        atl_date = convertDate(symbol["market_data"]["atl_date"][currency])
        ath_change_percentage = symbol["market_data"]["ath_change_percentage"][currency]    
        atl_change_percentage = symbol["market_data"]["atl_change_percentage"][currency]       
        percent2resistance = symbol["percent2resistance"]
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
        if type(percent2resistance) != str:
            if percent2resistance < threshold_percent2resistance and percent2resistance > -threshold_percent2resistance:
                flnotif = True
                fl2Resistance = True

        if flnotif:
            notif = f"- {id.upper()} | {code.upper()} "
        if flath:
            notif = notif + f"${current_price:,}, ATH ${ath}, "
        if flatl:
            notif = notif + f"${current_price:,}, ATL ${ath}, "
        if flPriceChangeUp1h:
            notif = notif + f"📈 {round(price_change_percentage_1h,2)}% 1H, "
        if flPriceChangeDown1h:
            notif = notif + f"📉 {round(price_change_percentage_1h,2)}% 1H, "
        if flPriceChangeUp24h:
            notif = notif + f"📈 {round(price_change_percentage_24h,2)}% 24H, "
        if flPriceChangeDown24h:
            notif = notif + f"📉 {round(price_change_percentage_24h,2)}% 24H, "
        if flPriceChangeUp7d and (price_change_percentage_24h != price_change_percentage_7d):
            notif = notif + f"📈 {round(price_change_percentage_7d,2)}% 7D, "
        if flPriceChangeDown7d and (price_change_percentage_24h != price_change_percentage_7d):
            notif = notif + f"📉 {round(price_change_percentage_7d,2)}% 7D, "
        if flPriceChangeUp30d and (price_change_percentage_24h != price_change_percentage_30d):
            notif = notif + f"📈 {round(price_change_percentage_30d,2)}% 30D, "
        if flPriceChangeDown30d and (price_change_percentage_24h != price_change_percentage_30d):
            notif = notif + f"📉 {round(price_change_percentage_30d,2)}% 30D, "
        if fl2Resistance:
            notif = notif + f"🧨{round(percent2resistance,2)}%"
        if flnotif:                    
            content.append(notif)
            
    if content:
        result = "\n".join(content)        
        return result

def getSupportResistanceArray(df):    
    # ticker = yfinance.Ticker(symbol+'-'+currency.upper())
    # data = ticker.info
    # start_time = '2021-05-01'
    # end_time = datetime.now().strftime("%Y-%m-%d")
    # df = ticker.history(interval="1d",start=start_time, end=end_time)    

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
    return levels
    
    
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

def chartGenerator(df, tickerID, levels=None):   
    try:                          
        plt.rcParams['figure.figsize'] = [16, 9]
        plt.rc('font', size=16)
        fig, ax = plt.subplots()
        candlestick_ohlc(ax,df.values,width=0.1, colorup='green', colordown='red', alpha=0.8)   
        
        if levels is not None:
            for level in levels:
                plt.hlines(level[1],xmin=df['Date'][level[0]],xmax=max(df['Date']),colors='blue')             
        
        # ax.set_xlabel('Date')
        # ax.set_ylabel('Price')
        # ax.set_facecolor('xkcd:black')
        date_format = mpl_dates.DateFormatter('%d %b %Y')
        ax.xaxis.set_major_formatter(date_format)        
        ax.grid(True)        
        ax.set_title(f'Chart Trend Coin {tickerID}', y=1.0, pad=10)
        # fig.autofmt_xdate()
        # fig.patch.set_facecolor('xkcd:grey')  
        fig.tight_layout()                       
              
        fig.show()                                
        # plt.suptitle(f'created by moramad.tech',fontsize=12)
        plt.savefig(f'chart/chart_{tickerID}.png')
        plt.close('all')
        print(f"Chart {tickerID} generated!")
    except Exception as e:
        print("An Error occured in chartGenerator :: ", e)
        return False             

def generateChart(id):
    id = id.lower()
    result = cg.get_coin_ohlc_by_id(id=id,vs_currency=currency,days=days)
    df = pd.DataFrame(result)
    df.columns = ["Date","Open","High","Low","Close"]
    df['Date'] = pd.to_datetime(df['Date'],unit='ms')
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']] 

    levels = getSupportResistanceArray(df)
    chartGenerator(df,id, levels)

def coreAnalytic():
    listSymbol = searchSymbols()
    for symbol in listSymbol:        
        symbolType = symbol["symbolType"]  
        symbolID = symbol["symbolID"]      
        tickerID = symbol["tickerID"]        
        if symbolType == "crypto":                        
            try:   
                result = cg.get_coin_ohlc_by_id(id=tickerID,vs_currency=currency,days=days)
                df = pd.DataFrame(result)
                df.columns = ["Date","Open","High","Low","Close"]
                df['Date'] = pd.to_datetime(df['Date'],unit='ms')
                df['Date'] = df['Date'].apply(mpl_dates.date2num)
                df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]                             

                updateTime = datetime.today()

                levels = getSupportResistanceArray(df)
                supports = []
                for level in levels :
                    support = rounding(level[1])
                    supports.append(support)

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
                chartGenerator(df, tickerID, levels)
            except Exception as e:
                print("An Error occured in coreAnalytic :: ", e)
                return False
    return True    

def main():
    print("coreAnalyzer")
    print(marketSummarize())
    # print(topcapSummarize())
    # priceSummarize("bitcoin")
    # supports = getSupportResistanceArray("DOGE")     
    # getSupportResistance("btc")
    # getSupportResistance("ada")    
    # coreAnalytic()
    # generateChart("bitcoin")

if __name__ == "__main__":    
    main()