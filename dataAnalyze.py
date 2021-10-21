from datetime import datetime
from masterSymbols import *
from masterHistories import *
from dataCatcher import *
from dataModels import *
from notifications import *

import logging 
logging.basicConfig(format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',level=logging.INFO,filename='trendTracker.log')
logger = logging.getLogger('trendTracker')

currency = "usd"

def priceSummarize(id):
    try:        
        item = searchHistory(id)[0]        
        # item = getCoinData(id)               
        id = item["id"]
        symbol = item["symbol"]
        name = item["name"]
        current_price = item["current_price"]
        price_change_percentage_1h = item["price_change_percentage_1h"]
        price_change_percentage_24h = item["price_change_percentage_24h"]
        price_change_percentage_7d = item["price_change_percentage_7d"]
        price_change_percentage_30d = item["price_change_percentage_30d"]        
        ath = item["ath"]
        atl = item["atl"]
        ath_date = item["ath_date"]
        atl_date = item["atl_date"]
        ath_change_percentage = item["ath_change_percentage"]
        atl_change_percentage = item["atl_change_percentage"]
        trend_current_price = item["trend_current_price"]
        count_trend_current_price = item["count_trend_current_price"]
        percent_trend_current_price = item["percent_trend_current_price"]
        updateTime = item["updateTime"]
        # percent_2_resistance = item["percent_2_resistance"]
        
        format = f"<b>COIN SUMMARY</b> :\n"          
        format = format + f"{name} | {symbol.upper()} | {id} \n"
        format = format + f"💵💲{current_price:,} | "
        if trend_current_price >= 0 :
            format = format + f"⬆💲{trend_current_price} | {percent_trend_current_price}% | {count_trend_current_price} \n"
        elif trend_current_price < 0 :
            format = format + f"⬇💲{trend_current_price} | {percent_trend_current_price}% | {count_trend_current_price} \n"
        format = format + f"📈1H {round(price_change_percentage_1h,2)}% 📈24H {round(price_change_percentage_24h,2)}% 📈7D {round(price_change_percentage_7d,2)}% 📈30D {round(price_change_percentage_30d,2)}% \n"                                 
        format = format + f"ATH💲{ath:,} | {round(ath_change_percentage,2)}% | 📅{ath_date}\n"    
        format = format + f"ATL💲{atl:,} | {round(atl_change_percentage,2)}% | 📅{atl_date}\n"
        # format = format + f"💣 ${percent_2_resistance}%"
        print(format)
        # telegram_sendMessage(format)
        return format
    except Exception as e:
        print("An Error occured in priceSummarize: ", e)
        return False

def topcapSummarize():
    topcap = searchTopCap()
    
    format = f"<b>TOPCAP SUMMARY</b> : \n"
    for item in topcap:
        id = item["id"]
        symbol = item["symbol"]
        name = item["name"]
        current_price = item["current_price"]
        price_change_percentage_24h = round(item["price_change_percentage_24h"],2)
        updateTime = item["updateTime"]
        percent_2_resistance = item["percent_2_resistance"]
        market_cap_rank = item["market_cap_rank"]      
        ath = item["ath"]
        atl = item["atl"]
        percent_trend_current_price = item["percent_trend_current_price"]
        support = item["support"]
        resistance = item["resistance"]

        format = format + f"{market_cap_rank}. {id.upper()} ({symbol}) 💰${current_price:,} H💲{ath:,} | L💲{atl:,} "
        if percent_trend_current_price < 0 :
            format = format + f"⬇{percent_trend_current_price}% "
        else :
            format = format + f"⬆{percent_trend_current_price}% "
        if price_change_percentage_24h < 0 :
            format = format + f"📉24H {price_change_percentage_24h}% "
        else :
            format = format + f"📈24H {price_change_percentage_24h}% "    
        if type(percent_2_resistance) != str :
            format = format + f"S/R {support:,}/{resistance:,} 💣{percent_2_resistance}% \n"
        else:
            format = format + f"\n"
    # format = format + f"Update @ {updateTime}"
    return format

def bestSummarize():
    best = searchBest()
    
    format = f"<b>BEST SUMMARY</b> : \n"
    urut = 1
    for item in best:
        id = item["id"]
        symbol = item["symbol"]
        name = item["name"]
        current_price = item["current_price"]       
        price_change_percentage_1h = round(item["price_change_percentage_1h"],2)
        updateTime = item["updateTime"]
        percent_2_resistance = item["percent_2_resistance"]
        market_cap_rank = item["market_cap_rank"]      
        ath = item["ath"]
        atl = item["atl"]
        percent_trend_current_price = item["percent_trend_current_price"]
        support = item["support"]
        resistance = item["resistance"]
        
        format = format + f"{urut}. {id.upper()} ({symbol}) 💰${current_price:,} H💲{ath:,} | L💲{atl:,} "
        if percent_trend_current_price < 0 :
            format = format + f"⬇{percent_trend_current_price}% "
        else :
            format = format + f"⬆{percent_trend_current_price}% "
        if price_change_percentage_1h < 0 :
            format = format + f"📉1H {price_change_percentage_1h}% "
        else :
            format = format + f"📈1H {price_change_percentage_1h}% "    
        if type(percent_2_resistance) != str :
            format = format + f"S/R {support:,}/{resistance:,} 💣{percent_2_resistance}% \n"
        else:
            format = format + f"\n"
        
        urut += 1    
    return format

def worstSummarize():
    worst = searchWorst()
    
    format = f"<b>WORST SUMMARY</b> : \n"
    urut = 1
    for item in worst:        
        id = item["id"]        
        symbol = item["symbol"]
        name = item["name"]
        current_price = item["current_price"]
        price_change_percentage_1h = round(item["price_change_percentage_1h"],2)
        updateTime = item["updateTime"]
        percent_2_resistance = item["percent_2_resistance"]
        market_cap_rank = item["market_cap_rank"]      
        ath = item["ath"]
        atl = item["atl"]
        percent_trend_current_price = item["percent_trend_current_price"]
        support = item["support"]
        resistance = item["resistance"]
        
        format = format + f"{urut}. {id.upper()} ({symbol}) 💰${current_price:,} H💲{ath:,} | L💲{atl:,} "
        if percent_trend_current_price < 0 :
            format = format + f"⬇{percent_trend_current_price}% "
        else :
            format = format + f"⬆{percent_trend_current_price}% "
        if price_change_percentage_1h < 0 :
            format = format + f"📉1H {price_change_percentage_1h}% "
        else :
            format = format + f"📈1H {price_change_percentage_1h}% "    
        if type(percent_2_resistance) != str :
            format = format + f"S/R {support:,}/{resistance:,} 💣{percent_2_resistance}% \n"
        else:
            format = format + f"\n"
        
        urut += 1            
    return format

def suggestSummarize():
    suggest = searchSuggest()

    format = f"<b>SUGGEST SUMMARY</b> : \n"
    urut = 1
    for item in suggest:        
        id = item["id"]        
        symbol = item["symbol"]
        name = item["name"]
        current_price = item["current_price"]
        price_change_percentage_1h = round(item["price_change_percentage_1h"],2)
        updateTime = item["updateTime"]
        percent_2_resistance = item["percent_2_resistance"]
        market_cap_rank = item["market_cap_rank"]      
        ath = item["ath"]
        atl = item["atl"]
        percent_trend_current_price = item["percent_trend_current_price"]
        support = item["support"]
        resistance = item["resistance"]
        
        format = format + f"{urut}. {id.upper()} ({symbol}) 💰${current_price:,} H💲{ath:,} | L💲{atl:,} "
        if percent_trend_current_price < 0 :
            format = format + f"⬇{percent_trend_current_price}% "
        else :
            format = format + f"⬆{percent_trend_current_price}% "
        if price_change_percentage_1h < 0 :
            format = format + f"📉1H {price_change_percentage_1h}% "
        else :
            format = format + f"📈1H {price_change_percentage_1h}% "    
        if type(percent_2_resistance) != str :
            format = format + f"S/R {support:,}/{resistance:,} 💣{percent_2_resistance}% \n"
        else:
            format = format + f"\n"
        
        urut += 1  
    return format

if __name__ == "__main__":
    print("dataAnalyze")
    # priceSummarize('bitcoin')
    # telegram_sendMessage(topcapSummarize())
    # telegram_sendMessage(bestSummarize())
    telegram_sendMessage(suggestSummarize())
