from notifications import *
from dataModels import *
from masterTrends import *

def analyze():
    threshold_change_percentage_24h = 3
    threshold_change_percentage_7d = 20
    threshold_change_percentage_30d = 40
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

        # format = f"harga {id} = {current_price} \n"
        # format = format + f"price_change_percentage_24h = {price_change_percentage_24h} \n"
        # format = format + f"price_change_percentage_7d = {price_change_percentage_7d} \n"
        # format = format + f"price_change_percentage_30d = {price_change_percentage_30d} \n"
        # format = format + f"total_volume = {total_volume} \n"
        # format = format + f"ath = {ath} \n"
        # format = format + f"ath_change_percentage = {ath_change_percentage} \n"
        # format = format + f"atl = {atl} \n"
        # format = format + f"atl_change_percentage = {atl_change_percentage} \n"
        # print(format)
        
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
        # telegram_sendMessage(result)

def main():
    print("coreAnalyzer")
    analyze()

if __name__ == "__main__":    
    main()