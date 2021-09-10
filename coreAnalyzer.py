from notifications import *
from dataModels import *
from masterTrends import *

def analyze():
    threshold_change_percentage = 0
    listSymbol = searchTrend()
    content = []
    for symbol in listSymbol:        
        id = symbol["symbol"]
        price_change_percentage_24h = symbol["market_data"]["price_change_percentage_24h"]
        current_price = symbol["market_data"]["current_price"]["usd"]

        if price_change_percentage_24h > threshold_change_percentage :
            result = f"{id} saat ini ${current_price}, naik {round(price_change_percentage_24h, 2)}%"
        if price_change_percentage_24h < threshold_change_percentage :
            result = f"{id} saat ini ${current_price}, turun {round(price_change_percentage_24h, 2)}%"        
        content.append(result)      
    result = "\n".join(content)
    print(result)
    telegram_sendMessage(result)

def main():
    print("coreAnalyzer")
    analyze()

if __name__ == "__main__":    
    main()