from dataModels import *
from bson.json_util import dumps, loads
import json, pymongo

###################
def configIndex():
    try:        
        result = dbSymbol.create_index([("symbolID", pymongo.DESCENDING), ("tickerID", pymongo.ASCENDING)],unique=True)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def registerSymbols(symbol):    
    try:          
        result = dbSymbol.insert_one(symbol)
        return True
    except pymongo.errors.DuplicateKeyError:
        # symbolID = symbol["symbolID"]
        # print (f"key {symbolID} is duplicate!")
        return False
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def updateTickerSymbols(symbolID, tickerID):    
    query = {'symbolID': symbolID}
    set = {
        "$set": {
            "tickerID" : tickerID
        }
    }    

    try:        
        result = dbSymbol.update_many(query, set)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def searchSymbols(query=None):
    try:        
        if query is None :
            query = {"allowUpdate":True}
            result = dbSymbol.find(query)
        if query is not None :
            result = dbSymbol.find(query)        
        listSymbol = []
        for item in result:
            listSymbol.append(item)    
        return listSymbol        
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def getListSymbols():
    try:        
        result = dbSymbol.find({}, {'tickerID': 1, '_id': 0})        
        listSymbol = []
        for item in result:
            listSymbol.append(item["tickerID"])    
        return listSymbol        
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def unregisterSymbols(query=None):    
    try:           
        if query is None :
            result = dbSymbol.delete_many({})
        if query is not None :
            result = dbSymbol.delete_many(query)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

    # bentuk resultnya macem apa, misal status success.
    return result

def enableSymbols(query=None):
    set = {
        "$set": {
            "allowUpdate" : True
        }
    }    

    try:        
        if query is None :
            result = dbSymbol.update_many({}, set)
        if query is not None :
            result = dbSymbol.update_many(query, set)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def disableSymbols(query=None):
    set = {
        "$set": {
            "allowUpdate" : False
        }
    }    

    try:        
        if query is None :
            result = dbSymbol.update_many({}, set)
        if query is not None :
            result = dbSymbol.update_many(query, set)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False


def main():
    # asii = Symbols("ASII","stock",False,"ASII.JK")        
    # print(registerSymbols(asii))
    # print(asii["symbolID"])
    updateTickerSymbols("STETH","staked-ether")
    # print(searchSymbols({}))
    # print(getListSymbols())    
    # unregisterSymbols({'symbolID':'ASII'})
    # unregisterSymbols()
    # coin = Symbols("BTC","crypto",False,"bitcoin")       
    # print(registerSymbols(coin))
    # configIndex()
    # enableSymbols()
    
    # emittenJSON = json.dumps(emitten)
    # print(emittenJSON)
    # emittenJSONData = json.loads(emittenJSON)
    # print(emittenJSONData['symbolID'])
    print("masterSymbols")

if __name__ == "__main__":
    main()