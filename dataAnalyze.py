from datetime import datetime, timedelta
import datetime
from masterSymbols import *
from masterHistories import *
from dataCatcher import *
from dataModels import *

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
        updateTime = item["updateTime"] + timedelta(hours=7)        
        waktu = updateTime.strftime("%x %X")
        percent_2_resistance = item["percent_2_resistance"]
        
        format = f"<b>COIN SUMMARY</b> : {waktu}\n"          
        format = format + f"{name} | {symbol.upper()} | {id} \n"
        format = format + f"💵💲{current_price:,} | "

        if trend_current_price >= 0 :
            format = format + f"⬆💲{trend_current_price} | {percent_trend_current_price}% | {count_trend_current_price} \n"
        elif trend_current_price < 0 :
            format = format + f"⬇💲{trend_current_price} | {percent_trend_current_price}% | {count_trend_current_price} \n"
        
        if price_change_percentage_1h >= 0 :
            format = format + f"📈1H {round(price_change_percentage_1h,2)}% "
        elif price_change_percentage_1h < 0 :
            format = format + f"📉1H {round(price_change_percentage_1h,2)}% "
        if price_change_percentage_24h >= 0 :
            format = format + f"📈24H {round(price_change_percentage_24h,2)}% "
        elif price_change_percentage_24h < 0 :
            format = format + f"📉24H {round(price_change_percentage_24h,2)}% "
        if price_change_percentage_7d >= 0 :
            format = format + f"📈1H {round(price_change_percentage_7d,2)}% "
        elif price_change_percentage_7d < 0 :
            format = format + f"📉1H {round(price_change_percentage_7d,2)}% "
        if price_change_percentage_30d >= 0 :
            format = format + f"📈1H {round(price_change_percentage_30d,2)}% \n"
        elif price_change_percentage_30d < 0 :
            format = format + f"📉1H {round(price_change_percentage_30d,2)}% \n"

        format = format + f"ATH💲{ath:,} | {round(ath_change_percentage,2)}% | 📅{ath_date}\n"    
        format = format + f"ATL💲{atl:,} | {round(atl_change_percentage,2)}% | 📅{atl_date}\n"

        format = format + f"💣 ${percent_2_resistance}%"
        print(format)
        # telegram_sendMessage(format)
        return format
    except Exception as e:
        logger.error(f"An Error occured in priceSummarize :: {e}")
        print("An Error occured priceSummarize: ", e)
        return False

def topcapSummarize():
    try:
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
    except Exception as e:
        logger.error(f"An Error occured in topcapSummarize :: {e}")
        print("An Error occured topcapSummarize: ", e)

def bestSummarize():
    try:
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
    except Exception as e:
        logger.error(f"An Error occured in bestSummarize :: {e}")
        print("An Error occured bestSummarize: ", e)

def worstSummarize():
    try:
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
    except Exception as e:
        logger.error(f"An Error occured in worstSummarize :: {e}")
        print("An Error occured worstSummarize: ", e)

def suggestSummarize():
    try:
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
    except Exception as e:
        logger.error(f"An Error occured in suggestSummarize :: {e}")
        print("An Error occured suggestSummarize: ", e)

def marketSummarize():
    try:
        threshold_change_percentage_1h = 1
        threshold_change_percentage_24h = 15
        threshold_change_percentage_7d = 150
        threshold_change_percentage_30d = 300
        threshold_ath_change_percentage = 5
        threshold_percent_2_resistance = 5
        listSymbol = searchHistory()    
        content = []
        
        for item in listSymbol:
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

            id = item["id"]         
            name = item["name"]
            symbol = item["symbol"]
            current_price = item["current_price"]
            price_change_percentage_1h = item["price_change_percentage_1h"]
            price_change_percentage_24h = item["price_change_percentage_24h"]
            price_change_percentage_7d = item["price_change_percentage_7d"]
            price_change_percentage_30d = item["price_change_percentage_30d"]
            total_volume = item["total_volume"]
            ath = item["ath"]
            atl = item["atl"]
            ath_date = convertDate(item["ath_date"])     
            atl_date = convertDate(item["atl_date"])
            ath_change_percentage = item["ath_change_percentage"]    
            atl_change_percentage = item["atl_change_percentage"]       
            percent_2_resistance = item["percent_2_resistance"]
            updateTime = item["updateTime"]
            trend_current_price = item["trend_current_price"]
            count_trend_current_price = item["count_trend_current_price"]
            percent_trend_current_price = item["percent_trend_current_price"]
            
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
            if type(percent_2_resistance) != str:
                if (percent_2_resistance < threshold_percent_2_resistance and percent_2_resistance > -threshold_percent_2_resistance) \
                    or (percent_2_resistance > (100 - threshold_percent_2_resistance) and percent_2_resistance < (100 + threshold_percent_2_resistance)):
                    flnotif = True
                    fl2Resistance = True
            
            if flnotif:
                notif = f"- {id.upper()} | {symbol.upper()} |"
                notif = notif + f"${current_price:,}, "
            if flath:
                notif = notif + f"ATH ${ath:,}, "
            if flatl:
                notif = notif + f"ATL ${atl:,}, "
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
                notif = notif + f"💣{round(percent_2_resistance,2)}%"
            if flnotif:                    
                content.append(notif)
                
        if content:
            result = "\n".join(content)        
            return result
    except Exception as e:
        logger.error(f"An Error occured in marketSummarize :: {e}")
        print("An Error occured marketSummarize: ", e)

if __name__ == "__main__":
    print("dataAnalyze")
    # priceSummarize('bitcoin')
    # telegram_sendMessage(topcapSummarize())
    # telegram_sendMessage(bestSummarize())
    # telegram_sendMessage(suggestSummarize())
    print(marketSummarize())    
