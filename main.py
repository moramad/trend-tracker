from masterSymbols import *
from masterAccounts import *
from dataCatcher import *
import csv
  
# os.environ['http_proxy'] = 'http://10.9.20.27:3128/'
# os.environ['https_proxy'] = 'http://10.9.20.27:3128/'
# os.environ['no_proxy']='localhost,127.0.0.1,*.astra-honda.com,10.*'

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
    # print("test")    
    # unregisterSymbols()
    # registerCoins()
    # registerStock()     
    # deleteTrend()   
    print(trendUpdater1())    
    print(trendUpdater2())    

if __name__ == "__main__":    
    main()