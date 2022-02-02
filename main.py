# update 03/02/2022

from masterSymbols import *
from masterAccounts import *
from dataCatcher import *
from dataAnalyze import *
import csv

def registerCoins():
    print("register new Coin")
    with open("coins.idx") as indexCoin:
        reader = csv.reader(indexCoin)
        for row in reader:
            id = row[0]
            ticker = row[1]
            coin = Symbols(id,"crypto",True,ticker)
            if registerSymbols(coin) :
                print (f"coin {ticker} is complete registered")

def registerStock():
    print("register new stock..")
    with open("stocks.idx") as indexStock:
        for line in indexStock:
            id = line.strip()
            try:                
                stock = Symbols(id,"stock",True,id.upper() +'.JK')
                if registerSymbols(stock) :
                    print (f"stock {id} is complete registered")
            except:
                print("Error!")
    print("finished register stock")

def main():
    print("main")    
    # unregisterSymbols()
    registerCoins()
    # registerStock()     
    # deleteTrend()   
      

if __name__ == "__main__":    
    main()
