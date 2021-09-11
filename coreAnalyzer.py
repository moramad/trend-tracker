from notifications import *
from dataModels import *
from masterTrends import *

def coinSummarize(id):
    try:
        symbol = getCoinData(id)
        id = symbol["id"]
        code = symbol["symbol"]
        current_price = symbol["market_data"]["current_price"]["usd"]
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

        content = []
        format = f"COIN SUMMARY : {id} \n"
        format = format + f"price = ${current_price} \n"
        format = format + f"change % 24h = {round(price_change_percentage_24h,2)}% \n"
        format = format + f"change % 7d = {round(price_change_percentage_7d,2)}% \n"
        format = format + f"change % 30d = {round(price_change_percentage_30d,2)}% \n"            
        format = format + f"volume = {total_volume} \n"
        format = format + f"ath = ${ath} pada {ath_date}, selisih {round(ath_change_percentage,2)}%  \n"    
        format = format + f"atl = ${atl} pada {atl_date}, selisih {round(atl_change_percentage,2)}%"    
        print(format)
        # telegram_sendMessage(format)
        return format
    except:
        return False

def marketSummarize():
    threshold_change_percentage_24h = 3
    threshold_change_percentage_7d = 10
    threshold_change_percentage_30d = 30
    threshold_ath_change_percentage = 10
    listSymbol = searchTrend()
    content = []
    result = ""
    for symbol in listSymbol:                
        id = symbol["id"]
        code = symbol["symbol"]
        current_price = symbol["market_data"]["current_price"]["usd"]
        price_change_percentage_24h = symbol["market_data"]["price_change_percentage_24h"]
        price_change_percentage_7d = symbol["market_data"]["price_change_percentage_7d"]
        price_change_percentage_30d = symbol["market_data"]["price_change_percentage_30d"]
        total_volume = symbol["market_data"]["total_volume"]["usd"]
        ath = symbol["market_data"]["ath"]["usd"]
        atl = symbol["market_data"]["atl"]["usd"]
        ath_change_percentage = symbol["market_data"]["ath_change_percentage"]["usd"]    
        atl_change_percentage = symbol["market_data"]["atl_change_percentage"]["usd"]        
        
        if ath_change_percentage >= -threshold_ath_change_percentage :
            result = f"harga {id} saat ini ${current_price}, akan mencapai ATH pada ${ath}"
            content.append(result)
        if atl_change_percentage <= threshold_ath_change_percentage :
            result = f"harga {id} saat ini ${current_price}, akan mencapai ATH pada ${ath}"
            content.append(result)
        if price_change_percentage_24h > threshold_change_percentage_24h :
             result = f"harga {id} saat ini ${current_price}, naik {round(price_change_percentage_24h, 2)}% dalam 24 jam"             
             content.append(result)
        if price_change_percentage_24h < -threshold_change_percentage_24h :
             result = f"harga {id} saat ini ${current_price}, turun {round(price_change_percentage_24h, 2)}% dalam 24 jam"             
             content.append(result)
        if price_change_percentage_7d > threshold_change_percentage_7d :
             result = f"harga {id} saat ini ${current_price}, naik {round(price_change_percentage_7d, 2)}% dalam 7 hari"
             content.append(result)
        if price_change_percentage_7d < -threshold_change_percentage_7d :
             result = f"harga {id} saat ini ${current_price}, turun {round(price_change_percentage_7d, 2)}% dalam 7 hari"
             content.append(result)
        if price_change_percentage_30d > threshold_change_percentage_30d :
             result = f"harga {id} saat ini ${current_price}, naik {round(price_change_percentage_30d, 2)}% dalam 30 hari"
             content.append(result)
        if price_change_percentage_30d < -threshold_change_percentage_30d :
             result = f"harga {id} saat ini ${current_price}, turun {round(price_change_percentage_30d, 2)}% dalam 30 hari"                    
             content.append(result)
    if content :
        result = "\n".join(content)
        print(result)
        return result

def main():
    print("coreAnalyzer")
    # marketSummarize()
    # coinSummarize("ethereum")

if __name__ == "__main__":    
    main()