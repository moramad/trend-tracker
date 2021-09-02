from masterSymbols import *
  
# os.environ['http_proxy'] = 'http://10.9.20.27:3128/'
# os.environ['https_proxy'] = 'http://10.9.20.27:3128/'
# os.environ['no_proxy']='localhost,127.0.0.1,*.astra-honda.com,10.*'

def registerCoin():
    print("register new coin..")
    with open("coins.idx") as indexCoin:
        for line in indexCoin:
            id = line.strip()
            try:                
                coin = Symbols(id,"crypto",True,id)
                if registerSymbols(coin) :
                    print (f"coin {id} is complete registered")
            except:
                print("Error!")
    print("finished register coin")

def main():
    print("test")

if __name__ == "__main__":    
    main()