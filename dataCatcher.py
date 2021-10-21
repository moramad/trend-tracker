from datetime import datetime
import time
from pycoingecko import CoinGeckoAPI
import yfinance as yf
from masterSymbols import *
from masterTrends import *
from masterHistories import *

import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import numpy as np

import logging 
logging.basicConfig(format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',level=logging.INFO,filename='trendTracker.log')
logger = logging.getLogger('trendTracker')

cg = CoinGeckoAPI()
currency = "usd"
days = "30"

# inactive
def getCoinPrice(id):
    try:
        coin = cg.get_coin_by_id(id, tickers=False, community_data=False, developer_data=False, sparkline=False)        
    except:        
        result = False
    return coin
# inactive
def getStockPrice(emitten):
    try:
        ticker = yf.Ticker(emitten)    
        data = ticker.info    
        data = data["currentPrice"]
        # data = data.get("currentPrice")
    except Exception as e:
        logger.error(f"An Error occured in getStockPrice :: {e}")
        return False
    return data
# active
def getCoinData(id):
    try:
        result = cg.get_coin_by_id(id)
        return result
    except Exception as e:
        logger.error(f"An Error occured in getCoinData :: {e}")
        return False

# inactive
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
                
            except:                              
                return False
    return True

def dataUpdater():
    logging.info("Start Data Catcher")
    listSymbol = searchSymbols()
    for item in listSymbol:        
        symbolID = item["symbolID"]
        symbolType = item["symbolType"]
        tickerID = item["tickerID"]      
        if symbolType == "crypto":                        
            try:                  
                # v1
                # datatrend = searchTrend(tickerID)[0]               
                # updateTime = datatrend["updateTime"]                

                # v2
                datatrend = getCoinData(tickerID)
                updateTime = datetime.today()
                datatrend.update({"updateTime": updateTime})

                try:
                    datahistory = searchHistory(tickerID)[0]
                    last_updateTime = datahistory["updateTime"]                    
                    print(f"Update Data {tickerID}")
                    # logging.info(f"Update Data {tickerID}")
                    initialize = False
                except:                    
                    # logging.info(f"Insert Data {tickerID}")
                    initialize = True
                                        
                # data current
                id = datatrend["id"]
                symbol = datatrend["symbol"]
                name = datatrend["name"]                            
                updateTime = datatrend["updateTime"]
                current_price = datatrend["market_data"]["current_price"][currency]
                high = datatrend["market_data"]["high_24h"][currency]
                low = datatrend["market_data"]["low_24h"][currency]
                market_cap = datatrend["market_data"]["market_cap"][currency]
                market_cap_rank = datatrend["market_cap_rank"]
                price_change_percentage_1h = datatrend["market_data"]["price_change_percentage_1h_in_currency"][currency]
                price_change_percentage_24h = datatrend["market_data"]["price_change_percentage_24h"]
                price_change_percentage_7d = datatrend["market_data"]["price_change_percentage_7d"]
                price_change_percentage_30d = datatrend["market_data"]["price_change_percentage_30d"]
                total_volume = datatrend["market_data"]["total_volume"][currency]
                ath = datatrend["market_data"]["ath"][currency]
                atl = datatrend["market_data"]["atl"][currency]    
                ath_date = convertDate(datatrend["market_data"]["ath_date"][currency])     
                atl_date = convertDate(datatrend["market_data"]["atl_date"][currency])
                ath_change_percentage = datatrend["market_data"]["ath_change_percentage"][currency]    
                atl_change_percentage = datatrend["market_data"]["atl_change_percentage"][currency]        
                updateTime = datatrend["updateTime"]
                
                # data prev
                if initialize :
                    trend_current_price = 0
                    count_trend_current_price = 0
                    percent_trend_current_price = 0
                else:
                    last_updateTime = datahistory["updateTime"]
                    last_current_price = datahistory["current_price"]
                    last_high = datahistory["high"]
                    last_low = datahistory["low"]
                    last_market_cap = datahistory["market_cap"]
                    # formula
                    # intervalTime = updateTime - last_updateTime
                    trend_current_price = round(current_price - last_current_price,2)
                    percent_trend_current_price = round((trend_current_price / last_current_price) * 100,2)
                    count_trend_current_price = datahistory["count_trend_current_price"]      

                    if trend_current_price > 0 : 
                        count_trend_current_price += 1
                    elif trend_current_price < 0 : 
                        count_trend_current_price -= 1
                    else :
                        count_trend_current_price = 0
                
                # construct data
                coin = {}
                coin.update({"id": id.lower()})
                coin.update({"symbol": symbol.lower()})    
                coin.update({"name": name.lower()})                
                coin.update({"current_price": current_price})
                coin.update({"high": high})
                coin.update({"low": low})                
                coin.update({"price_change_percentage_1h": price_change_percentage_1h})
                coin.update({"price_change_percentage_24h": price_change_percentage_24h})
                coin.update({"price_change_percentage_7d": price_change_percentage_7d})
                coin.update({"price_change_percentage_30d": price_change_percentage_30d})
                coin.update({"market_cap": market_cap})
                coin.update({"market_cap_rank": market_cap_rank})
                coin.update({"total_volume": total_volume})
                coin.update({"ath": ath})
                coin.update({"atl": atl})
                coin.update({"ath_date": ath_date})
                coin.update({"atl_date": atl_date})
                coin.update({"ath_change_percentage": ath_change_percentage})
                coin.update({"atl_change_percentage": atl_change_percentage})

                coin.update({"trend_current_price": trend_current_price})
                coin.update({"count_trend_current_price": count_trend_current_price})
                coin.update({"percent_trend_current_price": percent_trend_current_price})
                coin.update({"updateTime": updateTime})    
                # coin.update({"intervalTime": intervalTime})                
                result = updateHistory(coin)                                     
            except Exception as e:                
                print("An Error occured in dataUpdater : ", e)
                logging.error("Data catcher error : ", e)
                return False    
    logging.info("Finish Data Catcher")

# inactive
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

# SupportResistance
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
        logger.error(f"An Error occured in chartGenerator :: {e}")
        return False             

def getSupportResistance():
    logger.info("Start Get Support Resistance Loop")
    listSymbol = searchSymbols()
    for item in listSymbol:        
        symbolType = item["symbolType"]  
        symbolID = item["symbolID"]      
        tickerID = item["tickerID"]        
        if symbolType == "crypto":                        
            try:   
                updateTime = datetime.today()
                result = cg.get_coin_ohlc_by_id(id=tickerID,vs_currency=currency,days=days)
                df = pd.DataFrame(result)
                df.columns = ["Date","Open","High","Low","Close"]
                df['Date'] = pd.to_datetime(df['Date'],unit='ms')
                df['Date'] = df['Date'].apply(mpl_dates.date2num)
                df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]                                             

                levels = getSupportResistanceArray(df)
                supports = []
                for level in levels :
                    support = rounding(level[1])
                    supports.append(support)

                coinData = searchHistory(tickerID)[0]  
                current_price = coinData["current_price"]    
                supres = takeClosest(current_price, supports)                                
                print(f"{symbolID} | {tickerID} | {supports} | {current_price}")

                if supres and len(supports)>1 and len(supres)>1:                                                                 
                    try:
                        support = supres[0]
                        resistance = supres[1]
                        percent_2_resistance = round(((current_price - support) / (resistance - support)) * 100,2)                        
                    except Exception as e:                        
                        logger.error(f"An Error Occured when calculate percent_2_resistance : {e}")
                        percent_2_resistance = "NA"                                            
                else:
                    support = 0
                    resistance = 0
                    percent_2_resistance = "NA"
                
                coin = {}                
                coin.update({"id": tickerID})                
                coin.update({"updateTime": updateTime})
                coin.update({"supports": supports})
                coin.update({"support": support})
                coin.update({"resistance": resistance})
                coin.update({"percent_2_resistance": percent_2_resistance})    
                updateHistorySupportResistance(coin)                                
                chartGenerator(df, tickerID, levels)
            except Exception as e:
                logger.error(f"An Error occured in getSupportResistance :: {e}")
                return False
    logger.info("Finish Get Support Resistance Loop")
    return True    

if __name__ == "__main__":    
    print("dataCatcher")     
    # print(trendUpdater())    
    dataUpdater()
    time.sleep(60)
    getSupportResistance()
    

